import reflex as rx

from saas.state import AuthState, DownloadState


def download_page() -> rx.Component:
    _img_btn = rx.button("img", on_click=rx.download(url="/favicon.ico"))
    return rx.box(
        # _img_btn, # use this one to test if the download is working in general
        rx.button("zip", on_click=DownloadState.download_release),
    )


def dashboard_page() -> rx.Component:
    return rx.cond(
        AuthState.is_hydrated,
        rx.cond(
            AuthState.session_is_valid,
            rx.box(
                rx.heading("Dashboard"),
                rx.text(f"Welcome to the dashboard user: {AuthState.user_email}"),
            ),
            AuthState.redirect_alert_dialog,
        ),
    )
