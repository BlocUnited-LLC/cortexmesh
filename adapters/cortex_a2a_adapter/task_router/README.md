# Task Router

The Task Router is a core submodule of the CortexMesh A2A Adapter. It is responsible for receiving incoming tasks, converting them into a structured format that AG2 agents can process, and then preparing the output for further orchestration. The Task Router serves as a critical intermediary between raw task submissions and downstream multi-agent orchestration.

## Overview

**Submodules & Components:**

- **Server:**  
  A FastAPI-based server that exposes endpoints to receive task submissions and to provide agent metadata via an agent card. It logs every HTTP interaction and internal processing step using the dedicated Router Logger.

- **Client:**  
  Provides an asynchronous function to send tasks to the A2A adapter server. This component is used for testing and for external systems to integrate with the adapter. Outgoing requests and their responses are logged using the Client Logger.

- **Task Processing:**  
  The task processing module leverages the Task Clarification Agent from the agent layer to analyze each incoming task. This agent, using its underlying LLM call, produces a robust, JSON-formatted clarification outline that identifies whether additional details are needed. This module is entirely asynchronous and uses the Router Logger to record every step of the processing.

- **Artifact Handling:**  
  Once the task has been analyzed, the output is passed to the Artifact Handler, which enriches the response with a UTC timestamp and protocol version. The Artifact Handler is integrated within the Router logging framework, ensuring that every transformation is traceable.

**Dependencies:**

- The Task Router relies on the Task Clarification Agent (located in the agents layer) for its reasoning. This agent calls its underlying LLM through the production-ready methods provided by AG2 and logs its reasoning and response details using the Agent Logger.
  
- All components are asynchronous, ensuring production readiness and scalability.

## Key Responsibilities

- **Task Reception and Validation:**  
  The Task Router listens for HTTP POST requests containing tasks, validating that each task contains the required fields: a task identifier, a description, and a payload.

- **Task Analysis:**  
  Through an asynchronous call to the Task Clarification Agent, the Task Router analyzes each task to determine if it is complete. If the task lacks necessary details (for example, missing payloads or ambiguous descriptions), the clarification logic produces an outline showing what additional information is required.

- **Standardized Response Formation:**  
  The output from the Task Clarification Agent is encapsulated into an artifact, which the Artifact Handler further augments with metadata such as timestamps and a protocol version. This standardization ensures interoperability across the A2A ecosystem.

- **Logging:**  
  - The **Agent Logger** is used exclusively within the Task Clarification Agent to record details about the internal reasoning and LLM responses.
  - The **Router Logger** documents all API interactions (both endpoint requests and internal task processing) along with the formation of the final artifact.
  - The **Client Logger** tracks outgoing HTTP requests and responses from the client module, ensuring clear visibility of external communication.

## Usage

- **Server Operation:**  
  Deploy the FastAPI server to handle incoming tasks. The server will process each task asynchronously, using the Task Clarification Agent to generate a clarification outline and then assembling a standardized artifact before returning the response.

- **Task Submission:**  
  Tasks submitted through HTTP POST requests are validated and processed by the Task Router. The response clearly indicates whether further clarification is needed, with accompanying details logged for transparency.

- **Client Interaction:**  
  The asynchronous client module is available for testing and integration, sending tasks to the server and logging all communications via the Client Logger.

## Future Enhancements

- **Dynamic Routing:**  
  Implement advanced decision logic for selecting processing paths based on task complexity.
  
- **Extended Multi-Turn Interaction:**  
  Enhance the system to support follow-up interactions when tasks require further clarification.
  
- **Scalability:**  
  Adapt and deploy the Task Router in a distributed manner to handle high volumes of tasks while maintaining robust logging and traceability.
  
- **Monitoring and Alerting:**  
  Integrate centralized monitoring systems to track the log outputs from each dedicated logger, providing real-time operational insights.