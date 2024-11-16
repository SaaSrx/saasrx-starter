import reflex as rx

from saas.state import AuthState, State


def signin_show_admin_info():
    return rx.box(
        rx.cond(
            ~State.is_prod_mode,
            rx.text(f"Login with: `{State.show_admin_info}`"),
        )
    )


def cancel_redirect():
    return rx.box(rx.button("Cancel Redirect", on_click=AuthState.toggle_cancel_redirect))
