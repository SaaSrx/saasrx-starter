import reflex as rx


def create_icon(alt_text, icon_tag):
    """Create an icon with specified alt text and tag."""
    return rx.icon(
        alt=alt_text,
        tag=icon_tag,
        height="3rem",
        margin_bottom="1rem",
        width="3rem",
    )


def create_heading(heading_level, font_size, text):
    """Create a heading with customizable font size and level."""
    return rx.heading(
        text,
        font_weight="600",
        margin_bottom="0.5rem",
        font_size=font_size,
        line_height="1.75rem",
        as_=heading_level,
    )


def create_colored_text(color, text):
    """Create text with a specified color."""
    return rx.text(
        text,
        # color=color,
    )


def create_feature_box(icon_alt, icon_tag, heading_text, description_text):
    """Create a feature box with an icon, heading, and description."""
    return rx.box(
        create_icon(alt_text=icon_alt, icon_tag=icon_tag),
        create_heading(
            heading_level="h3",
            font_size="1.25rem",
            text=heading_text,
        ),
        create_colored_text(color="#4B5563", text=description_text),
        # background_color="#ffffff",
        padding="1.5rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_button(hover_styles, background_color, text):
    """Create a customizable button with hover effects."""
    return rx.el.a(
        text,
        href="#",
        # background_color=background_color,
        transition_duration="300ms",
        font_weight="600",
        # _hover=hover_styles,
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        border_radius="0.5rem",
        # color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_hero_section():
    """Create the hero section with title, description, and call-to-action button."""
    return rx.box(
        rx.heading(
            "Launch Your Python Project Fast",
            font_weight="700",
            margin_bottom="1rem",
            font_size="2.25rem",
            line_height="2.5rem",
            # color="#111827",
            as_="h1",
        ),
        rx.text(
            "Pre-built code and tools for rapid development of SaaS, AI tools, and web apps",
            margin_bottom="2rem",
            # color="#4B5563",
            font_size="1.25rem",
            line_height="1.75rem",
        ),
        create_button(
            hover_styles={"background-color": "#1D4ED8"},
            background_color="#2563EB",
            text="Get Started",
        ),
        margin_bottom="3rem",
        text_align="center",
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.heading("Welcome to SaaS RX! 🤠"),
        # create_feature_box(
        #     icon_alt="Payment Icon",
        #     icon_tag="credit-card",
        #     heading_text="Payment Integration",
        #     description_text="Easy setup for various payment gateways to monetize your app quickly.",
        # ),
        # create_hero_section(),
        rx.link(rx.button("docs"), href="/docs"),
        rx.theme_panel(default_open=False),
    )
