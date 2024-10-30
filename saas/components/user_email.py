import reflex as rx

from saas.state import CheckoutState


def user_email_form() -> rx.Component:
    return rx.box(
        rx.heading("email"),
        rx.form.root(
            rx.hstack(
                rx.input(
                    name="email",
                    placeholder="Enter email for purchase...",
                    type="email",
                    required=True,
                ),
                rx.button("purchase", type="submit"),
                width="100%",
            ),
            on_submit=CheckoutState.handle_submit,
        ),
    )
