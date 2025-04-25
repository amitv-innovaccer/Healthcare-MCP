# HMCP Specification

Healthcare Model Context Protocol (HMCP) expands on base [MCP](https://modelcontextprotocol.io/specification/2025-03-26) by adding the below enhancements:
- [Authentication, Authorization & Scopes](#authentication--scopes)
    - Auth can be OAuth 2.0 or mTLS
- [Patient Context](#patient-context)
- [Guardrails](#guardrails)
    - Define few example guardrails
- Logging/Auditing
- [Bidirectional agent to agent communication](#bi-directional-agent-to-agent-communication)

## Architecture Components

### Diagram

```mermaid
---
Title: Health MCP in action
---
graph LR
    subgraph HS[Health System]
        subgraph AIA[AI Agent]
        end
    end

    subgraph HMCP Server
        subgraph GATE[HMCP Gateway]
        end
        subgraph IMA[Agents]
        end
        AIA <--> |HMCP| GATE
        GATE <--> |HMCP| IMA
    end

    subgraph 3PP[3rd party platform]
        subgraph 3PDS[Data store]
        end
        subgraph 3PALGO[Clinical Algorithm]
        end
        GATE <--> |HMCP|3PDS
        GATE <--> |HMCP|3PALGO
    end
```

### Authentication & Scopes
We will use OAuth 2.0 protocol when authentication is needed where end user token is needed. [OAuth Flow](./auth.md)

If service to service communication is needed then we will use mTLS.

### Guardrails

For guardrails we will use the Nvidia Nemo Guardrails library. Guardrails need to be defined 

Example [Validate LLM output against journals](./guardrails.md)

### Patient Context

[Details](./context.md)

### Bi-directional agent to agent communication

[Sampling](./sampling.md)

### TODO:

- Add JSON specification
- Add ability to define guardrails in specification/ or in experimental capabilities
- Publish agent card
- Add capability negotiation in client for sampling
- Added section on bi-directional agent communication
- Add a sequence diagram showing the complete flow with auth and guardrails