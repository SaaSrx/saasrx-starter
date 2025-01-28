import functools
from typing import Callable

import reflex as rx


def not_logged_in_base() -> rx.Component:
    return rx.box(
        rx.text("Not logged in"),
        rx.link(rx.button("Login", class_name="text-white"), href="/"),
    )


def make_require_login(state: rx.State) -> Callable:
    """
    if using GoogleOAuthProvider, you can use the following:
        ```
        GoogleOAuthProvider.create(
            rx.cond(
                State.is_hydrated,
                rx.cond(State.token_is_valid, page(), login()),
                rx.spinner(),
            ),
            client_id=CLIENT_ID,
        )
        ```
    """

    def require_wrapper(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
        @functools.wraps(page)
        def protected_page() -> rx.Component:
            return rx.box(
                rx.cond(
                    state.is_hydrated,
                    rx.cond(
                        state.valid_session,
                        page(),
                        not_logged_in_base(),
                    ),
                    rx.spinner(),
                ),
            )

        return protected_page

    return require_wrapper
