# File: adapters/cortex_a2a_adapter/task_router/task_router.py
# This module processes A2A tasks by translating them into AG2 agent inputs.
# It leverages the Task Clarification Agent to generate a clarification outline for each task.
# The output is encapsulated into a standardized artifact for downstream orchestration.
# All processing steps are logged using the Router Logger.

import asyncio
import logging
import os
from agents.task_clarification_agent.task_clarification_agent import TaskClarificationAgent

# Set up the Router Logger
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
ROUTER_LOG_FILE = os.path.join(LOGS_DIR, "router.log")

router_logger = logging.getLogger("RouterLogger")
router_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
if not router_logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    router_logger.addHandler(console_handler)
    file_handler = logging.FileHandler(ROUTER_LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    router_logger.addHandler(file_handler)

async def process_task(task: dict) -> dict:
    router_logger.debug("Processing task: %s", task)
    clarifier = TaskClarificationAgent()
    clarification_outline = await clarifier.clarify_task(task)
    router_logger.debug("Clarification outline: %s", clarification_outline)
    artifact = {
        "task_id": task.get("task_id"),
        "status": "complete" if clarification_outline.get("is_complete") else "clarification_needed",
        "artifact": clarification_outline
    }
    router_logger.debug("Generated artifact: %s", artifact)
    return artifact

if __name__ == "__main__":
    async def main():
        test_task = {"task_id": "123", "description": "Test? Analyze data", "payload": {}}
        result = await process_task(test_task)
        print(result)
    
    asyncio.run(main())
