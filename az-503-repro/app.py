import asyncio
import os
from fastapi import FastAPI
from fastapi.responses import Response

import uvicorn

sleep_for = float(os.getenv("SLEEP_FOR", 5))

app = FastAPI()

@app.get("/no-content")
async def no_content():
    return Response("", status_code=204)

@app.post("/hit")
async def hit():
    await asyncio.sleep(sleep_for)
    return "ok"
