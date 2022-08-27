from fastapi import FastAPI, BackgroundTasks

import control
from schemas import PulseParams

app = FastAPI()

@app.get("/")
async def root():
    return { "hello": "world" }

@app.post("/demo")
async def demo(background_tasks: BackgroundTasks):
    background_tasks.add_task(control.demo)
    return {"result": "Running demo"}

@app.post("/pulse")
async def pulse(params: PulseParams, background_tasks: BackgroundTasks):
    background_tasks.add_task(control.pulse, params.colors, params.reverse)
    return {"result": "Pulse queued"}

@app.post("/chaos")
async def chaos(background_tasks: BackgroundTasks):
    background_tasks.add_task(control.chaos)
    return {"result": "Chaos queued"}
