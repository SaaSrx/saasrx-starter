from fastapi import APIRouter

from .health import health_router
from .webhooks import webhooks_router

# Main API router for the application
# All other routers will be included here
api_router_v1 = APIRouter(prefix="/api/v1")

# Include individual routers
api_router_v1.include_router(health_router, tags=["Health"])
api_router_v1.include_router(webhooks_router, tags=["Webhooks"])

# You can add more routers here as the application grows
# Example:
# from .users import users_router
# api_router_v1.include_router(users_router, prefix="/users", tags=["Users"])
