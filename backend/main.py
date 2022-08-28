import hashlib
import hmac
import http
import os

import httpx
from fastapi import Header, HTTPException, FastAPI, Request

app = FastAPI()

def generate_hash_signature(secret: bytes, payload: bytes, digest_method=hashlib.sha1):
    return hmac.new(secret, payload, digest_method).hexdigest()

async def handle_webhooks(request: Request, event: str):

    body = await request.json()
    address = os.environ.get("PI_ADDRESS")

    if event == "ping":
        r = httpx.post(f"{address}/chaos")
    elif event.startswith("pull_request"):
        r = httpx.post(f"{address}/pulse", 
            json={"colors": [0x00FF50], "reverse": False})
    elif event.startswith("issues"):

        if body["action"] == "closed":
            r = httpx.post(f"{address}/pulse", 
                json={"colors": [0x72ff72, 0x00FF00, 0x72ff72], "reverse": False})
        elif body["action"] == "opened":
            r = httpx.post(f"{address}/pulse", 
                json={"colors": [0x0050c9, 0x0ebdf2, 0x0050c9], "reverse": False})


    elif event == "push":
        r = httpx.post(f"{address}/pulse", 
            json={"colors": [0xff7572, 0xFF0000, 0xff7572], "reverse": False})

@app.get("/")
async def root():
    return { "Hey", "World!"}

@app.post("/webhook", status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request, x_hub_signature: str = Header(None), x_github_event: str = Header(None)):
    payload = await request.body()
    secret = os.environ.get("WEBHOOK_SECRET").encode("UTF-8")
    signature = generate_hash_signature(secret, payload)


    if x_hub_signature != f"sha1={signature}":
        raise HTTPException(status_code=401, detail="Authentication error.")

    if x_github_event != "":
        await handle_webhooks(request, x_github_event)

    return {}
