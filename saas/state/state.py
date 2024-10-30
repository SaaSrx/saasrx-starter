import reflex as rx

# from saas.rxext.secrets import secrets
from rxconfig import config, secrets


def _complete_purchase(email: str):
    print("complete purcahse for email", email)


class State(rx.State):
    pass


class MenuState(State):
    menu_title: str = config.formated_app_name
    is_open: bool = False

    def toggle_menu(self):
        self.is_open = not self.is_open


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
