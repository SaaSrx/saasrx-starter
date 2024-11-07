import reflex as rx

from saas.components import features, navbar


def pricing() -> rx.Component:
    return rx.box(rx.text("Pricing Section"), id="pricing")


def testimonials() -> rx.Component:
    return rx.box(rx.text("Testimonials Section"), id="testimonials")


def get_started() -> rx.Component:
    return rx.box(rx.text("Get Started Section"), id="get-started")


def index() -> rx.Component:
    """The index page"""
    return rx.box(
        navbar.navbar(),
        features.features(),
        rx.flex(
            # features.included_card(),
            # features.included_card(),
            spacing="5",
            justify="center",
        ),
    )
