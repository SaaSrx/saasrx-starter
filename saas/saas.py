import reflex as rx

from saas.api import api
from saas.pages import index
from saas.rxext.app import App

webhooks = api.webhooks


class Customer(rx.Model, table=True):  # type: ignore
    """The customer model."""

    customer_name: str
    email: str
    age: int
    gender: str
    location: str
    job: str
    salary: int


tailwind_config = {
    "theme": {
        "extend": {},
    },
    "plugins": [
        "@tailwindcss/typography",
        "@tailwindcss/components",
        "@tailwindcss/base",
        "@tailwindcss/utilities",
    ],
}

app = App(
    # admin_dash=rx.AdminDash(models=[Customer]),
    # tailwind=tailwind_config,
)


# setup_api_routes(app.api)
# add web pages here:
app.add_page(component=index, route="/")
# app.add_page(create_document, route="/docs")


app.api.add_api_route("/health", api.api_health, methods=["GET"])
app.api.add_api_route("/webhook/stripe", api.webhooks.stripe, methods=["POST"])
