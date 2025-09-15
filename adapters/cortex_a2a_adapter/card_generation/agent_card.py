# File: adapters/cortex_a2a_adapter/card_generation/agent_card.py
"""
This file generates an agent card (agent.json) that describes this agent for the A2A ecosystem.
Includes metadata such as agent name, version, capabilities, endpoints, and license.
"""

import json

def generate_agent_card() -> dict:
    card = {
        "agent_name": "CortexMesh-A2A-Agent",
        "version": "1.0.0",
        "capabilities": ["task_processing", "artifact_generation"],
        "endpoints": {
            "task_endpoint": "http://localhost:8000/task",
            "agent_card_endpoint": "http://localhost:8000/agent_card"
        },
        "contact": "support@cortexmesh.io",  # #NOTE: Update with your actual contact info.
        "license": "Apache-2.0"
    }
    return card

if __name__ == "__main__":
    card = generate_agent_card()
    print(json.dumps(card, indent=4))