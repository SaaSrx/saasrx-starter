import reflex as rx

from saas.state import AuthState, DownloadState


def download_image() -> rx.Component:
    # Button to use to test if download is working
    return rx.button("zip", on_click=rx.download(url="/favicon.ico"))


def download_page() -> rx.Component:
    return rx.box(
        rx.button("zip", on_click=DownloadState.download_release),
    )


def dashboard_authed() -> rx.Component:
    return rx.box(
        rx.heading("Dashboard"),
        rx.text(f"Welcome to the dashboard user: {AuthState.user_email}"),
        rx.text(f"User Session: {AuthState.session_token}"),
    )


def dashboard_page() -> rx.Component:
    return rx.cond(
        AuthState.is_hydrated,
        rx.cond(
            AuthState.valid_session,
            dashboard_authed(),
            # AuthState.redirect_alert_dialog,
            rx.box("Not Authed"),
        ),
    )
