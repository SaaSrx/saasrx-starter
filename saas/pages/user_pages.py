import reflex as rx

from saas.components import admin_components, auth_components, signin_components
from saas.components.admin_components import cancel_redirect
from saas.state import AuthState


def verify_request_page() -> rx.Component:
    return rx.box(
        rx.cond(
            AuthState.is_hydrated,
            rx.box(
                cancel_redirect(),
                rx.cond(
                    AuthState.token_is_valid,
                    auth_components.verify_request_success(),
                    auth_components.verify_request_emailed(),
                ),
            ),
        ),
    )


def already_logged_in() -> rx.Component:
    return rx.box(
        rx.text(
            f"You are already logged in as: `{AuthState.session_token}`",
            class_name="mt-6 font-extrabold text-indigo-800",
        ),
        class_name="shadow-lg p-4 rounded",
    )


def signin_page() -> rx.Component:
    return rx.box(
        signin_components.redirect_to_purchase_alert_dialog(),
        rx.box(
            rx.flex(
                rx.box(
                    rx.cond(AuthState.valid_session, already_logged_in()),
                    signin_components.signin_hero(),
                    signin_components.email_signin_form(),
                    signin_components.signup_text(),
                    class_name="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg",
                ),
            ),
            class_name="min-h-screen bg-gradient-to-b from-indigo-50 to-white flex items-center justify-center px-4",
        ),
    )


def auth_verify_page() -> rx.Component:
    return rx.heading("User Authed")


def dashboard_page() -> rx.Component:
    return rx.box(
        rx.heading("Dashboard"),
        rx.text("Welcome to the dashboard!"),
    )
