import reflex as rx

from saas.pages import index
from saas.state import State


class App(rx.App):
    pass
    # theme = rx.theme(**config.theme.dict())


app = App()


def create_document():
    return rx.text("document page")


app.add_page(create_document, route="/docs")
app.add_page(index.index)
