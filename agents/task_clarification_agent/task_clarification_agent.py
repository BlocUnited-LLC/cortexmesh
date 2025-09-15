# File: agents/task_clarification_agent/task_clarification_agent.py
# This module defines the TaskClarificationAgent.
# It extends AG2's AssistantAgent to analyze incoming tasks and generate a JSON-formatted clarification outline.
# The agent makes an asynchronous LLM call via its native a_run() method to produce a structured response.
# All LLM interactions and internal reasoning are logged using the AgentLogger.

from autogen import AssistantAgent
from dotenv import load_dotenv
import os
import logging
import asyncio
import json

# Load environment variables from .env file
load_dotenv()

# Set up the Agent Logger to log to both console and a file in the centralized logs folder.
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
AGENT_LOG_FILE = os.path.join(LOGS_DIR, "agent.log")

agent_logger = logging.getLogger("AgentLogger")
agent_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
agent_logger.addHandler(console_handler)
file_handler = logging.FileHandler(AGENT_LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
agent_logger.addHandler(file_handler)

class TaskClarificationAgent(AssistantAgent):
    def __init__(self, name="task_clarifier", llm_config=None):
        system_message = (
            "You are a task clarification agent. Analyze the incoming task and output a JSON-formatted outline that "
            "includes 'task_id', a boolean 'is_complete', and a list 'clarification_points'. "
            "If the task's payload is missing or the description is ambiguous, mark 'is_complete' as false and include "
            "appropriate messages; otherwise, mark it as true."
        )
        # Set human_input_mode to NEVER for fully automated processing.
        super().__init__(name, system_message=system_message, llm_config=llm_config, human_input_mode="NEVER")
        agent_logger.debug("Initialized TaskClarificationAgent with system message: %s", system_message)

    async def clarify_task(self, task: dict) -> dict:
        """
        Asynchronously analyze the incoming task and generate a JSON-formatted clarification outline.

        This method constructs a detailed prompt from the task details, calls the underlying LLM asynchronously 
        using a_run(), and returns a parsed JSON response by examining the message history.
        
        Args:
            task (dict): A dictionary with keys 'task_id', 'description', and 'payload'.
        
        Returns:
            dict: A clarification outline containing:
                  - task_id: The task identifier.
                  - is_complete: A boolean indicating if sufficient information is provided.
                  - clarification_points: A list of strings specifying missing or ambiguous details.
        """
        agent_logger.debug("Received task for clarification: %s", task)
        prompt = (
            f"Analyze the task and generate a JSON output in the following format:\n\n"
            f'{{ "task_id": "<task_id>", "is_complete": true/false, "clarification_points": ["message1", "message2"] }}\n\n'
            f"Task Details:\n"
            f"Task ID: {task.get('task_id')}\n"
            f"Description: {task.get('description')}\n"
            f"Payload: {task.get('payload')}\n\n"
            f"If the payload is missing or the description is ambiguous, set is_complete to false and include clarification messages; "
            f"otherwise, set is_complete to true with an empty clarification_points array."
        )
        agent_logger.debug("Sending prompt to LLM: %s", prompt)
        # Execute the LLM call asynchronously using the native a_run() method.
        llm_response = await self.a_run(message=prompt, user_input=False)
        # Wait for and fetch the message history from the LLM response.
        try:
            messages = await llm_response.messages  # Await the messages if they are async iterable
            if not messages:
                agent_logger.error("LLM returned an empty messages list.")
                raise ValueError("LLM returned an empty messages list.")
            last_message = messages[-1]["content"]
        except Exception as e:
            agent_logger.error("Error retrieving message history: %s", str(e))
            raise e
        
        agent_logger.debug("Raw LLM output extracted from message history: %s", last_message)
        try:
            clarification_outline = json.loads(last_message)
            agent_logger.debug("Parsed LLM response: %s", clarification_outline)
        except json.JSONDecodeError as e:
            agent_logger.error("Failed to decode LLM output as JSON. Received: %s", last_message)
            raise e

        return clarification_outline

# Example usage for testing
if __name__ == "__main__":
    import asyncio
    llm_config = {"model": os.getenv("MODEL"), "api_key": os.getenv("API_KEY")}
    clarifier = TaskClarificationAgent(llm_config=llm_config)
    agent_logger.info("Testing TaskClarificationAgent with sample task.")
    example_task = {
        "task_id": "test_task_1",
        "description": "Analyze sales data?",
        "payload": {}
    }
    async def main():
        outline = await clarifier.clarify_task(example_task)
        print("Clarification Outline:")
        print(outline)
    asyncio.run(main())
