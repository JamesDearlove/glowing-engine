import hashlib
import hmac
import http
import os

import httpx
from fastapi import Header, HTTPException, FastAPI, Request

app = FastAPI()

def generate_hash_signature(secret: bytes, payload: bytes, digest_method=hashlib.sha1):
    return hmac.new(secret, payload, digest_method).hexdigest()

def handle_webhooks(request: Request, event: str):
    address = os.environ.get("PI_ADDRESS")

    if event == "ping":
        httpx.post(f"{address}/chaos")
    elif event == "pull_request":
        httpx.post(f"{address}/pulse", 
            data={"colors": [0x00FF50], "reverse": False})
    elif event == "issue":
        httpx.post(f"{address}/pulse", 
            data={"colors": [0x0ebdf2], "reverse": False})
    elif event == "push":
        httpx.post(f"{address}/pulse", 
            data={"colors": [0xFF0000], "reverse": False})

@app.get("/")
async def root():
    return { "Hello", "World!"}

@app.post("/webhook", status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request, x_hub_signature: str = Header(None), x_github_event: str = Header(None)):
    payload = await request.body()
    secret = os.environ.get("WEBHOOK_SECRET").encode("UTF-8")
    signature = generate_hash_signature(secret, payload)

    if x_hub_signature != f"sha1={signature}":
        raise HTTPException(status_code=401, detail="Authentication error.")

    if x_github_event != "":
        handle_webhooks(request, x_github_event)

    return {}