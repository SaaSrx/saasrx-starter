import stripe
from fastapi import HTTPException, Request

from rxext import console  # type: ignore[import-not-found]


class StripeUtil:
    def __init__(self, webhook_secret: str):
        self.webhook_secret = webhook_secret


def get_stripe_payment_link(email: str | None = None):
    # TODO: inject actual stripe_web_url via config or env
    stripe_web_url = "https://stripe.com/pay"  # placeholder
    return f"{stripe_web_url}?prefilled_email={email}"


def verify_webhook_signature(payload: bytes | dict, headers: dict, webhook_secret: str | None = None) -> dict:
    """Verify the Stripe webhook signature and return the parsed event."""
    if webhook_secret is None:
        # TODO: Get from config or environment
        webhook_secret = "your_webhook_secret_here"
    
    try:
        console.log(f"verify for \n{payload=}\nand\n{headers=}")
        
        # Handle both bytes and dict payloads
        if isinstance(payload, dict):
            import json
            payload_bytes = json.dumps(payload).encode('utf-8')
        else:
            payload_bytes = payload
            
        event = stripe.Webhook.construct_event(
            payload=payload_bytes,
            sig_header=headers.get("stripe-signature", ""),
            secret=webhook_secret,
        )
        return event
    except stripe.error.SignatureVerificationError as e:
        console.error(f"⚠️ Webhook signature verification failed: {e}\n{payload=}")
        raise HTTPException(
            status_code=400, detail="Webhook signature verification failed"
        )


async def handle_event(event: dict) -> None:
    """Handle different types of Stripe events."""
    event_type = event["type"]
    data_object = event["data"]["object"]

    match event_type:
        case "payment_intent.succeeded":
            console.log(f"PaymentIntent Success: {data_object=}")
        case "payment_method.attached":
            console.log(f"PaymentMethod Success: {data_object=}")
        case _:
            console.warn(f"Unhandled event type: {event_type}")


async def process_webhook(req: Request) -> dict:
    """Process the incoming Stripe webhook request."""
    event = await verify_webhook_signature(req.body, req.headers)
    await handle_event(event)
    return {"success": True}


def get_payments(pay_id: str) -> list:
    """Retrieve all payments from Stripe for the given pay_id."""
    try:
        payments = stripe.PaymentIntent.list(metadata={"pay_id": pay_id})
        return payments.data  # type: ignore[attr-defined]
    except stripe.error.StripeError as e:
        console.error(f"Error fetching payments for pay_id {pay_id}: {e}")
        raise HTTPException(
            status_code=400, detail="Failed to retrieve payments from Stripe."
        )
