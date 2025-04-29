# Chapter 7: JWT Handler

Welcome to the final chapter of our core concepts tutorial! In [Chapter 6: Auth Configuration](06_auth_configuration_.md), we learned about the "security rulebook" (`AuthConfig`) that holds all the vital settings for our server's security, like the secret key and allowed clients.

But just having a rulebook isn't enough. We need someone (or something!) to actually *use* those rules to create and check the security passes. How does the server reliably generate those secure JWT tokens we discussed in [Chapter 3: Authentication (OAuth & JWT)](03_authentication__oauth___jwt__.md)? And how does it verify that incoming tokens are legitimate and haven't been tampered with?

That's the job of the **JWT Handler**!

## What's the Big Idea? The Security Pass Printer & Scanner

Imagine our hospital security system again. We have the master plan ([Auth Configuration](06_auth_configuration_.md)) specifying who is allowed access, their passwords, and the design of the security passes.

Now, we need the specialized machine that actually:

1.  **Prints the Passes (Creates Tokens):** When an authorized application proves its identity, this machine takes the rules (secret key, expiry time) and the specific permissions for that application, and prints a secure, tamper-proof access pass (a JWT).
2.  **Scans the Passes (Verifies Tokens):** When someone tries to enter a secure area using their pass, this machine scans it. It checks if the pass was printed using the correct secret template (signature), if it hasn't expired, and if it's intended for use in this specific building (audience).

The **JWT Handler** is precisely this specialized machine within the HMCP project. It's a focused component whose *only job* is to correctly create (encode) and verify (decode) JSON Web Tokens (JWTs) based on the rules defined in the [Auth Configuration](06_auth_configuration_.md).

## What is the JWT Handler?

The `JWTHandler` is a class (found in `src/hmcp/auth/jwt_handler.py`) dedicated to handling the cryptographic operations involved with JWTs. It takes the configuration details provided by an `AuthConfig` object and uses them to perform two main functions:

1.  **`generate_token(...)`:** Creates a new JWT string. It packages up information like the client ID (`sub`), granted permissions (`scope`), issuer (`iss`), audience (`aud`), and expiry time (`exp`), and then digitally signs this package using the `JWT_SECRET_KEY` and `JWT_ALGORITHM` from the `AuthConfig`.
2.  **`verify_token(...)`:** Takes an incoming JWT string and checks its validity. It uses the same `JWT_SECRET_KEY` and `JWT_ALGORITHM` to verify the digital signature. It also checks if the token has passed its `exp` time and if the `aud` matches the server. If everything checks out, it returns the decoded information (the "payload") contained within the token.

By centralizing this logic, we ensure that tokens are always created and verified consistently and securely according to the defined configuration.

## How It's Used

Other parts of the server, like the authentication endpoint handler (`OAuthServer`) and the security middleware (`AuthMiddleware`), rely on the `JWTHandler`.

**1. Generating a Token (Example Usage):**

When a client successfully authenticates (as seen in [Chapter 3: Authentication (OAuth & JWT)](03_authentication__oauth___jwt__.md)), the server logic (e.g., `OAuthServer`) uses the `JWTHandler` to create the access token.

```python
# --- Assume we have these objects already ---
# auth_config: An instance of AuthConfig with all the rules
# jwt_handler: An instance of JWTHandler(auth_config)
# client_id_validated: The ID of the client that just logged in
# scopes_granted: The permissions approved for this client

print(f"Asking JWT Handler to create a token for {client_id_validated}...")

# Use the handler to generate the token string
access_token = jwt_handler.generate_token(
    client_id=client_id_validated,
    scope=" ".join(scopes_granted) # Scopes are usually space-separated
    # patient_id might be added here if needed
)

print(f"JWT Handler returned a token: {access_token[:20]}...")
# This 'access_token' string is then sent back to the client.
```

**Explanation:**

*   The server logic calls `jwt_handler.generate_token`.
*   It provides the necessary details like the `client_id` and the `scope`.
*   The `JWTHandler` uses the secret key and other settings from its `AuthConfig` internally to create and sign the JWT.
*   It returns the final, secure JWT string.

**2. Verifying a Token (Example Usage):**

When a client makes a request to a protected resource (like asking for [Sampling Functionality](04_sampling_functionality_.md)), the server's security middleware (`AuthMiddleware`, discussed in [Chapter 1: HMCP Server](01_hmcp_server_.md)) uses the `JWTHandler` to check the token sent by the client.

