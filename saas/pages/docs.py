import reflex as rx


def create_hover_link(hover_style, href, content):
    """Create a link with hover effect and custom color."""
    return rx.link(
        content,
        href=href,
        _hover=hover_style,
        color="#4B5563",
    )


def create_bold_link(href, content):
    """Create a bold link with custom color and font weight."""
    return rx.link(
        content,
        href=href,
        font_weight="600",
        color="#2563EB",
    )


def create_custom_heading(heading_type, font_size, content):
    """Create a custom heading with specified font size and weight."""
    return rx.heading(
        content,
        font_weight="600",
        margin_bottom="0.5rem",
        font_size=font_size,
        line_height="1.75rem",
        as_=heading_type,
    )


def create_section_heading(font_size, line_height, content):
    """Create a section heading with custom font size and line height."""
    return rx.heading(
        content,
        font_weight="700",
        margin_bottom="1rem",
        font_size=font_size,
        line_height=line_height,
        as_="h2",
    )


def create_list_item_with_hover_link(href, content):
    """Create a list item with a hover link."""
    return rx.list(
        rx.link(
            content,
            hover_style={"color": "#2563EB"},
            href=href,
            color="#4B5563",
        )
    )


def create_custom_text(color, margin_bottom, content):
    """Create custom text with specified color and bottom margin."""
    return rx.text(content, margin_bottom=margin_bottom, color=color)


def create_code_block(content):
    """Create a pre-formatted code block with custom styling."""
    return rx.el.pre(
        content,
        background_color="#1F2937",
        margin_bottom="1rem",
        padding="1rem",
        border_radius="0.5rem",
        color="#ffffff",
    )


def create_list_item(content):
    """Create a simple list item."""
    return rx.el.li(content)


def create_bullet_list(item1, item2, item3):
    """Create a bullet list with three items."""
    return rx.list(
        rx.list_item(item1),
        rx.list_item(item2),
        rx.list_item(item3),
        list_style_type="disc",
        list_style_position="inside",
        margin_bottom="1rem",
        color="#4B5563",
    )


def create_footer_link(content):
    """Create a footer link with hover effect."""
    return rx.link(content, href="#", _hover={"color": "#ffffff"})


def create_footer_list_item(content):
    """Create a footer list item with a link."""
    return rx.list(create_footer_link(content=content))


def create_header():
    """Create the header section with logo and navigation links."""
    return rx.flex(
        rx.box(
            "RefleX Boilerplate",
            font_weight="700",
            color="#1F2937",
            font_size="1.25rem",
            line_height="1.75rem",
        ),
        rx.flex(
            rx.link(
                "Home",
                href="/",
                hover_style={"color": "#1F2937"},
            ),
            create_bold_link(href="#", content="Documentation"),
            create_hover_link(
                hover_style={"color": "#1F2937"},
                href="#",
                content="Community",
            ),
            create_hover_link(
                hover_style={"color": "#1F2937"},
                href="#",
                content="Pricing",
            ),
            display="flex",
            column_gap="1rem",
        ),
        display="flex",
        align_items="center",
        justify_content="space-between",
    )


