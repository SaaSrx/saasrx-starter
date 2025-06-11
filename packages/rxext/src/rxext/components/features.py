from typing import Any

import reflex as rx


def features_section(
    features: list[dict[str, Any]],
    title: str = "Features",
    subtitle: str = "Everything in Python?",
    subtitle_emphasis: str = "Everything.",
    description: str = "Launch your SaaS product with confidence using our complete toolkit and guide.",
) -> rx.Component:
    """Modern features section component with configurable data.
    
    Args:
        features: List of feature dictionaries with 'name', 'description', and 'icon' keys
        title: Section title (defaults to "Features")
        subtitle: Primary subtitle text
        subtitle_emphasis: Emphasized subtitle text
        description: Section description text
    
    Returns:
        Responsive features grid component
    """
    return rx.box(
        rx.box(
            rx.box(
                rx.heading(
                    title,
                    size="4",
                    color=rx.color("accent", 11),
                    weight="bold",
                    text_transform="uppercase",
                    letter_spacing="wide",
                ),
                rx.heading(
                    subtitle,
                    size="8",
                    color=rx.color("gray", 12),
                    weight="bold",
                    mt="2",
                ),
                rx.heading(
                    subtitle_emphasis,
                    size="8", 
                    color=rx.color("gray", 12),
                    weight="bold",
                    mt="2",
                ),
                rx.text(
                    description,
                    size="5",
                    color=rx.color("gray", 11),
                    mt="4",
                    max_width="42rem",
                ),
                text_align="center",
                mx="auto",
            ),
            rx.box(
                rx.grid(
                    *[
                        rx.box(
                            rx.flex(
                                rx.box(
                                    rx.icon(
                                        feature["icon"],
                                        size=24,
                                        color="white",
                                    ),
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    height="3rem",
                                    width="3rem",
                                    bg=rx.color("accent", 9),
                                    border_radius="md",
                                    flex_shrink="0",
                                ),
                                rx.box(
                                    rx.heading(
                                        feature["name"],
                                        size="5",
                                        color=rx.color("gray", 12),
                                        weight="medium",
                                    ),
                                    rx.text(
                                        feature["description"],
                                        size="3",
                                        color=rx.color("gray", 11),
                                        mt="2",
                                    ),
                                ),
                                direction="row",
                                spacing="4",
                                align="start",
                            ),
                        )
                        for feature in features
                    ],
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing="6",
                ),
                mt="12",
            ),
            max_width="80rem",
            mx="auto",
            px="4",
        ),
        py="16",
        id="features",
    )


def default_features() -> list[dict[str, Any]]:
    """Default features list for SaaS applications."""
    return [
        {
            "name": "Entirely Python",
            "description": "Frontend and backend are both written in Python. No more context switching.",
            "icon": "worm",
        },
        {
            "name": "Lightning Fast Setup",
            "description": "Get your SaaS up and running in minutes with our pre-built components and templates.",
            "icon": "zap",
        },
        {
            "name": "Save Weeks of Development",
            "description": "Skip the boilerplate and focus on what makes your product unique.",
            "icon": "clock",
        },
        {
            "name": "Authentication Ready",
            "description": "Secure authentication system with social logins, ready out of the box.",
            "icon": "lock",
        },
        {
            "name": "Clean Code",
            "description": "Well-structured, documented code following best practices.",
            "icon": "code",
        },
        {
            "name": "Database Setup",
            "description": "Pre-configured database schemas and models for common use cases.",
            "icon": "database",
        },
    ]


def features() -> rx.Component:
    """Default features section using the default features list."""
    return features_section(default_features())