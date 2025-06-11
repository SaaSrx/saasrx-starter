"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxext import rxext_info

from saasrx.api.bootstrap import api_app
from saasrx.state import State
from saasrx.pages import index


class User(rx.Model, table=True):
    username: str
    email: str

    def test_func(self, other_val: str):
        return f"Hello {other_val}"

app = rx.App(
    api_transformer=api_app,
    admin_dash=rx.AdminDash(models=[User]),
)
app.add_page(index)
