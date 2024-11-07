import stripe
from fastapi import HTTPException, Request

from saas.rxext import console
from saas.saas_secrets import secrets

webhook_secret = secrets.stripe_webhook_secret


def verify_webhook_signature(payload: dict, headers: dict) -> dict:
    """Verify the Stripe webhook signature.

    Args:
        req (Request): The incoming request from Stripe.

    Returns:
        dict: The event data if verification is successful.

    Raises:
        HTTPException: If signature verification fails.
    """
    # payload = await req.body()
    # sig_header = req.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=headers["stripe-signature"],
            secret=webhook_secret,
        )
        return event
    except stripe.error.SignatureVerificationError as e:
        console.error(f"⚠️  Webhook signature verification failed: {e}\n{payload=}")
        raise HTTPException(
            status_code=400,
            detail="Webhook signature verification failed",
        )


def handle_event(event: dict) -> None:
    """Handle different types of Stripe events.

    Args:
        event (dict): The event data from Stripe.
    """
    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "payment_intent.succeeded":
        console.log(f"PaymentIntent Success: {data_object=}")
        # Add your custom logic here
    elif event_type == "payment_method.attached":
        console.log(f"PaymentMethod Success: {data_object=}")
        # handle_payment_method_attached(data_object)
    else:
        console.warn(f"Unhandled event type: {event_type}")


async def process_webhook(req: Request) -> dict:
    """Process the incoming Stripe webhook request.

    Args:
        req (Request): The incoming request from Stripe.

    Returns:
        dict: A success message.
    """
    event = await verify_webhook_signature(req)
    handle_event(event)
    return {"success": True}
