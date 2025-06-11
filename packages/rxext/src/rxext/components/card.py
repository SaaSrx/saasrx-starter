from typing import Any

import reflex as rx


def homepage_card(
    button_text: str,
    avatar_src: str,
    href: str = "#",
    heading_size: str = "5",
    avatar_size: str = "4",
    spacing: str = "3",
    text_align: str = "center",
    heading_props: dict[str, Any] | None = None,
    link_props: dict[str, Any] | None = None, 
    avatar_props: dict[str, Any] | None = None,
    flex_props: dict[str, Any] | None = None,
) -> rx.Component:
    """Configurable homepage card component with avatar and link.
    
    Args:
        button_text: Text to display as the heading
        avatar_src: Source URL for the avatar image
        href: Link destination (defaults to "#")
        heading_size: Size of the heading text (defaults to "5")
        avatar_size: Size of the avatar (defaults to "4")
        spacing: Spacing between elements (defaults to "3")
        text_align: Text alignment (defaults to "center")
        heading_props: Additional props for the heading
        link_props: Additional props for the link
        avatar_props: Additional props for the avatar
        flex_props: Additional props for the flex container
    
    Returns:
        A card component with avatar, heading, and link
    """
    heading_props = heading_props or {}
    link_props = link_props or {}
    avatar_props = avatar_props or {}
    flex_props = flex_props or {}
    
    # Merge default props with passed props
    final_heading_props = {"size": heading_size, **heading_props}
    final_flex_props = {"spacing": spacing, "align": "center", "direction": "column", **flex_props}
    final_link_props = {"href": href, **link_props}
    final_avatar_props = {"size": avatar_size, **avatar_props}
    
    return rx.card(
        rx.link(
            rx.flex(
                rx.avatar(src=avatar_src, **final_avatar_props),
                rx.heading(button_text, **final_heading_props),
                **final_flex_props,
            ),
            **final_link_props,
        ),
        text_align=text_align,
    )


def simple_card(
    title: str,
    description: str = "",
    icon: str = None,
    href: str = "#",
    variant: str = "surface",
) -> rx.Component:
    """Simple card component with optional icon, title, and description.
    
    Args:
        title: Card title
        description: Optional description text
        icon: Optional icon name
        href: Link destination
        variant: Card variant style
    
    Returns:
        A simple card component
    """
    content = []
    
    if icon:
        content.append(
            rx.icon(
                icon,
                size=24,
                color=rx.color("accent", 9),
                mb="3",
            )
        )
    
    content.append(
        rx.heading(
            title,
            size="4",
            color=rx.color("gray", 12),
            mb="2" if description else "0",
        )
    )
    
    if description:
        content.append(
            rx.text(
                description,
                size="2",
                color=rx.color("gray", 11),
            )
        )
    
    return rx.card(
        rx.link(
            rx.box(*content),
            href=href,
            text_decoration="none",
            color="inherit",
            _hover={"transform": "translateY(-2px)"},
            transition="transform 0.2s ease",
        ),
        variant=variant,
    )