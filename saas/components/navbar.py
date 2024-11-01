import reflex as rx

import rxconfig
from saas.state import MenuState

# Define your MenuLinks here
MenuLinks: dict[str, str] = {
    # href: link-text
}

# ---- Navbar General Components


def navbar_icon() -> rx.Component:
    return rx.box(
        rx.box(rx.icon("rocket", class_name="h-8 w-8"), class_name="text-indigo-600"),
        rx.text(
            MenuState.menu_title,
            class_name="ml-2 text-xl font-bold text-gray-900",
            on_click=MenuState.toggle_menu_title,
        ),
        class_name="flex items-center",
    )


# ---- Navbar Desktop Components


def navbar_desktop() -> rx.Component:
    link_style = "text-gray-600 hover:text-gray-900"
    btn_style = "bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
    return rx.box(
        rx.link("Features", href="#features", class_name=link_style),
        rx.link("Pricing", href="#pricing", class_name=link_style),
        rx.link("Testimonials", href="#testimonials", class_name=link_style),
        rx.link(rx.button("Get Started", class_name=btn_style), href="#get-started"),
        class_name="hidden md:flex items-center space-x-8",
    )


def navbar_desktop_open() -> rx.Component:
    return rx.box()


# ---- Navbar Mobile Components


def navbar_mobile() -> rx.Component:
    return rx.box()


def navbar_menu_open() -> rx.Component:
    return rx.box()


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
        rx.cond(
            MenuState.is_open,
            navbar_menu_open(),
        ),
        # Styling for the nav component
        class_name="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md z-50 border-b border-gray-100",
    )
