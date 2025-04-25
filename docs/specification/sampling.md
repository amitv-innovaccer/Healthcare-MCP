# Agent to Agent bi-directional communication

Agent to agent bi-directional communication is implemented by adding [sampling](https://modelcontextprotocol.io/specification/2025-03-26/client/sampling) capability to the HMCP server. The base MCP implementation already has sampling implemented on the client. That way HMCP client and server both can communicate using LLM inputs and output.

## Capabilities

HMCP Server defines `sampling` as a sub-capability under the [experimental](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle#capability-negotiation) capability. 

## Message Flow

Depicting the flow as described in the HMCP Demo files (under examples folder)

```mermaid
sequenceDiagram
    participant AI as AI Agent (Orchestrator)
    participant EMR as EMR Writeback Agent
    participant Patient as Patient Data Access Agent
    
    Note over AI,Patient: Workflow initialization
    
    AI->>EMR: Start EMR Agent (StdioServerParameters)
    Note right of EMR: EMR Agent initializes<br>with HMCPServer and<br>registers sampling handler
    EMR-->>AI: Initialization response
    
    AI->>Patient: Start Patient Agent (StdioServerParameters)
    Note right of Patient: Patient Agent initializes<br>with HMCPServer and<br>registers sampling handler
    Patient-->>AI: Initialization response
    
    AI->>EMR: Connect to EMR via ClientSession
    EMR-->>AI: Connection established (emr_init_result)
    
    Note over AI,EMR: First clinical data request
    AI->>EMR: create_message([clinical_data_message])
    Note right of EMR: Invokes handle_emr_writeback_sampling()
    EMR-->>AI: "Additional information required: Need patient_id"
    
    AI->>Patient: Connect to Patient Agent via ClientSession
    Patient-->>AI: Connection established (patient_init_result)
    
    Note over AI,Patient: Patient ID request
    AI->>Patient: create_message([patient_request_message])
    Note right of Patient: Invokes handle_patient_data_sampling()
    Patient-->>AI: "Patient identifier for John Smith: patient_id=PT12345"
    
    Note over AI,EMR: Final clinical data request with ID
    AI->>EMR: create_message([clinical_data_with_id_message])
    Note right of EMR: Invokes handle_emr_writeback_sampling()
    EMR-->>AI: "Success: Clinical data has been written to the EMR system"
    
    Note over AI,Patient: Workflow completed
```

