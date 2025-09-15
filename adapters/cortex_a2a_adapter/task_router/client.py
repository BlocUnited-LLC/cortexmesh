# File: adapters/cortex_a2a_adapter/task_router/client.py
# This module implements a simple A2A client using httpx.
# It provides an asynchronous function to send tasks to the A2A adapter server and logs outgoing requests and responses.
# Logging is configured using the ClientLogger, which writes logs to both the console and a file.

import httpx
import asyncio
import logging
import os

# Set up the logs directory to point to the root-level logs folder.
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
CLIENT_LOG_FILE = os.path.join(LOGS_DIR, "client.log")

client_logger = logging.getLogger("ClientLogger")
client_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console handler for ClientLogger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
client_logger.addHandler(console_handler)

# File handler for ClientLogger
file_handler = logging.FileHandler(CLIENT_LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
client_logger.addHandler(file_handler)

async def send_task(server_url: str, task: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{server_url}/task", json=task)
        response.raise_for_status()
        client_logger.debug("Sent task: %s", task)
        client_logger.debug("Received response: %s", response.json())
        return response.json()

if __name__ == "__main__":
    sample_task = {
        "task_id": "example123",
        "description": "Test task for clarification?",
        "payload": {"data": "example_data"}
    }
    server_url = "http://localhost:8000"
    result = asyncio.run(send_task(server_url, sample_task))
    print("Task result:", result)
