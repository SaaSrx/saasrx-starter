import stripe
from fastapi import HTTPException, Request

from saas.app_secret import secrets
from saas.rxext import console

webhook_secret: str = secrets["stripe_webhook_secret"]


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
        console.log(f"verify for \n{payload=}\nand\n{headers=}")
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=headers["stripe-signature"],
            secret=webhook_secret,
        )
        return event
    except stripe.error.SignatureVerificationError as e:
        console.error(f"⚠️ Webhook signature verification failed: {e}\n{payload=}")
        raise HTTPException(
            status_code=400,
            detail="Webhook signature verification failed",
        )


async def handle_event(event: dict) -> None:
    """Handle different types of Stripe events.

    Args:
        event (dict): The event data from Stripe.
    """
    event_type = event["type"]
    data_object = event["data"]["object"]

    # TODO: turn this into dict/case match with event callback
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
    event_resp = await handle_event(event)
    return {"success": True}


def get_payments(pay_id: str) -> list:
    """
    Retrieve all payments from Stripe for the given pay_id.

    Args:
        pay_id (str): The payment identifier to filter payments.

    Returns:
        list: A list of payment objects associated with the pay_id.

    Raises:
        HTTPException: If an error occurs while fetching payments.
    """
    try:
        payments = stripe.PaymentIntent.list(metadata={"pay_id": pay_id})
        return payments.data
    except stripe.error.StripeError as e:
        console.error(f"Error fetching payments for pay_id {pay_id}: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve payments from Stripe.")