```python
# --- Assume we have these objects ---
# jwt_handler: An instance of JWTHandler(auth_config)
# incoming_token: The JWT string received from the client's Authorization header

print(f"Asking JWT Handler to verify token: {incoming_token[:20]}...")

try:
    # Use the handler to verify and decode the token
    payload = jwt_handler.verify_token(token=incoming_token)

    # If successful, 'payload' is a dictionary with the token data
    client_id = payload.get("sub")
    scopes = payload.get("scope")
    print(f"Token verified! Client: {client_id}, Scopes: {scopes}")
    # Now the middleware knows who the user is and can allow the request

except InvalidTokenError as e:
    # If verification fails (bad signature, expired, etc.)
    print(f"Token verification failed: {e}")
    # The middleware would reject the request (e.g., send a 401 error)
```

**Explanation:**

*   The middleware calls `jwt_handler.verify_token` with the token string from the request.
*   The `JWTHandler` uses the secret key and algorithm from its `AuthConfig` to check the signature. It also checks expiry and audience.
*   If the token is valid, it returns the decoded `payload` (a dictionary).
*   If the token is invalid for any reason, it raises an `InvalidTokenError`.

## How it Works Under the Hood: Creation and Verification

Let's trace the process when the `JWTHandler` is called.

**Token Creation (`generate_token`):**

1.  **Receive Request:** The `generate_token` method is called with `client_id`, `scope`, etc.
2.  **Get Config:** It accesses its stored `AuthConfig` object.
3.  **Prepare Payload:** It creates a dictionary (`payload`) containing standard JWT claims:
    *   `iss` (Issuer): From `auth_config.ISSUER`.
    *   `sub` (Subject): The provided `client_id`.
    *   `aud` (Audience): From `auth_config.JWT_AUDIENCE`.
    *   `iat` (Issued At): Current time.
    *   `exp` (Expiration Time): Current time + `auth_config.TOKEN_EXPIRY_HOURS`.
    *   `scope`: The provided `scope`.
    *   (Maybe `patient` if relevant).
4.  **Get Signing Details:** It retrieves the `auth_config.JWT_SECRET_KEY` and `auth_config.JWT_ALGORITHM`.
5.  **Encode & Sign:** It uses an underlying JWT library (like `PyJWT`) to encode the `payload` dictionary into a JSON string, then Base64 encode it, and finally create a digital signature using the secret key and algorithm. These parts (encoded header, encoded payload, signature) are joined by dots (`.`) to form the final JWT string.
6.  **Return Token:** It returns the complete JWT string.

**Token Verification (`verify_token`):**

1.  **Receive Request:** The `verify_token` method is called with the `token` string.
2.  **Get Config:** It accesses its stored `AuthConfig` object.
3.  **Get Verification Details:** It retrieves the `auth_config.JWT_SECRET_KEY`, `auth_config.JWT_ALGORITHM`, and `auth_config.JWT_AUDIENCE`.
4.  **Decode & Verify:** It uses the underlying JWT library to:
    *   Split the token string into its header, payload, and signature parts.
    *   Decode the header and payload.
    *   **Verify Signature:** Re-calculate the signature using the header, payload, and the `JWT_SECRET_KEY`, then compare it to the signature part of the token. If they don't match, raise an error (Invalid Signature).
    *   **Verify Expiry:** Check if the current time is before the `exp` time found in the payload. If expired, raise an error.
    *   **Verify Audience:** Check if the `aud` claim in the payload matches the expected `auth_config.JWT_AUDIENCE`. If not, raise an error.
    *   (Other checks like 'Issued At' (`iat`) or 'Not Before' (`nbf`) might also occur).
5.  **Return Payload:** If all checks pass, return the decoded `payload` dictionary. If any check fails, raise an `InvalidTokenError`.

