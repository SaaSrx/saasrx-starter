"""Unified configuration system for Reflex applications."""

from dataclasses import asdict, dataclass, field
from typing import Any

import reflex as rx


@dataclass
class DownloadInfo:
    """Information about a download."""
    filepath: str
    filename: str


@dataclass
class ImageAssets:
    """Information about image assets."""
    favicon: str
    app_icon: str


class Config(rx.Config):
    """Extended config class that adds app-specific functionality."""
    
    formatted_application_name: str

    @property
    def module(self) -> str:
        if hasattr(self, "module_path"):
            return self.module_path.replace("/", ".")
        return super().module

    @property
    def reload_dirs(self) -> list[str]:
        if hasattr(self, "reload_paths"):
            return self.reload_paths
        elif hasattr(self, "module_path"):
            return [self.module.split(".")[0]]
        else:
            return [self.app_name]


@dataclass
class APIConfig:
    """Configuration for FastAPI app creation and route loading."""
    
    # FastAPI constructor kwargs
    title: str = "API"
    version: str = "0.1.0"
    description: str | None = None
    docs_url: str | None = "/docs"
    openapi_url: str | None = "/openapi.json"
    redoc_url: str | None = "/redoc"
    
    # Route loading configuration
    route_paths: list[str] = field(default_factory=list)
    prefix: str = "/api"
    add_default_health: bool = True
    default_method: str = "GET"
    
    # Environment and logging
    include_client_info: bool = True
    include_environment_info: bool = True
    
    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        """Extract FastAPI constructor arguments from config."""
        fastapi_params = {
            "title", "version", "description", "docs_url", 
            "openapi_url", "redoc_url"
        }
        return {
            k: v for k, v in asdict(self).items()
            if k in fastapi_params and v is not None
        }


@dataclass
class WebhookConfig:
    """Configuration for webhook handlers."""
    
    # Stripe webhook settings
    stripe_webhook_secret: str | None = None
    stripe_verify_signature: bool = True
    
    # Event handler configuration
    log_unhandled_events: bool = True
    default_response: dict = field(default_factory=lambda: {"success": True})


@dataclass
class AppConfig:
    """Main application configuration that combines all config types."""
    
    # Basic app info
    app_name: str
    formatted_app_name: str
    
    # Sub-configurations
    api: APIConfig = field(default_factory=APIConfig)
    webhook: WebhookConfig = field(default_factory=WebhookConfig)
    
    # Assets and downloads
    assets: ImageAssets | None = None
    downloads: list[DownloadInfo] = field(default_factory=list)
    
    def __post_init__(self):
        """Set up default API title if not provided."""
        if self.api.title == "API":
            self.api.title = f"{self.formatted_app_name} API"