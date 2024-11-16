import reflex as rx

from saas.app_config import config, image_assets


def homepage_card(
    button_text: str = config.formatted_application_name,
    avatar_src: str = image_assets["favicon"],
    # size: str = "2",
    heading_props: dict = {},
    link_props: dict = {},
    avatar_props: dict = {},
    flex_props: dict = {},
) -> rx.Component:
    heading_props = {"size": "2", **heading_props}
    flex_props = {"class_name": "text-center", "spacing": "3", **flex_props}
    link_props = {"href": config.deploy_url, "class_name": "items-center", **link_props}
    return rx.card(
        rx.link(
            rx.flex(
                rx.avatar(src=avatar_src, **avatar_props),
                rx.heading(button_text, **heading_props),
                **flex_props,
            ),
            **link_props,
        ),
        as_child=True,
    )
