import functools
from typing import Callable

import reflex as rx

from saas.routes import ROUTES


def unauthorized_page_default() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.link(
                rx.button("Take me to login", class_name="text-white", size="4"),
                href=ROUTES.SIGNIN,
            ),
        ),
        class_name="flex items-center justify-center p-10",
    )


def make_require_login(
    state: rx.State,
    unauthorized_page: Callable = unauthorized_page_default,
) -> Callable:
    """
    if using GoogleOAuthProvider, you can use the following:
        ```
        GoogleOAuthProvider.create(
            rx.cond(
                State.is_hydrated,
                rx.cond(State.login_valid_check, page(), login()),
                rx.spinner(),
            ),
            client_id=CLIENT_ID,
        )
        ```
    """

    def require_wrapper(page: Callable) -> Callable:
        @functools.wraps(page)
        def protected_page() -> rx.Component:
            return rx.box(
                rx.cond(
                    state.is_hydrated,
                    rx.cond(
                        state.valid_session,
                        page(),
                        unauthorized_page(),
                    ),
                    rx.spinner(),
                ),
            )

        return protected_page

    return require_wrapper
