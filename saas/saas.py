import reflex as rx

import saas.api as api
from saas.pages import index, signin_page
from saas.rxext.app import App, make_admin_dash

app = App(
    theme=rx.theme(appearance="light", radius="large", accent_color="iris"),
    admin_dash=make_admin_dash(),
)


# add web pages here:
app.add_page(component=index, route="/")
app.add_page(component=signin_page, route="/signin")
# app.add_page(create_document, route="/docs")

app.api.add_api_route("/health", api.api_health, methods=["GET"])
# app.api.add_api_route("/webhook/stripe", api.webhooks.stripe, methods=["POST"])
