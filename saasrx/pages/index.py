import reflex as rx

from rxext.components import navbar, card, features
from rxext import rxext_info
from saasrx.state.menu_items import MenuItems


def hero_section() -> rx.Component:
    """Hero section with main heading and call-to-action buttons."""
    return rx.vstack(
        rx.heading("SaaSRX Starter", size="9", mb="2"),
        rx.heading("Launch your SaaS in Python", size="6", color=rx.color("gray", 11), weight="medium", mb="4"),
        rx.text(
            "Build your entire SaaS application using Python with Reflex. Front-end, back-end, everything in between.",
            mb="6",
            max_width="600px",
            text_align="center",
        ),
        rx.hstack(
            rx.button("Get Started", on_click=rx.redirect("/signin"), size="3"),
            rx.button("Learn More", variant="outline", on_click=rx.redirect("#features"), size="3"),
            spacing="4",
        ),
        padding="8em 1em 4em 1em",
        align_items="center",
    )


def cards_section() -> rx.Component:
    """Cards section showcasing main features."""
    return rx.vstack(
        rx.heading("Quick Access", size="7", mb="6"),
        rx.grid(
            card.homepage_card(
                "Documentation", "/static/docs-icon.png", href="/docs", link_props={"is_external": True}
            ),
            card.homepage_card("Templates", "/static/templates-icon.png", href="/templates"),
            card.homepage_card("Admin", "/static/admin-icon.png", href="/admin"),
            card.homepage_card("API", "/static/api-icon.png", href="/api/docs", link_props={"is_external": True}),
            columns=rx.breakpoints(initial="1", sm="2", lg="4"),
            spacing="6",
        ),
        padding="4em 1em",
        max_width="1200px",
        width="100%",
        margin="0 auto",
    )


def main_content() -> rx.Component:
    return rx.box(
        hero_section(),
        cards_section(),
        features.features(),
        rx.divider(),
        rx.box(rx.text(rxext_info), padding="2em", text_align="center"),
        width="100%",
        overflow_x="hidden",
    )


def index() -> rx.Component:
    return rx.box(
        navbar.navbar(items=MenuItems, app_icon="rocket", app_name="SaaSRX"),
        main_content(),
    )
