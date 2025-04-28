# HMCP-Example

Healthcare MCP example

### Feature
- Bidirectional communication
- Authentication and Authorization
- Guardrails


### How to run the demo

```bash

# Temporary steps till the package isn't published:
pip install hatch
hatch build

# Actual steps:
cd examples

# Install required dependencies using below command
pip install -r requirements.txt


# create .env by taking reference from .env.example
# and define below ENV variables 
OPENAI_API_KEY=<your-openai-api-key>  # provide your openai api key here, used by guardrails

# START EMR MCP server
# Open a new terminal and execute below commands
python hmcp_demo.py --emr-server

# START PATIENT data MCP server
# Open a new terminal and execute below commands
python hmcp_demo.py --patient-data-server


# Run the DEMO using client server with SSE transport (recommended)
# Open a new terminal and execute below commands
python hmcp_demo.py

```

HMCP Demo Workflow Steps
=======================

This document outlines the steps performed in the hmcp_demo.py clinical data workflow demonstration.

Overview
--------
The demo involves three agents working together:
1. AI Agent (Main Orchestrator)
2. EMR Writeback Agent
3. Patient Data Access Agent

Detailed Workflow Steps
----------------------

1. Initial Setup
   - AI Agent initializes authentication components
   - Generates JWT token for secure communication
   - Sets up OAuth client with test credentials

2. EMR Writeback Agent Connection
   - AI Agent connects to EMR Writeback Agent
   - Establishes SSE (Server-Sent Events) connection
   - Initializes EMR session

3. First Clinical Data Submission
   - AI Agent sends initial clinical data to EMR Writeback Agent
   - Data includes diagnosis, blood pressure, and medication information
   - Format: {"diagnosis": "Hypertension", "blood_pressure": "140/90", "medication": "Lisinopril 10mg"}

4. Guardrail Testing
   - AI Agent tests the guardrail functionality
   - Sends a test message to verify security measures
   - Verifies proper response handling

5. Patient Data Access
   - EMR Writeback Agent requests additional information (patient ID)
   - AI Agent connects to Patient Data Access Agent
   - Requests patient identifier for "John Smith"
   - Receives patient ID (PT12345)

6. Final EMR Update
   - AI Agent sends complete data to EMR Writeback Agent
   - Includes both clinical data and patient ID
   - Receives confirmation of successful EMR update

7. Workflow Completion
   - All required information is processed
   - EMR system is updated successfully
   - Demo workflow is completed

Note: The demo includes error handling and logging at each step to ensure proper execution and debugging capabilities. 