import reflex as rx

from saas.state import AuthState, MenuState


def redirect_cancel_buttons() -> rx.Component:
    return rx.flex(
        rx.hstack(
            rx.alert_dialog.cancel(
                rx.button(
                    "Cancel",
                    on_click=AuthState.redirect_alert_toggle,
                    variant="soft",
                    color_scheme="gray",
                ),
            ),
            rx.alert_dialog.cancel(
                rx.button(
                    "Home",
                    on_click=MenuState.redirect_home,
                    variant="soft",
                    color_scheme="iris",
                ),
            ),
        ),
        spacing="3",
        justify="between",
    )


def redirect_to_purchase_alert_dialog() -> rx.Component:
    return rx.box(
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.flex(
                    rx.alert_dialog.title(
                        "Lets get you started!",
                        class_name="mt-6 text-3xl font-extrabold text-indigo text-center",
                    ),
                    rx.box(
                        rx.alert_dialog.action(
                            rx.button(
                                "Purchase Access",
                                on_click=AuthState.redirect_to_external_purchase,
                                size="4",
                                class_name="w-[100%] justify-center",
                            ),
                        ),
                    ),
                    rx.alert_dialog.description(
                        f"No account found for: {AuthState.entered_user_email}. You need to purchase an account.",
                        class_name="my-5 text-md",
                    ),
                    direction="column",
                    spacing="2",
                ),
                redirect_cancel_buttons(),
            ),
            open=AuthState.show_redirect_alert,
        ),
    )


def signup_text() -> rx.Component:
    return rx.box(
        rx.text(
            "Don't have an account? Enter your email and we will redirect you to pay and create an account.",
            class_name="text-sm text-indigo-600/80",  # class_name="mt-2 text-sm text-indigo-700/80",
        ),
        class_name="mt-4 text-center",
    )


def signin_hero() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.icon(
                "mail",
                class_name="mx-auto h-12 w-12 stroke-2 hover:stroke-[3px] stroke-indigo-800",
            ),
            rx.heading(
                "Sign in to your account",  # delete this component after
                class_name="mt-6 text-3xl font-extrabold text-indigo-800",  #  text-center",
            ),
        ),
        text_align="center",
        justify="center",
    )


def email_signin_form() -> rx.Component:
    return rx.flex(
        rx.form.root(
            rx.flex(
                rx.form.field(
                    rx.flex(
                        # rx.form.label(""),  # if you want label above input,
                        rx.form.control(
                            rx.input(
                                placeholder="you@email.com",
                                on_change=AuthState.set_entered_user_email,
                                name="email",
                            ),
                            as_child=True,
                        ),
                        rx.form.message(
                            "A valid Email is required",
                            match="valueMissing",
                            force_match=AuthState.invalid_email,
                            color="var(--red-11)",
                        ),
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="email",
                    server_invalid=AuthState.signin_input_invalid,
                ),
                rx.form.submit(
                    rx.button(
                        "Send Magic Link Or Checkout",
                        disabled=AuthState.signin_input_invalid,
                        # class_name="bg-indigo-600 text-white hover:bg-indigo-800",
                    ),
                    as_child=True,
                ),
                direction="column",
                spacing="4",
            ),
            on_submit=AuthState.handle_login,
        ),
        width="100%",
        class_name="text-center",
    )
