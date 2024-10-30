from fastapi import Request

from rxconfig import secrets
from saas.rxext import console

# import .webhooks as webhooks
from . import webhooks

# stripe_util.stripe.api_key = secrets.stripe_secret_key
webhook_secret = secrets.stripe_webhook_secret

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
    console.log(f"Got health check: {req=}")
    return {"status": "ok"}


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


# def setup_api_routes(app: APIRouter, routes: dict = ROUTES):
#     """
#     Sets up API routes for the given FastAPI router.

#     This function iterates over the ROUTES dictionary and adds each route-handler
#     pair to the provided APIRouter instance.

#     Args:
#         app (APIRouter): The FastAPI router instance to which the routes will be added.
#     """
#     for route, fn in routes.items():
#         fn, opts = (fn, {}) if callable(fn) else fn
#         app.add_api_route(route, fn, **opts)
