import reflex as rx


def checkout_success():
    return rx.box(
        rx.text("Checkout successful!"),
    )
