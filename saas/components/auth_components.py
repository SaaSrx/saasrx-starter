import reflex as rx

from saas.app_config import config
from saas.components import card
from saas.state import AuthState, State


def fake_user_button() -> rx.Component:
    return rx.box(
        rx.button("Fake User", class_name="btn btn-primary", on_click=State.gen_fake_user),
        class_name="flex justify-center",
    )


def fake_gen_button() -> rx.Component:
    return rx.box(
        rx.button("Check", class_name="btn btn-primary", on_click=State.get_fake_auth),
        class_name="flex justify-center",
    )


def verify_request_success() -> rx.Component:
    return rx.box(f"Success, logged in for user: {AuthState.user_email}")


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
