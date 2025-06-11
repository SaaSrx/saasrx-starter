"""Main configuration for SaaSRX application."""

from pathlib import Path

from rxext.config import APIConfig, AppConfig, ImageAssets, WebhookConfig

# Application info
APP_NAME = "saasrx"
FORMATTED_APP_NAME = "SaaSRX"
VERSION = "0.1.0"

# Asset configuration
image_assets = ImageAssets(
    favicon="/favicon.ico",
    app_icon="/saasrx-icon.png",
)

# API configuration
api_config = APIConfig(
    title=f"{FORMATTED_APP_NAME} API",
    version=VERSION,
    description="SaaS Starter API built with Reflex and FastAPI",
    route_paths=[str(Path(__file__).parent / "api" / "api_routes")],
    prefix="/api",
    add_default_health=True,
    include_client_info=True,
    include_environment_info=True,
)

# Webhook configuration
webhook_config = WebhookConfig(
    stripe_verify_signature=False,  # Set to True in production with real secret
    log_unhandled_events=True,
)

# Main app configuration
app_config = AppConfig(
    app_name=APP_NAME,
    formatted_app_name=FORMATTED_APP_NAME,
    api=api_config,
    webhook=webhook_config,
    assets=image_assets,
)