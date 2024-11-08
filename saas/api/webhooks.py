from fastapi import Request

from saas.rxext import console
from saas.rxext.endpoints import Endpoint
from saas.saas_secrets import secrets
from saas.rxext.utils import stripe_util

webhook_secret = secrets.stripe_webhook_secret


class WebhookHandler(Endpoint):
    route = "webhook"


# ---- STRIPE WEBHOOK HANDLER ----


async def _handle_default_event(data_object: dict):
    """Handle default event."""
    console.warn(f"Unhandled event type: {data_object=}")


async def _handle_payment_intent_succeeded(data_object: dict):
    """Handle payment intent succeeded event."""
    console.log(f"PaymentIntent Success: {data_object=}")
    # Add your custom logic here


async def _handle_payment_intent_attached(data_object: dict):
    """Handle payment method attached event."""
    console.log(f"PaymentMethod Success: {data_object=}")
    # Add your custom logic here


async def _handle_checkout_session_completed(data_object: dict):
    """Handle checkout session completed event."""
    console.log(f"Checkout Session Success: {data_object=}")
    # Add your custom logic here


_handlers = {
    # Add more handlers as needed
    "payment_intent.succeeded": _handle_payment_intent_succeeded,
    "payment_method.attached": _handle_payment_intent_attached,
    "checkout.session.completed": _handle_checkout_session_completed,
    "default": _handle_default_event,
}


async def stripe(req: Request) -> dict:
    """
    Handle incoming Stripe webhook events.

    This function processes the incoming request, verifies the webhook signature,
    and dispatches the event to the appropriate handler based on the event type.

    Args:
        req (Request): The incoming HTTP request containing the Stripe event payload.

    Returns:
        dict: A dictionary indicating the success of the operation and the response from the event handler.
    """
    data = await req.json()  # rather than await req.body()
    event = stripe_util.verify_webhook_signature(payload=data, headers=req.headers)

    # Handle the event
    event_handler = _handlers.get(event["type"], _handlers["default"])
    event_resp = await event_handler(event["data"]["object"])

    return {"success": True, "event": event_resp}


async def send_email(req: Request) -> dict:
    """Handle incoming email events."""
    console.log("Email event received")
    return {"success": True}
