from dataclasses import dataclass
from enum import StrEnum

import reflex as rx

from rxconfig import config
from saas.models import MagicLinkAuth, User
from saas.rxext import console
from saas.saas_secrets import secrets
from saas.utils.email_util import invalid_email


class MenuType(StrEnum):
    LINK = "link"
    BUTTON = "button"


@dataclass
class MenuItem:
    text: str
    link: str
    typeof: MenuType


MenuItems = [
    MenuItem("Features", "#features", "link"),
    MenuItem("Pricing", "#pricing", "link"),
    MenuItem("Testimonials", "#testimonials", "link"),
    MenuItem("Guide", "/guide", "link"),
    MenuItem("Get Started", "/signin", "button"),
]


class State(rx.State):
    pass


class DownloadState(State):
    def start_download(self):
        asset_path, filename = "releases/saasrx.zip", "saasrx.zip"
        return rx.download(url=asset_path, filename=filename)


class MenuState(State):
    menu_items: list[MenuItem] = MenuItems
    # ---
    menu_title: str = config.formated_app_name  # "SaaSrx"  # config.formated_app_name
    is_open: bool = False

    def toggle_menu(self):
        self.is_open = not self.is_open

    def toggle_menu_title(self):
        self.menu_title = {
            config.app_name: config.formated_app_name,
            config.formated_app_name: config.app_name,
        }.get(self.menu_title, config.app_name)

    def redirect_home(self):
        return rx.redirect("/")


class CheckoutState(rx.State):
    async def handle_submit(self, data: dict):
        print("handle submit", data)

        if stripe_web_url := secrets.get("stripe_web_url"):
            return rx.redirect(stripe_web_url)

        return rx.window_alert("No stripe web url!")

    def complete_purchase(self):
        pass


def _check_email(email: str):
    yield rx.toast.info(f"Checking email: {email}")
    # yield asyncio.sleep(2)
    yield rx.toast.success(f"Success: {email}")


async def _get_user(email: str) -> User:
    with rx.session() as session:
        user = session.exec(MagicLinkAuth.select().where(MagicLinkAuth.email == email)).first()
        return user


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
        return rx.redirect(secrets.stripe_web_url + "?prefilled_email=" + self.entered_user_email)

    def redirect_alert(self):
        self.show_redirect_alert = not self.show_redirect_alert
        console.log("show redirect alsert")

    def handle_login(self, data: dict = None):
        console.log(f"User login: {data=}")
        user_found = False
        yield rx.toast.error(f"Email not found: {data['email']}")
        if not user_found:
            return self.redirect_alert()
