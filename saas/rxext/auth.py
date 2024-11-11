import functools

import reflex as rx

# def require_google_login(page) -> rx.Component:
#     @functools.wraps(page)
#     def _auth_wrapper() -> rx.Component:
#         return GoogleOAuthProvider.create(
#             rx.cond(
#                 State.is_hydrated,
#                 rx.cond(State.token_is_valid, page(), login()),
#                 rx.spinner(),
#             ),
#             client_id=CLIENT_ID,
#         )

#     return _auth_wrapper


def require_login(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated, then redirect to the login page.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """

    def protected_page():
        return rx.cond(
            LoginState.is_authenticated,
            page(),
            rx.center(
                rx.spinner(on_mount=LoginState.redir),
                width="100vw",
                height="100vh",
            ),
        )

    protected_page.__name__ = page.__name__
    return protected_page
