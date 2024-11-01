import reflex as rx

from saas.state import AuthState


def redirect_alert_dialog() -> rx.Component:
    # return rx.container(
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.flex(
                rx.alert_dialog.title(
                    "Lets get you started!",
                    class_name="mt-6 text-3xl font-extrabold text-indigo text-center",
                ),
                rx.alert_dialog.description(
                    f"No account found, purchase access for: {AuthState.entered_user_email}",
                    class_name="my-4 text-md",
                ),
                direction="column",
                spacing="2",
                align="stretch",
                justify="center",
            ),
            rx.flex(
                rx.hstack(
                    rx.alert_dialog.cancel(
                        rx.button(
                            "Cancel",
                            on_click=AuthState.redirect_alert,
                            variant="soft",
                            color_scheme="gray",
                        ),
                    ),
                    rx.alert_dialog.cancel(
                        rx.button(
                            "Home",
                            on_click=rx.redirect("/"),
                            variant="soft",
                            color_scheme="iris",
                        ),
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Purchase Access",
                        on_click=AuthState.redirect_to_external_purchase,
                        class_name="bg-indigo-600 text-white hover:bg-indigo-800",
                    ),
                ),
                spacing="3",
                justify="between",
                # class_name="flex justify-between",
            ),
            width="50%",
        ),
        open=AuthState.show_redirect_alert,
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
            # rx.text(
            #     "If you have an account, we'll send you a magic link to your email. Otherwise we'll redirect you to purchase access which will create an account.",
            #     class_name="mt-2 text-sm text-indigo-700/80",
            # ),
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
                        rx.form.label(""),  # "Email",
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
                    server_invalid=AuthState.invalid_email,
                ),
                rx.form.submit(
                    rx.button(
                        "Send Magic Link Or Checkout",
                        disabled=AuthState.input_invalid,
                        color_scheme="indigo",
                        width="100%",
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
