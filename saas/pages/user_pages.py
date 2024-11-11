import reflex as rx

from saas.app_config import config, image_assets
from saas.components import general, signin_components
from saas.rxext import console
from saas.state import State


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


def verify_request_page() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.box(
                    # rx.heading(
                    #     config.formatted_application_name,
                    #     align="center",
                    #     size="8",
                    #     # class_name="text-3xl font-extrabold text-indigo-800 text-uppercase text-center",
                    # ),
                    rx.heading("Check your email", class_name="text-center"),
                    general.homepage_card(button_text="A sign in link has been sent to your email address."),
                    class_name="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg",
                ),
            ),
            class_name="min-h-screen bg-gradient-to-b from-indigo-50 to-white flex items-center justify-center px-4",
        ),
    )


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


def auth_verify_page() -> rx.Component:
    return rx.heading("User Authed")


def dashboard_page() -> rx.Component:
    return rx.box(
        rx.heading("Dashboard"),
        rx.text("Welcome to the dashboard!"),
    )
