import reflex as rx

from saas.app_config import config
from saas.components import card
from saas.state import AuthState


def verify_request_success() -> rx.Component:
    return rx.box(
        rx.cond(
            AuthState.user,
            rx.text(f"Success, logged in for user: {AuthState.user.email}"),
            rx.text("No user logged in"),
        )
    )


def verify_request_emailed() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.box(
                    rx.heading(config.formatted_application_name, align="center", size="8"),
                    rx.heading("Check your email", class_name="text-center"),
                    card.homepage_card(button_text="A sign in link has been sent to your email address."),
                    class_name="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg",
                ),
            ),
            class_name="min-h-screen bg-gradient-to-b from-indigo-50 to-white flex items-center justify-center px-4",
        ),
    )
