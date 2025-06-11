from fastapi import APIRouter, Request, HTTPException

webhooks_router = APIRouter()


@webhooks_router.post("/webhook/stripe")
async def webhook_stripe(req: Request):
    # Placeholder for Stripe webhook logic
    # payload = await req.body()
    # sig_header = req.headers.get('stripe-signature')
    # event = None

    # try:
    #     # Use stripe_util.verify_webhook_signature from your old rxext.utils
    #     # event = stripe.Webhook.construct_event(
    #     #     payload, sig_header, stripe_webhook_secret
    #     # )
    #     print("Stripe webhook received (not yet verified or processed)")
    # except ValueError as e:
    #     # Invalid payload
    #     raise HTTPException(status_code=400, detail=str(e))
    # except stripe.error.SignatureVerificationError as e:
    #     # Invalid signature
    #     raise HTTPException(status_code=400, detail=str(e))

    # Handle the event
    # if event['type'] == 'checkout.session.completed':
    #   session = event['data']['object']
    #   # Fulfill the purchase...
    # else:
    #   print('Unhandled event type {}'.format(event['type']))

    return {"status": "success", "message": "Stripe webhook received (placeholder)"}
