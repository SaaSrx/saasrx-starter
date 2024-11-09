from fastapi import APIRouter

from saas.api import basic_routes, webhooks

"""
This module defines API basic routes for a FastAPI application, including health checks and Stripe webhooks.

Functions:
api_health(req: Request) -> dict:
    Handles health check requests and returns the status of the API.



"""

api_router = APIRouter()

api_router.add_api_route("/health", basic_routes.api_health, methods=["GET"])
api_router.add_api_route("/webhook/stripe", webhooks.stripe, methods=["POST"])
