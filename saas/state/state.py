from datetime import datetime

import reflex as rx

from rxconfig import config
from saas.saas_config import secrets


def _complete_purchase(email: str):
    print("complete purchase for email", email)


class State(rx.State):
    pass


class MenuState(State):
    menu_title: str = config.formated_app_name  # "SaaSrx"  # config.formated_app_name
    is_open: bool = False

    def toggle_menu(self):
        self.is_open = not self.is_open

    def toggle_menu_title(self):
        self.menu_title = {
            config.app_name: config.formated_app_name,
            config.formated_app_name: config.app_name,
        }.get(self.menu_title, config.app_name)


class CheckoutState(rx.State):
    user_email: str = ""

    def handle_submit(self, data: dict):
        print("handle submit", data)

        _complete_purchase(data)
        print(f"secrets are:{secrets=}")

        if stripe_web_url := secrets.get("stripe_web_url"):
            return rx.redirect(stripe_web_url)

        return rx.window_alert("No stripe web url!")

    def complete_purchase(self):
        pass
