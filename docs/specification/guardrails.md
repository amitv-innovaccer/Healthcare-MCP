# Guardrails

Guardrails are an important differentiator of the HMCP protocol. We define guardrails as part of the `experimetal` capabilities of client and server. You can configure the exact guardrail which needs to be executed for each input/output of the agent (client or server).

Below we show an example of how guardrails can be implemented using Nvidia Nemo Guardrails library.

## Medical Journal Validation Flow

Below is an example of a guardrail which validates LLM response for clinical accuracy by checking against medical journals.

### Key Components

1. **User & LLM**: The entry point for medical questions and initial responses
2. **Guardrails Framework**: The infrastructure that intercepts LLM responses for validation
3. **NeMo Guardrails Actions**: Custom functions that process and validate medical content
4. **MedicalJournalValidator**: Core validation logic against medical literature
5. **Vector DB (Chroma)**: Database of medical journal information stored as vector embeddings

### Workflow Summary

1. System initializes with medical journal database
2. User asks a medical question, LLM generates a response
3. Response is intercepted by guardrails for validation
4. Medical statements are extracted and checked against journal data
5. System adds citations to validated statements or provides corrections for unverified information
6. Final validated response is delivered to the user

This validation system ensures that medical information provided by the LLM is backed by authoritative medical literature, increasing reliability and trustworthiness. 

```mermaid
sequenceDiagram
    actor User
    participant LLM as AI Agent
    participant GATE as HMCP Gateway
    participant GF as Guardrails Framework
    participant Actions as NeMo Guardrails Actions
    participant Validator as MedicalJournalValidator
    participant VectorDB as Vector DB (Chroma)

    %% Initialization
    rect rgb(240, 240, 240)
        Note over Validator, VectorDB: Initialization
        Validator->>Validator: _initialize_vector_db()
        Validator->>VectorDB: Load or create vector database with medical journal data
    end

    %% Agent Registration
    rect rgb(240, 240, 240)
        Note over LLM, GATE: Agent Registration
        LLM->>GATE: Register Agent and <br>configure guardrails
        Note right of GATE: Extract statements using regex patterns and medical keywords  
        LLM->>LLM: Generate initial response
    end

    %% User Interaction
    rect rgb(240, 240, 240)
        Note over User, LLM: User Interaction
        User->>LLM: Ask medical question
        LLM->>LLM: Generate initial response
    end

    %% Validation Process
    rect rgb(240, 240, 240)
        Note over LLM, VectorDB: Validation Process
        LLM->>GF: Pass initial response
        GF->>Actions: validate_llm_response(response)
        Actions->>Actions: extract_medical_statements(response)
        Note right of Actions: Extract statements using regex patterns and medical keywords

        loop For each medical statement
            Actions->>Actions: validate_medical_statement(statement)
            Actions->>Validator: validate_fact(statement)
            Validator->>VectorDB: similarity_search_with_score(statement)
            VectorDB-->>Validator: Return similar journal entries with scores
            Validator->>Validator: Compare similarity to threshold
            Validator-->>Actions: Return validation result and source info
        end

        Actions->>Actions: Compile validation results
        Actions-->>GF: Return validation results
    end

    %% Response Generation
    rect rgb(240, 240, 240)
        Note over GF, User: Response Generation
        GF->>Actions: generate_validated_response(original_response, validation_results)
        
        alt All statements validated
            Actions->>Actions: Add citations to validated statements
        else Some statements invalid
            Actions->>Actions: Create response with valid statements and warnings
        else No valid statements
            Actions->>Actions: Create complete correction message
        end
        
        Actions-->>GF: Return validated response
        GF-->>LLM: Apply validated response
        LLM-->>User: Deliver validated response with citations or corrections
    end
```