**Sequence Diagram (Token Verification):**

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant Middleware as AuthMiddleware
    participant JWTH as JWT Handler
    participant AuthCfg as AuthConfig

    Client->>+Middleware: Request with JWT in Header
    Middleware->>Middleware: Extract token string
    Middleware->>+JWTH: verify_token(token)
    JWTH->>+AuthCfg: Get JWT_SECRET_KEY, ALGORITHM, AUDIENCE
    JWTH->>JWTH: Decode token, Check Signature (using Secret Key)
    JWTH->>JWTH: Check Expiry (using payload 'exp')
    JWTH->>JWTH: Check Audience (using payload 'aud' and AuthCfg)
    alt Token is Valid
        JWTH-->>-Middleware: Return decoded payload
        Middleware->>Middleware: Extract client_id, scopes from payload
        Middleware->>Client: Allow request to proceed / Send Response
    else Token is Invalid
        JWTH-->>-Middleware: Raise InvalidTokenError
        Middleware-->>-Client: Send Error Response (e.g., 401 Unauthorized)
    end

```

**Code Snippets (`src/hmcp/auth/jwt_handler.py` Simplified):**

*   **Class Structure:**

    ```python
    # Inside src/hmcp/auth/jwt_handler.py
    import jwt as pyjwt # Using the PyJWT library
    from datetime import datetime, timedelta
    from .config import AuthConfig
    from .exceptions import InvalidTokenError

    class JWTHandler:
        def __init__(self, config: AuthConfig):
            """Stores the security rulebook."""
            self.config = config
            # self.blacklisted_tokens = set() # For token revocation (optional)

        def generate_token(self, client_id: str, scope: str, ...) -> str:
            """Creates and signs a JWT."""
            # 1. Prepare payload dictionary using self.config
            payload = { ... } # Includes sub, exp, scope, iss, aud...
            payload['exp'] = datetime.utcnow() + timedelta(
                hours=self.config.TOKEN_EXPIRY_HOURS
            )

            # 2. Encode using PyJWT and settings from self.config
            token = pyjwt.encode(
                payload,
                self.config.JWT_SECRET_KEY,
                algorithm=self.config.JWT_ALGORITHM
            )
            return token

        def verify_token(self, token: str) -> dict:
            """Verifies a JWT's signature, expiry, audience and returns payload."""
            try:
                # 1. Decode using PyJWT and settings from self.config
                #    This automatically checks signature, expiry, audience
                payload = pyjwt.decode(
                    token,
                    self.config.JWT_SECRET_KEY,
                    algorithms=[self.config.JWT_ALGORITHM],
                    audience=self.config.JWT_AUDIENCE
                )
                # 2. Return payload if successful
                return payload
            except (pyjwt.ExpiredSignatureError, pyjwt.InvalidAudienceError,
                    pyjwt.InvalidTokenError) as e:
                # 3. Raise our specific error if PyJWT validation fails
                raise InvalidTokenError(f"JWT Verification Failed: {e}")
    ```

**Explanation:**

*   The `__init__` method stores the `AuthConfig` instance passed to it.
*   `generate_token` builds the `payload` dictionary using details from the arguments and `self.config`, then uses `pyjwt.encode` with the secret key and algorithm from `self.config`.
*   `verify_token` uses `pyjwt.decode`, passing the token string and the verification parameters (secret key, algorithms, audience) directly from `self.config`. The `pyjwt` library handles the complex signature, expiry, and audience checks internally. If any check fails, it raises an exception, which we catch and re-raise as our specific `InvalidTokenError`.

## Conclusion

You've reached the end of our core concepts tour! In this chapter, we focused on the **JWT Handler**. You learned it's the specialized component responsible for the critical tasks of **creating (encoding)** and **verifying (decoding)** JSON Web Tokens. Acting like a dedicated security pass printer and scanner, it uses the rules (secret key, algorithm, expiry, audience) defined in the [Auth Configuration](06_auth_configuration_.md) to ensure tokens are generated securely and validated correctly. Components like the `OAuthServer` and `AuthMiddleware` rely on the `JWTHandler` to manage the lifecycle of these important security tokens.

Understanding these seven core components – the [HMCP Server](01_hmcp_server_.md), [HMCP Client](02_hmcp_client_.md), the overall [Authentication (OAuth & JWT)](03_authentication__oauth___jwt__.md) flow, the unique [Sampling Functionality](04_sampling_functionality_.md), the safety net of [Guardrails](05_guardrails_.md), the security rulebook in [Auth Configuration](06_auth_configuration_.md), and the token engine of the [JWT Handler](07_jwt_handler_.md) – gives you a solid foundation for working with the Healthcare-MCP project. Happy coding!

