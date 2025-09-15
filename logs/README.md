# Logging Overview for CortexMesh A2A Adapter

## TL;DR
- **Agent Logger:** Handles internal reasoning and agent-related output (e.g., TaskClarificationAgent).
- **Router Logger:** Covers API endpoint interactions and all internal processing within the task router (including detailed processing steps).
- **Client Logger:** Records outgoing requests and responses for tasks sent to the A2A adapter server.

### Agent Logger
- **Purpose:**  
  The Agent Logger is dedicated to logging all internal reasoning and outputs produced by our TaskClarificationAgent. It captures detailed diagnostic information about task analysis, such as decision points regarding missing payloads or ambiguous descriptions.
- **Usage Context:**  
  This logger is used within the agent layer. It ensures that the internal logic of the TaskClarificationAgent is fully traceable, providing a granular view of its reasoning process and facilitating production-level debugging and auditability.

### Router Logger
- **Purpose:**  
  The Router Logger manages all log entries related to the FastAPI endpoints and internal processing within the task router. It logs every step—from the receipt of HTTP requests, through task transformation and clarifications, to the final generation of artifact responses.
- **Usage Context:**  
  Deployed in the server, task router, and artifact handler files, this logger ensures that both external interactions (i.e., API calls) and internal workflows are clearly documented. This centralized logging enables easy monitoring of the entire task lifecycle within the A2A adapter.

### Client Logger
- **Purpose:**  
  The Client Logger is responsible for logging all outgoing HTTP requests and the corresponding responses when tasks are sent from the client module to the A2A adapter server.
- **Usage Context:**  
  Located within the client module, this logger tracks every request dispatched and response received. It provides essential insights into client-server communication and aids in verifying that the external interactions of the system work as expected.
