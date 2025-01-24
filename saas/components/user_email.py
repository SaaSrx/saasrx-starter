import reflex as rx


def user_email_form() -> rx.Component:
    def _handle_data(data):
        # handle with CheckoutState
        pass

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
            on_submit=_handle_data,
        ),
    )
