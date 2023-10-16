import asyncio
import os
from fastapi import FastAPI

sleep_for = int(os.getenv("SLEEP_FOR", 5))

app = FastAPI()

@app.post("/hit")
async def hit():
    await asyncio.sleep(sleep_for)
    return "ok"
