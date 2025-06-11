from fastapi import APIRouter, Request

from rxext.webhook_handlers import StripeWebhookHandler
from saasrx.config import app_config

router = APIRouter()

# Use centralized webhook configuration
stripe_handler = StripeWebhookHandler(app_config.webhook)

@router.post("/webhook/stripe")
async def webhook_stripe(request: Request):
    """Handle incoming Stripe webhook events."""
    return await stripe_handler.process_webhook(request)