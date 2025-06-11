"""API bootstrap for SaaSRX application."""

from rxext.api_bootstrap import create_api_app
from saasrx.config import app_config

# Create the FastAPI app using centralized config
api_app = create_api_app(app_config.api)
# api_app.add_api_route("/health", api_health, methods=["GET"])
