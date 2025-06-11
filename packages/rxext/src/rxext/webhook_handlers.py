"""Webhook handler system for various services."""

from typing import Any, Callable, Dict

from fastapi import HTTPException, Request

from .config import WebhookConfig
from .console import console
from .utils.stripe_util import verify_webhook_signature


class WebhookHandlerRegistry:
    """Registry for webhook event handlers."""
    
    def __init__(self, config: WebhookConfig):
        self.config = config
        self._handlers: Dict[str, Callable] = {}
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Set up default event handlers."""
        self._handlers["default"] = self._handle_default_event
    
    def register_handler(self, event_type: str, handler: Callable):
        """Register a handler for a specific event type."""
        self._handlers[event_type] = handler
    
    def get_handler(self, event_type: str) -> Callable:
        """Get handler for event type, falling back to default."""
        return self._handlers.get(event_type, self._handlers["default"])
    
    async def _handle_default_event(self, data_object: dict) -> dict:
        """Handle unregistered event types."""
        if self.config.log_unhandled_events:
            console.warn(f"Unhandled event type with data: {data_object}")
        return self.config.default_response


class StripeWebhookHandler(WebhookHandlerRegistry):
    """Specialized webhook handler for Stripe events."""
    
    def _setup_default_handlers(self):
        """Set up Stripe-specific default handlers."""
        super()._setup_default_handlers()
        
        # Register default Stripe event handlers
        self._handlers.update({
            "payment_intent.succeeded": self._handle_payment_intent_succeeded,
            "payment_method.attached": self._handle_payment_method_attached,
            "checkout.session.completed": self._handle_checkout_session_completed,
        })
    
    async def process_webhook(self, request: Request) -> dict:
        """Process incoming Stripe webhook request."""
        try:
            # Get raw body for signature verification
            payload = await request.body()
            headers = dict(request.headers)
            
            # Verify webhook signature if configured
            if self.config.stripe_verify_signature:
                event = verify_webhook_signature(
                    payload, headers, self.config.stripe_webhook_secret
                )
            else:
                # Parse JSON directly if not verifying signature
                import json
                event = json.loads(payload)
            
            console.log(f"Processing Stripe webhook event: {event.get('type')}")
            
            # Get and execute event handler
            event_type = event.get("type", "unknown")
            handler = self.get_handler(event_type)
            result = await handler(event.get("data", {}).get("object", {}))
            
            return {"success": True, "event": result}
            
        except HTTPException:
            # Re-raise HTTP exceptions (like signature verification failures)
            raise
        except Exception as e:
            console.error(f"Error processing Stripe webhook: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    async def _handle_payment_intent_succeeded(self, data_object: dict) -> dict:
        """Handle payment intent succeeded event."""
        console.log(f"PaymentIntent succeeded: {data_object.get('id')}")
        # Add custom logic here
        return {"processed": "payment_intent.succeeded"}
    
    async def _handle_payment_method_attached(self, data_object: dict) -> dict:
        """Handle payment method attached event."""
        console.log(f"PaymentMethod attached: {data_object.get('id')}")
        # Add custom logic here
        return {"processed": "payment_method.attached"}
    
    async def _handle_checkout_session_completed(self, data_object: dict) -> dict:
        """Handle checkout session completed event."""
        console.log(f"Checkout session completed: {data_object.get('id')}")
        # Add custom logic here
        return {"processed": "checkout.session.completed"}