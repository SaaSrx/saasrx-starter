import reflex as rx

import saas.api as api
from rxconfig import config
from saas.pages import index
from saas.rxext.app import App
from saas.state.state import CheckoutState, IndexState, MenuState, State

# webhooks = api.webhooks

app = App(
    # admin_dash=rx.AdminDash(models=[Customer]),
    # tailwind=tailwind_config,
)


# app.api.add_api_route("/health", api.api_health, methods=["GET"])
# setup_api_routes(app.api)
# add web pages here:
# app.add_page(component=index_, route="/")
app.add_page(component=index, route="/")
# app.add_page(create_document, route="/docs")

app.api.add_api_route("/health", api.api_health, methods=["GET"])
# app.api.add_api_route("/webhook/stripe", api.webhooks.stripe, methods=["POST"])
