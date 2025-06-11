import reflex as rx

from rxext.components import navbar
from rxext import rxext_info
from saasrx.state.menu_items import MenuItems


def main_content() -> rx.Component:
    return rx.box(
        rx.heading(rxext_info),
        rx.divider(),
        rx.text("refactor/migrate to reflex 0.7.xx"),
    )


# test the navbar.for_page wrapper to see how to use with require_login
# @navbar.for_page
def index() -> rx.Component:
    return rx.box(
        navbar.navbar_desktop(items=MenuItems),
        main_content(),
    )
