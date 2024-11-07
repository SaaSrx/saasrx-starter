import reflex as rx

from saas.components import signin_components


def signin_page() -> rx.Component:
    return rx.box(
        signin_components.redirect_alert_dialog(),
        rx.box(
            rx.flex(
                rx.box(
                    signin_components.signin_hero(),
                    signin_components.email_signin_form(),
                    signin_components.signup_text(),
                    class_name="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg",
                    # class_name="max-w-md space-y-8 bg-white p-8 rounded-xl shadow-lg",
                ),
            ),
            class_name="min-h-screen bg-gradient-to-b from-indigo-50 to-white flex items-center justify-center px-4",
        ),
    )


def success_page() -> rx.Component:
    return signin_components.payment_success()


def dashboard_page() -> rx.Component:
    return rx.box(
        rx.heading("Dashboard"),
        rx.text("Welcome to the dashboard!"),
    )
