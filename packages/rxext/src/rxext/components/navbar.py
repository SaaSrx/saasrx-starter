import reflex as rx
from rxext.dto import MenuItem

# from saas.state import MenuItem, MenuState

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

# In a shared-library context we should *not* depend on any application-level
# state.  Therefore, callers **must** explicitly supply their `MenuItem` list to
# the public helpers.  No implicit fallbacks are attempted.


def _link_component(text: str, href: str, is_button: bool = False, mobile: bool = False) -> rx.Component:  # noqa: E501
    """Return the link representation for a single menu item.

    Args:
        text: Text to display.
        href: The target URL.
        is_button: If ``True`` render a *button* style link, otherwise render a plain text link.
        mobile: If ``True`` the component is rendered inside a mobile dropdown menu.
    """
    if is_button:
        if mobile:
            return rx.menu.item(
                rx.link(
                    rx.text(text, size="3", weight="medium", color="white"),
                    href=href,
                ),
                bg=rx.color("accent", 5),
                _hover={"bg": rx.color("accent", 6)},
                border_radius="md",
            )
        # desktop button style
        return rx.link(
            rx.button(
                text,
                bg=rx.color("accent", 5),
                color="white",
                _hover={"bg": rx.color("accent", 6)},
                px="1em",
                py="0.5em",
            ),
            href=href,
        )

    # ---------------------------------------------------------------------
    # Plain link styles
    # ---------------------------------------------------------------------
    if mobile:
        return rx.menu.item(text, href=href)
    return rx.link(
        text,
        href=href,
        color=rx.color("gray", 9),
        _hover={"color": rx.color("gray", 12)},
    )


def _build_menu_items(items: list[MenuItem], mobile: bool = False) -> list[rx.Component]:
    """Create a list of components representing each menu item."""
    components: list[rx.Component] = []
    for item in items:
        components.append(
            _link_component(
                text=item.text,
                href=item.link,
                is_button=item.typeof == "button" or str(item.typeof).lower() == "button",  # type: ignore[arg-type]
                mobile=mobile,
            )
        )
    return components


# ---------------------------------------------------------------------------
# Public components
# ---------------------------------------------------------------------------


def navbar_icon(app_icon: str = "rocket", *, desktop: bool = False, app_name: str = "SaaSRX") -> rx.Component:
    """Branded icon & title used in both breakpoints (larger on desktop)."""
    return rx.hstack(
        rx.icon(app_icon, size=24, color=rx.color("accent", 9)),
        rx.heading(
            app_name,
            size="7" if desktop else "6",
            weight="bold",
            color=rx.color("gray", 12),
        ),
        align_items="center",
        spacing="3",
    )


# ---- Navbar Desktop & Mobile Layouts -----------------------------------------


def navbar_desktop(items: list[MenuItem], app_icon: str = "rocket", app_name: str = "SaaSRX") -> rx.Component:
    """Horizontal navbar suitable for *desktop* screens."""
    return rx.hstack(
        navbar_icon(app_icon=app_icon, desktop=True, app_name=app_name),
        rx.hstack(*_build_menu_items(items), spacing="6", align_items="center"),
        justify="between",
        align_items="center",
        width="100%",
    )


def navbar_mobile(items: list[MenuItem], app_icon: str = "rocket", app_name: str = "SaaSRX") -> rx.Component:
    """Compact navbar with *hamburger* style dropdown for mobile / tablet."""
    return rx.hstack(
        navbar_icon(app_icon=app_icon, app_name=app_name),
        rx.menu.root(
            rx.menu.trigger(rx.icon("menu", size=30, color=rx.color("accent", 9))),
            rx.menu.content(*_build_menu_items(items, mobile=True)),
        ),
        justify="between",
        align_items="center",
        width="100%",
    )


# ---- Top-level helpers --------------------------------------------------------


def navbar(items: list[MenuItem], app_icon: str = "rocket", app_name: str = "SaaSRX") -> rx.Component:
    """Responsive navbar rendered for *all* breakpoints.

    This shared-library component is **pure**—it does not import application
    globals.  You must pass in the list of menu items you want displayed.
    """
    return rx.box(
        rx.desktop_only(navbar_desktop(items=items, app_icon=app_icon, app_name=app_name)),
        rx.mobile_and_tablet(navbar_mobile(items=items, app_icon=app_icon, app_name=app_name)),
        bg=rx.color("accent", 3),
        backdrop_filter="blur(8px)",
        border_bottom=f"1px solid {rx.color('gray', 6)}",
        padding="1em",
        width="100%", 
        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="1000",
        box_shadow="0 2px 10px rgba(0,0,0,0.05)"
    )


def page_with_navbar(*children: list[rx.Component], items: list[MenuItem], app_icon: str = "rocket", app_name: str = "SaaSRX") -> rx.Component:
    """Wrap arbitrary components with a fixed navbar and appropriate top padding."""
    return rx.box(
        navbar(items=items, app_icon=app_icon, app_name=app_name),
        rx.box(*children, pt="4.5em"),  # ≈ 72 px top padding for fixed navbar
    )


# def for_page(func) -> Callable[..., rx.Component]:
#     """Decorator that wraps a page component with the navbar and proper spacing.

#     Args:
#         func: The page component function to wrap

#     Returns:
#         The wrapped component with navbar and spacing
#     """

#     def wrapper(*args, **kwargs):
#         return page_with_navbar(items=MenuState.menu_items, func(*args, **kwargs))

#     return wrapper
