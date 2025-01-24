from typing import Callable

import reflex as rx

from saas.state import MenuItem, MenuState

# ---- Navbar General Components


def navbar_icon(app_icon: str = "rocket") -> rx.Component:
    return rx.box(
        rx.box(rx.icon(app_icon, class_name="h-8 w-8"), class_name="text-indigo-600"),
        rx.text(
            MenuState.menu_title,
            class_name="ml-2 text-xl font-bold text-gray-900",
            on_click=MenuState.toggle_menu_title,
        ),
        class_name="flex items-center",
    )


def make_menu_items(
    items: list[MenuItem],
    link_func: Callable[[str, str], rx.Component],
    btn_func: Callable[[str, str], rx.Component],
):
    def inner_func(item):
        return rx.match(
            item.typeof,
            ("link", link_func(item.text, item.link)),
            ("button", btn_func(item.text, item.link)),
            rx.text("Unknown MenuType."),
        )

    # rather than have inner_fn and outer, just apply foreach here
    return rx.foreach(items, inner_func)


# ---- Navbar Desktop Components


def navbar_desktop() -> rx.Component:
    link_style = "text-gray-600 hover:text-gray-900"
    btn_style = "text-white px-6 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-700 transition-colors"

    def link_func(text: str, href: str):
        return rx.link(text, href=href, class_name=link_style)

    def btn_func(text: str, href: str):
        return rx.link(rx.button(text, class_name=btn_style), href=href)

    return rx.box(
        make_menu_items(items=MenuState.menu_items, link_func=link_func, btn_func=btn_func),
        class_name="hidden md:flex items-center space-x-8",
    )


def navbar_desktop_() -> rx.Component:
    link_style = "text-gray-600 hover:text-gray-900"
    btn_style = "bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"

    def handler(item):
        return rx.match(
            item.typeof,
            ("link", rx.link(item.text, href=item.link, class_name=link_style)),
            ("button", rx.link(rx.button(item.text, class_name=btn_style), href=item.link)),
            rx.text("Unknown MenuType."),
        )

    return rx.box(
        rx.foreach(MenuState.menu_items, handler),
        class_name="hidden md:flex items-center space-x-8",
    )


# ---- Navbar Mobile Components


def navbar_mobile() -> rx.Component:
    # link_style = "text-gray-600 hover:text-gray-900"
    link_style = ""
    # btn_style = "px-6 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-800 text-white transition-colors"
    btn_style = "bg-indigo-500 hover:bg-indigo-800 transition-colors"

    def link_func(text, href):
        return rx.menu.item(text, href=href, class_name=link_style)

    def btn_func(text, href):
        return rx.menu.item(rx.link(text, href=href, class_name="text-white"), class_name=btn_style)

    return rx.box(
        rx.menu.root(
            rx.menu.trigger(
                rx.icon("menu", size=30),
            ),
            rx.menu.content(
                make_menu_items(items=MenuState.menu_items, link_func=link_func, btn_func=btn_func),
            ),
        ),
        class_name="flex",
    )


def navbar_items() -> rx.Component:
    return rx.box(
        rx.box(
            navbar_icon(),
            # Desktop navigation links
            rx.desktop_only(navbar_desktop()),
            # Mobile menu button
            rx.mobile_and_tablet(navbar_mobile()),
            class_name="flex justify-between items-center h-16",
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
    )


# Define the Navbar component
def navbar():
    return rx.el.nav(
        # Main container with styling
        navbar_items(),
        # Mobile navigation menu
        # Styling for the nav component
        # class_name="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md z-50 border-b border-gray-100",
        class_name="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md border-b border-gray-100",
    )
