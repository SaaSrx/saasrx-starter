import reflex as rx

from saas.components import features, navbar


def pricing() -> rx.Component:
    return rx.box(rx.text("Pricing Section"), id="pricing")


def testimonials() -> rx.Component:
    return rx.box(rx.text("Testimonials Section"), id="testimonials")


def get_started() -> rx.Component:
    return rx.box(rx.text("Get Started Section"), id="get-started")


def index() -> rx.Component:
    """
    main index page.  can check status with
    secrets.status_mode
    """
    return rx.box(
        navbar.navbar(),
        features.features(),
        # rx.vstack(
        # rx.spacer(),
        #     rx.spacer(),
        #     pricing(),
        #     rx.spacer(),
        #     testimonials(),
        #     rx.spacer(),
        #     get_started(),
        # ),
        # class_name="min-h-screen bg-white",
    )
