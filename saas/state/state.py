from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

import reflex as rx

from rxconfig import config
from saas.app_config import release_download
from saas.app_secret import secrets
from saas.models import MagicLink, User
from saas.rxext import console, is_prod_mode
from saas.rxext.utils.email_util import invalid_email


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
    # base state class
    @rx.var(cache=True)
    def is_prod_mode(self):
        return is_prod_mode()

    def gen_fake_user(self):
        try:
            user = User(email="graham@test.com")
            console.log(f"make user: {user=}")
            with rx.session() as session:
                session.add(user)
                session.commit()
        except Exception as err:
            console.log(f"Error creating user: {err=}")
        # console.log("doing this action")
        # user = User(email="graham@test.com")
        # console.log(f"Generated fake user: {user}")
        # auth = MagicLink(user_email=user.email)
        # console.log(f"Generated fake auth: {auth}")
        # with rx.session() as session:
        #     session.add(user)
        #     session.add(auth)
        #     session.commit()

    def get_fake_auth(self):
        with rx.session() as session:
            users = session.exec(
                MagicLink.select().where(User.email == "graham@test.com"),
            ).all()
            console.log(f"got users in get-fake-auth= {users=}")


class DownloadState(State):
    def download_release(self):
        # to setup the download for the release you need to symlink with the following:
        # ln -s "$PWD"/releases/ assets/releases
        return rx.download(url=release_download.filepath, filename=release_download.filename)


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
        user = session.exec(MagicLink.select().where(MagicLink.email == email)).first()
        return user


class AuthState(State):
    entered_user_email: str
    user_email: str

    show_redirect_alert: bool = False
    _auth_session: MagicLink = None

    # @rx.var(cache=True)
    # def auth_session(self) -> Optional[MagicLink]:
    #     return self._auth_session

    @rx.var(cache=True)
    def session_is_valid(self) -> bool:
        return True
        # return self.auth_session is not None

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

    def _check_recent(self, *args, **kwargs):
        return True

    def _get_user_from_email(self, email: str) -> User | bool:
        """
        Retrieve a user from the database based on their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User | bool: The User object if found, otherwise False.
        """
        with rx.session() as session:
            user = session.exec(User.select().where(User.email == email.lower())).first()
            return user or False

    def _get_magic_link(self, user: User) -> Optional[MagicLink]:
        with rx.session() as session:
            magic_link = session.exec(
                MagicLink.select().where(MagicLink.user_email == user.email, MagicLink.valid_link())
            ).first()
            if magic_link and magic_link.attempts_remaining > 0:
                magic_link.attempts_remaining -= 1  # Decrement remaining attempts
                session.add(magic_link)
                session.commit()
                return magic_link
        return None

    def _generate_magic_link(self, user: User):
        with rx.session() as session:
            magic_link = MagicLink(user_email=user.email)
            session.add(magic_link)
            session.commit()
        return magic_link

    def on_load_verify(self):
        params = self.router.page.params
        email = params.get("email")
        token = params.get("token")
        redir = params.get("redir")
        console.log(f"on_load_verify: {email=}, {token=}, {redir=}")
        # yield rx.redirect("/dashboard")

    def handle_login(self, data: dict = None):
        email = data.get("email")
        user = self._get_user_from_email(email=email)
        console.log(f"1User login: {user=}")
        if user:
            # if we have a user, send magic link
            magic_link = self._get_magic_link(user=user)
            console.log(f"2User login: {magic_link=}")
            user_check = self._check_recent(user=user, magic_link=magic_link)
            console.log(f"3User check: {user_check=}")

            if self.is_prod_mode:
                # Send email
                console.log(f"4sending email to: {user.email}")
            else:
                console.log(f"4click this magic link: {magic_link=}")
        else:
            yield rx.redirect(secrets.stripe_web_url + "?prefilled_email=" + email)
            # sending user to pay for the service

            # if user_check:
            #     magic_link = self._generate_link(user=user)

        # console.log(f"User login: {data=}")

        # user_found = False
        # # check_recent = self._check_recent(data["email"])
        # with rx.session() as session:
        #     # user = session.get(User, (data["email"],))
        #     # statement = select(User).where(User.user_email == email)
        #     statement = User.select().where(User.email == data["email"])
        #     console.log(f"made statement: {statement=}")
        #     user = session.exec(statement).first()
        #     # user = session.exec(User.select().where(User.email == data["email"])).first()
        #     if user:
        #         console.log(f"got user: {user=}")
        #     else:
        #         console.log(f"no user found: {data['email']=}")
        # # breakpoint()
        # # yield rx.toast.error(f"Email not found: {data['email']}")
        # # if not user_found:
        # #     return self.redirect_alert()
