# Configure logging
import logging
import os

from hmcp.auth import AuthConfig, OAuthServer, jwt_handler


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize auth components
auth_config = AuthConfig()
oauth_server = OAuthServer(auth_config)
jwt_handler = jwt_handler.JWTHandler(auth_config)
# Register a test client (in production, this would be done through a proper registration process)
client_id = os.getenv("CLIENT_ID", "test-client")
client_secret = os.getenv("CLIENT_SECRET", "test-secret")
logger.info(f"Registering test client {client_id} with secret {client_secret}")
oauth_server.register_client(client_id, client_secret)
logger.info("Test client registered successfully")