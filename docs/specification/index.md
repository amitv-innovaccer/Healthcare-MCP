## Architecture Components

### Diagram

```mermaid
---
title: Building AI Agents with Healthcare MCP Protocol and Server
---
graph TB
    subgraph 3rd party AI Agent
        AIA[AI Agent]
        subgraph CLISDK[Health MCP Client SDK]
            CE1[MCP Client]
        end
        AIA <--> CLISDK
    end

    subgraph Innovaccer AI Cloud

        subgraph DevTools
            AIAB[AI Agent Builder]
            DEVGB[Guardrails Builder]
            DEVRAG[RAG Data Store Builder]
        end
        

        subgraph CORE[MCP Core]
            Auth
            Logging
            Audit
            Guardrails
        end

        subgraph Innovaccer MCP Server
            subgraph GATE[MCP Gateway]
            end

            EP2[MCP Endpoint]
            RE2[Voice Agent System]
            %%RE2@{ shape: fr-rect }
            EP2 <--> RE2

            EP1[MCP Endpoint]
            RE1[(Patient Data Store)]
            EP1 <--> RE1

            EP3[MCP Endpoint]
            RE3[EHR Writeback]
            %%RE3@{ shape: fr-rect }
            EP3 <--> RE3

            EP4[MCP Endpoint]
            RE4[EHR Read Agent]
            %%RE4@{ shape: fr-rect }
            EP4 <--> RE4

            EP5[MCP Endpoint]
            RE5[EMPI]
            %%RE5@{ shape: fr-rect }
            EP5 <--> RE5

            EP6[MCP Endpoint]
            EP7[MCP Endpoint]

            EP8[MCP Endpoint]
            RE8[(RAG/Vector<br>Data Store)]
            EP8 <--> RE8
        end

        subgraph MS[Model Store]
            FLLM[Foundational LLM]
            SLM
            CM[Custom Models]
        end
    end

    subgraph 3rd party cloud
        3P1[(Data Store)]
        3P2[Clinical Algorithm]
        %%3P2@{ shape: fr-rect }
    end

    AIA <--> MS
    CLISDK <--> GATE
    GATE <--> |Auth, Logging, Audit, Guardrails <br> **Health MCP Protocol**| CORE
    GATE <--> |Identify patient and call context|EP2
    GATE <--> |Get Patient Details| EP1
    GATE <--> |Read from EHR| EP4
    GATE <--> |Write to EHR| EP3
    GATE <--> |Get EMPI ID| EP5
    GATE <--> |Get data from 3rd party server| EP6
    GATE <--> |Get results from 3rd party <br>clinical algorithm| EP7
    GATE <--> EP8
    EP6 <--> 3P1
    EP7 <--> 3P2
```

### Agent Card
- Each server side agent can define the agent card for clients to discover their configurations: (confirm this with MCP and A2A protocols)
    ```
    {
        name: Agent_Name,
        id: Unique Id for this deployment,
        Auth_Method : OAuth 2.0 or mTLS,
        Auth_Endpoint: Auth server URL,
        Capabilities: {
            Tools,
            List,
            Sampling,
            ...
        },
        Guardrails: {
            PHI_Redact,
            ...
        }
        Audit : Yes,

    }
    ```

### Other Features
- Allow to register agents and define capabilities
- Allow to define new guardrails
- Server will provide some default guardrails
- Server will provide access to Foundational/Custom LLM's & SLM's
- Allow to define authentication methods and provide certificate management for mTLS auth

## HMCP Protocol In-Depth

The aspects which we need to take care of are:
- Authentication & Authorization
    - Auth can be OAuth 2.0 or mTLS
- Guardrails
    - Define few example guardrails
- Logging/Auditing
- Agent Discovery
- Foundational LLM's discoverability
- Capabilities
- Registration of 3rd party agents
- Certificate management

### Authentication & Scopes
We will use OAuth 2.0 protocol when authentication is needed where end user token is needed. [OAuth Flow](./auth.md)

If service to service communication is needed then we will use mTLS.

### Guardrails

For guardrails we will use the Nvidia Nemo Guardrails library. Guardrails need to be defined 

Example [Validate LLM output against journals](./guardrails.md)

### Discoverability

### Patient Context

[Details](./context.md)
