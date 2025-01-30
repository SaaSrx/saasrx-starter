import reflex as rx

from saas.components import features, navbar, download
from saas.state import require_login


@navbar.for_page
@require_login
def download_page() -> rx.Component:
    return download.download_release()


def spinning_status() -> rx.Component:
    """
    can further customize the spinner with mount like
    rx.spinner(on_mount=LoginState.redir)
    """
    return rx.center(rx.spinner())


# test the navbar.for_page wrapper to see how to use with require_login
# @navbar.for_page
def index() -> rx.Component:
    return navbar.page_with_navbar(
        features.features(),
    )
