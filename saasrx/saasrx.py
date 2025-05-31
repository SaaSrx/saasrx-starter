"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from rxext import rxext_info


class State(rx.State):
    """The app state."""

    ...


class User(rx.Model, table=True):
    username: str
    email: str


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.text("refactor/migrate to reflex 0.7.13"),
        rx.divider(),
        rx.heading(rxext_info),
    )


app = rx.App(admin_dash=rx.AdminDash(models=[User]))
app.add_page(index)
