import reflex as rx

from rxconfig import config
from saas.rxext import console
from saas.saas_config import secrets
from saas.utils.email_util import invalid_email


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
    async def handle_submit(self, data: dict):
        print("handle submit", data)

        _complete_purchase(data)
        print(f"secrets are:{secrets=}")

        if stripe_web_url := secrets.get("stripe_web_url"):
            return rx.redirect(stripe_web_url)

        return rx.window_alert("No stripe web url!")

    def complete_purchase(self):
        pass


def _check_email(email: str):
    yield rx.toast.info(f"Checking email: {email}")
    # yield asyncio.sleep(2)
    yield rx.toast.success(f"Success: {email}")


class AuthState(State):
    entered_user_email: str
    user_email: str

    show_redirect_alert: bool = False

    @rx.var
    def invalid_email(self) -> bool:
        return invalid_email(self.entered_user_email)

    @rx.var
    def input_invalid(self) -> bool:
        return self.invalid_email

    def redirect_to_external_purchase(self):
        return rx.redirect(secrets.stripe_web_url)

    def redirect_alert(self):
        self.show_redirect_alert = not self.show_redirect_alert
        console.log("show redirect alsert")

    def handle_login(self, data: dict = None):
        console.log(f"User login: {data=}")
        user_found = False
        yield rx.toast.error(f"Email not found: {data['email']}")
        if not user_found:
            return self.redirect_alert()
