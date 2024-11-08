import reflex as rx
from fastapi import Request

# import .webhooks as webhooks
# import saas.api.webhooks as webhooks
from saas.rxext import console

"""
This module defines API routes for a FastAPI application, including health checks and Stripe webhooks.

Functions:
api_health(req: Request) -> dict:
    Handles health check requests and returns the status of the API.

api_webhook(req: Request) -> dict:
    Handles incoming webhook data from Stripe, verifies the signature, and processes events.

setup_api_routes(app: APIRouter):
    Sets up API routes for the given FastAPI router by iterating over the ROUTES dictionary and adding each route-handler pair to the provided APIRouter instance.

Constants:
ROUTES (dict): A dictionary mapping route paths to their corresponding handler functions and options.
"""


# Allows for either decorator or manual route addition, e.g.:
# @api("/health", methods=["GET"])
# or just add to the API_ROUTES list
async def api_health(req: Request):
    if not rx.utils.is_prod_mode():
        console.log(f"Not in production mode.")

    console.log(f"Got health check: {req=}")
    return {"status": "okay", "message": "retrieved health check"}


# API_ROUTES = [
#     dict(path="/health", endpoint=api_health),
#     dict(path="/webhook/stripe", endpoint=webhooks.stripe),
# ]

# ALTERNATIVE WAY TO SETUP API ROUTES
# ROUTES = {
#     # PATH: (HANDLER, OPTIONAL[OPTIONS])
#     "/health": (api_health, {"methods": ["GET"]}),
#     "/webhook": (api_webhook, {"methods": ["POST"]}),
# }
