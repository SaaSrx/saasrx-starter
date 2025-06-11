import reflex as rx


def spinning_status() -> rx.Component:
    """
    can further customize the spinner with mount like
    rx.spinner(on_mount=LoginState.redir)
    """
    return rx.center(rx.spinner())
