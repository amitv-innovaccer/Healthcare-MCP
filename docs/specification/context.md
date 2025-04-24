# Sharing Patient Context

**Here are few patterns you can adopt—directly inspired by SMART on FHIR—to carry patient context in every request:**

### Negotiate context at launch via OAuth2 scopes

During your initial OAuth2/OpenID Connect handshake, have the client request both the patient‑scoped resource scopes (e.g. patient/*.rs) and the launch context scope launch/patient.  If granted, the authorization server will return an access token response that includes a top‑level "patient" parameter whose value is the Patient’s logical ID (e.g. "patient":"123").  The client then sends that same access token in an Authorization: Bearer <token> header on each call, and the server automatically restricts any patient‑level operations to Patient 123.

### Embed patient ID as a JWT claim

If your access tokens are JWTs, include the patient ID as a "patient" claim.  On each request you simply present the JWT; your backend parses the token, extracts the patient claim, and enforces it when processing the call  .


By combining a one‑time context negotiation (via scopes) with per‑call token, you get a robust, extensible mechanism—just as SMART on FHIR does—to ensure every request is scoped to the right patient.