# File: adapters/cortex_a2a_adapter/task_router/server.py
# This module implements the A2A server interface using FastAPI.
# It processes incoming tasks via the task_router module and exposes an endpoint for generating an agent card.
# All HTTP interactions and internal processing steps are logged using the Router Logger.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
import os
import logging

# Import local modules
from . import task_router, artifact_handler
from ..card_generation import agent_card

# Set up the Router Logger
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
ROUTER_LOG_FILE = os.path.join(LOGS_DIR, "router.log")

router_logger = logging.getLogger("RouterLogger")
router_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
router_logger.addHandler(console_handler)
file_handler = logging.FileHandler(ROUTER_LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
router_logger.addHandler(file_handler)

class A2ATask(BaseModel):
    task_id: str
    description: str
    payload: dict

app = FastAPI(title="CortexMesh A2A Adapter Server")

@app.get("/")
async def read_root():
    router_logger.debug("Received request at root endpoint.")
    return {"message": "CortexMesh A2A Adapter Server is running"}

@app.get("/agent_card")
async def get_agent_card():
    try:
        router_logger.debug("Generating agent card.")
        card = agent_card.generate_agent_card()
        return card
    except Exception as e:
        router_logger.error("Error generating agent card: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/task")
async def process_task_endpoint(task: A2ATask):
    try:
        router_logger.debug("Received task via POST: %s", task.dict())
        raw_result = await task_router.process_task(task.dict())
        formatted = await artifact_handler.format_artifact(raw_result)
        return formatted
    except Exception as e:
        router_logger.error("Error processing task: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("adapters.cortex_a2a_adapter.task_router.server:app", host="0.0.0.0", port=8000)
