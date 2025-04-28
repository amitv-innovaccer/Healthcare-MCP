# Sharing Patient Context

HMCP implements patient context sharing based on SMART on FHIR specifications, ensuring healthcare AI agents maintain proper patient context isolation and security.

## Patient Context Methods

HMCP supports these patient context methods:

### 1. OAuth 2.0 Scope-Based Patient Context

During authorization, applications request patient-specific access:

```
GET /authorize?
  response_type=code&
  client_id=CLIENT_ID&
  redirect_uri=REDIRECT_URI&
  scope=patient/hmcp:read launch/patient&
  state=STATE
```

The authorization server's token response includes:

```json
{
  "access_token": "eyJhbGciOiJSUzI...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "patient/hmcp:read launch/patient",
  "patient": "123456",
  "encounter": "987654"
}
```

All API requests using this token automatically restrict operations to the specified patient.

### 2. JWT Claims for Patient Context

When using JWT access tokens, patient context is embedded as claims:

```json
{
  "iss": "https://authorization-server.example.com",
  "sub": "client_id",
  "exp": 1656086400,
  "iat": 1656082800,
  "scope": "patient/hmcp:read",
  "patient": "123456",
  "encounter": "987654"
}
```

The server extracts and enforces the patient context without requiring additional parameters in each API call.

### 3. HTTP Headers (For backwards compatibility)

For compatibility with systems that don't fully implement SMART on FHIR:

```
GET /api/resource
Authorization: Bearer ACCESS_TOKEN
X-HMCP-Patient: 123456
```

This method is less secure and recommended only for transition scenarios.

## Context Synchronization

HMCP provides mechanisms to ensure consistent patient context across multiple agents or services:

1. **Context propagation**: When an HMCP server forwards requests to other services, patient context is preserved
2. **Context validation**: Servers validate that patient context matches across related operations
3. **Patient switching**: Clear protocols for changing patient context within a session

## Implementation Guidelines

1. Always include patient context in OAuth 2.0 tokens when possible
2. Validate patient context on every request that accesses patient data
3. Use a common patient identifier system across all services
4. Implement access controls to prevent improper cross-patient data access
5. Log all access with patient context for audit purposes

## Security Considerations

Patient context should be treated with the same security considerations as authentication. Implementation must:

1. Verify patient context claims in tokens
2. Ensure tokens are properly validated and not expired
3. Use secure channels (TLS) for all communications
4. Prevent elevation of privilege through patient context manipulation
5. Audit all patient context changes

By combining scope-based authorization with per-request patient context in tokens, HMCP provides a robust, secure mechanism for patient data isolation and appropriate access control.