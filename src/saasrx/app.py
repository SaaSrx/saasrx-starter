import reflex as rx

from rxconfig import config
from saasrx.pages import index


class State(rx.State):
    """The app state."""

    _theme = config.theme


class App(rx.App):
    theme = rx.theme(**config.theme.dict())


app = App()


def create_document():
    return rx.text("document page")


app.add_page(create_document, route="/docs")
app.add_page(index.index)