def create_header_container():
    """Create a container for the header with responsive styling."""
    return rx.box(
        rx.box(
            create_header(),
            width="100%",
            style=rx.breakpoints(
                {
                    "640px": {"max-width": "640px"},
                    "768px": {"max-width": "768px"},
                    "1024px": {"max-width": "1024px"},
                    "1280px": {"max-width": "1280px"},
                    "1536px": {"max-width": "1536px"},
                }
            ),
            margin_left="auto",
            margin_right="auto",
            padding_left="1.5rem",
            padding_right="1.5rem",
            padding_top="0.75rem",
            padding_bottom="0.75rem",
        ),
        background_color="#ffffff",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_sidebar():
    """Create the sidebar with documentation links."""
    return rx.box(
        create_section_heading(
            font_size="1.25rem",
            line_height="1.75rem",
            content="Documentation",
        ),
        rx.box(
            rx.list(
                rx.el.li(
                    create_bold_link(
                        href="#getting-started",
                        content="Getting Started",
                    )
                ),
                create_list_item_with_hover_link(
                    href="#configuration",
                    content="Configuration",
                ),
                create_list_item_with_hover_link(
                    href="#api-reference",
                    content="API Reference",
                ),
                create_list_item_with_hover_link(
                    href="#troubleshooting",
                    content="Troubleshooting",
                ),
                display="flex",
                flex_direction="column",
                gap="0.5rem",
            )
        ),
        padding_right="2rem",
        width="16rem",
    )


def create_getting_started_section():
    """Create the 'Getting Started' section of the documentation."""
    return rx.box(
        create_section_heading(
            font_size="1.5rem",
            line_height="2rem",
            content="Getting Started",
        ),
        create_custom_text(
            color="#4B5563",
            margin_bottom="1rem",
            content="Welcome to the RefleX Boilerplate documentation. This guide will help you set up and start using the boilerplate for your projects.",
        ),
        create_custom_heading(
            heading_type="h3",
            font_size="1.25rem",
            content="Installation",
        ),
        create_code_block(content=" pip install reflex-boilerplate "),
        create_custom_heading(
            heading_type="h3",
            font_size="1.25rem",
            content="Quick Start",
        ),
        rx.list.ordered(
            create_list_item(content="Create a new project"),
            create_list_item(content="Configure your settings"),
            create_list_item(content="Run the development server"),
            list_style_type="decimal",
            list_style_position="inside",
            margin_bottom="1rem",
            color="#4B5563",
        ),
        id="getting-started",
        margin_bottom="2rem",
    )


def create_env_file_instruction():
    """Create instructions for setting up environment variables."""
    return rx.text(
        "Set up your environment variables in the ",
        rx.el.code(
            ".env",
            background_color="#E5E7EB",
            padding_left="0.5rem",
            padding_right="0.5rem",
            padding_top="0.25rem",
            padding_bottom="0.25rem",
            border_radius="0.25rem",
        ),
        " file:",
        margin_bottom="1rem",
        color="#4B5563",
    )


def create_troubleshooting_section():
    """Create the 'Troubleshooting' section of the documentation."""
    return rx.box(
        create_section_heading(
            font_size="1.5rem",
            line_height="2rem",
            content="Troubleshooting",
        ),
        create_custom_text(
            color="#4B5563",
            margin_bottom="1rem",
            content="Common issues and their solutions:",
        ),
        create_custom_heading(
            heading_type="h3",
            font_size="1.25rem",
            content="Database Connection Issues",
        ),
        create_custom_text(
            color="#4B5563",
            margin_bottom="1rem",
            content="If you're experiencing database connection problems, ensure that:",
        ),
        id="troubleshooting",
        margin_bottom="2rem",
    )


def create_main_content():
    """Create the main content area of the documentation page."""
    return rx.box(
        rx.heading(
            "RefleX Boilerplate Documentation",
            font_weight="700",
            margin_bottom="1.5rem",
            font_size="1.875rem",
            line_height="2.25rem",
            as_="h1",
        ),
        create_getting_started_section(),
        rx.box(
            create_section_heading(
                font_size="1.5rem",
                line_height="2rem",
                content="Configuration",
            ),
            create_custom_text(
                color="#4B5563",
                margin_bottom="1rem",
                content="Learn how to configure the RefleX Boilerplate to suit your project needs.",
            ),
            create_custom_heading(
                heading_type="h3",
                font_size="1.25rem",
                content="Environment Variables",
            ),
            create_env_file_instruction(),
            create_code_block(
                content=""" DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
DEBUG=True """
            ),
            id="configuration",
            margin_bottom="2rem",
        ),
        rx.box(
            create_section_heading(
                font_size="1.5rem",
                line_height="2rem",
                content="API Reference",
            ),
            create_custom_text(
                color="#4B5563",
                margin_bottom="1rem",
                content="Explore the available API endpoints and their usage.",
            ),
            create_custom_heading(
                heading_type="h3",
                font_size="1.25rem",
                content="Authentication",
            ),
            create_code_block(
                content=""" POST /api/auth/login
POST /api/auth/register
GET /api/auth/user """
            ),
            create_custom_heading(
                heading_type="h3",
                font_size="1.25rem",
                content="Data Management",
            ),
            create_code_block(
                content=""" GET /api/data
POST /api/data
PUT /api/data/:id
DELETE /api/data/:id """
            ),
            id="api-reference",
            margin_bottom="2rem",
        ),
        create_troubleshooting_section(),
        flex="1 1 0%",
    )


def create_content_container():
    """Create a responsive container for the main content and sidebar."""
    return rx.flex(
        create_sidebar(),
        create_main_content(),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        display="flex",
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
        padding_top="2rem",
        padding_bottom="2rem",
    )


def create_email_input():
    """Create an email input field for the newsletter subscription."""
    return rx.el.input(
        placeholder="Enter your email",
        required=True,
        type="email",
        background_color="#374151",
        _focus={"outline-style": "none"},
        padding_left="0.75rem",
        padding_right="0.75rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_top_left_radius="0.5rem",
        border_bottom_left_radius="0.5rem",
        color="#ffffff",
    )


def create_subscribe_button():
    """Create a subscribe button for the newsletter form."""
    return rx.el.button(
        "Subscribe",
        type="submit",
        background_color="#2563EB",
        transition_duration="300ms",
        _hover={"background-color": "#1D4ED8"},
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_top_right_radius="0.5rem",
        border_bottom_right_radius="0.5rem",
        color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_footer_content():
    """Create the main content of the footer section."""
    return rx.flex(
        rx.box(
            create_custom_heading(
                heading_type="h3",
                font_size="1.125rem",
                content="RefleX Boilerplate",
            ),
            rx.text(
                "Empowering developers to build faster and smarter.",
                color="#9CA3AF",
            ),
            margin_bottom=rx.breakpoints({"0px": "1.5rem", "768px": "0"}),
            width=rx.breakpoints({"0px": "100%", "768px": "25%"}),
        ),
        rx.box(
            create_custom_heading(
                heading_type="h4",
                font_size="1.125rem",
                content="Quick Links",
            ),
            rx.list(
                create_footer_list_item(content="Home"),
                create_footer_list_item(content="Features"),
                create_footer_list_item(content="Docs"),
                create_footer_list_item(content="Pricing"),
                color="#9CA3AF",
            ),
            margin_bottom=rx.breakpoints({"0px": "1.5rem", "768px": "0"}),
            width=rx.breakpoints({"0px": "100%", "768px": "25%"}),
        ),
        rx.box(
            create_custom_heading(
                heading_type="h4",
                font_size="1.125rem",
                content="Community",
            ),
            rx.list(
                create_footer_list_item(content="GitHub"),
                create_footer_list_item(content="Discord"),
                create_footer_list_item(content="Twitter"),
                color="#9CA3AF",
            ),
            margin_bottom=rx.breakpoints({"0px": "1.5rem", "768px": "0"}),
            width=rx.breakpoints({"0px": "100%", "768px": "25%"}),
        ),
        rx.box(
            create_custom_heading(
                heading_type="h4",
                font_size="1.125rem",
                content="Newsletter",
            ),
            create_custom_text(
                color="#9CA3AF",
                margin_bottom="0.5rem",
                content="Stay updated with our latest features and releases.",
            ),
            rx.form(
                create_email_input(),
                create_subscribe_button(),
                display="flex",
            ),
            width=rx.breakpoints({"0px": "100%", "768px": "25%"}),
        ),
        display="flex",
        flex_wrap="wrap",
        justify_content="space-between",
    )


def create_footer_container():
    """Create a container for the footer with copyright information."""
    return rx.box(
        create_footer_content(),
        rx.box(
            " © 2023 RefleX Boilerplate. All rights reserved. ",
            border_color="#374151",
            border_top_width="1px",
            margin_top="2rem",
            padding_top="2rem",
            text_align="center",
            color="#9CA3AF",
            font_size="0.875rem",
            line_height="1.25rem",
        ),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1.5rem",
        padding_right="1.5rem",
    )


def create_page_layout():
    """Create the overall layout of the page including header, content, and footer."""
    return rx.box(
        create_header_container(),
        create_content_container(),
        background_color="#F3F4F6",
        font_family='system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
    )


def create_document():
    """Create the complete document structure with necessary scripts and styles."""
    return rx.fragment(
        create_page_layout(),
    )
