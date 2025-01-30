import asyncio

from typing import Any, Callable
import urllib.parse

from datetime import datetime

import reflex as rx
from sqlmodel import select

from rxconfig import config
from saas.app_config import release_download
from saas.app_secret import secrets
from saas.models import AccessLevel, MagicLink, User, query
from saas.routes import ROUTES
from saas.rxext import console, is_prod_mode

from saas.rxext.auth import make_require_login
from saas.rxext.dto import MenuButton, MenuItem, MenuLink
from saas.rxext.utils import dev_invalid_email, get_stripe_payment_link, invalid_email

dev_should_email = not is_prod_mode() and False


MenuItems = [
    # use any of these types: MenuItem or MenuLink or MenuButton
    MenuItem(text="Features", link="#features", typeof="link"),
    MenuLink("Pricing", "#pricing"),
    MenuLink("Testimonials", "#testimonials"),
    MenuLink("Guide", "/guide"),
    MenuButton("Get Started", "/signin"),
]


class LocalDevInfo:
    def __init__(self):
        pass

    def _get_admin_info(self):
        with rx.session() as session:
            user = session.exec(select(User).where(User.access_level == AccessLevel.ADMIN)).first()
        return {user.email} if user else "NoAdmin"


class DownloadState(rx.State):
    def download_release(self):
        # to setup the download for the release you need to symlink with the following:
        # ln -s "$PWD"/releases/ assets/releases
        return rx.download(url=release_download.filepath, filename=release_download.filename)


class State(rx.State):
    # redirect helper
    redirect_cancel: bool = False
    redirect_timer_amt: int = 3
    _redirect_route: str = ROUTES.DASHBOARD
    _redirect_task: asyncio.Task | None = None  # this doesnt work afaict

    # base state class
    @rx.var(cache=True)
    def is_prod_mode(self) -> bool:
        return is_prod_mode()

    @rx.var(cache=False)
    def state_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # this will migrate to `rx.event(background=True)` in 0.6.5
    @rx.event(background=True)
    async def redirect_timer(self):
        """
        NOTE: Avoid redirects until it works with something like create_task which is cancellable

        Asynchronously waits for a specified duration and then returns a redirect response.

        This coroutine will sleep for the duration specified by the instance variable
        `_redirect_timer`, and then return a redirect response to the route specified
        by the instance variable `_redirect_route`.

        The reason this is necessary rather than using/partial or similar is that reflex
        requires using this specific format.
        trying to incorporate the rx.background decorated func will require understanding how
        `StateProxy` works for background tasks.

        # await asyncio.sleep(self._redirect_timer)
        # return rx.redirect(self._redirect_route)

        Returns:
            A redirect response to the specified route.
        """

        time_left, dec_amt = self.redirect_timer_amt, 1

        while time_left > 0:
            if self.redirect_cancel:
                async with self:
                    self.toggle_cancel_redirect()
                return rx.toast("Redirect cancelled.")
            await asyncio.sleep(dec_amt)
            time_left -= dec_amt
        return rx.redirect(self._redirect_route)

    @rx.event
    def toggle_cancel_redirect(self) -> None:
        self.redirect_cancel = not self.redirect_cancel


class MenuState(State):
    menu_items: list[MenuItem] = MenuItems
    # ---
    menu_title: str = config.formatted_application_name or config.app_name
    is_open: bool = False

    def toggle_menu(self) -> None:
        self.is_open = not self.is_open

    def toggle_menu_title(self) -> None:
        self.menu_title = {
            config.app_name: config.formatted_application_name,
            config.formatted_application_name: config.app_name,
        }.get(self.menu_title, config.app_name)

    def redirect_home(self) -> None:
        return rx.redirect("/")


class CheckoutState(rx.State):
    async def handle_submit(self, data: dict) -> None:
        console.log("handle submit", data)

        if stripe_web_url := secrets.get("stripe_web_url"):
            return rx.redirect(stripe_web_url)

        return rx.window_alert("No stripe web url!")

    def _redirect_to_checkout(self, email: str):
        return get_stripe_payment_link(email)

    def complete_purchase(self):
        pass


class AuthState(State):
    session_token: str = rx.LocalStorage(sync=True)
    entered_user_email: str
    # user_email: str
    user: User | None = None

    show_redirect_alert: bool = False
    _auth_session: MagicLink | None = None

    """
    note: rx.var are called regardless from reflex regardless of being used in a component/elsewhere
    """

    @rx.var(cache=False)
    def valid_session(self) -> bool:
        _valid = (self.session_token != "") and (self.user is not None)
        console.log(f"valid session: {_valid} for {self.user=}")
        return _valid

    @rx.var(cache=False)
    def token_is_valid(self) -> bool:
        return False

    @rx.var(cache=False)
    def invalid_email(self) -> bool:
        """
        used for live validation of the email input
        """
        if not self.is_prod_mode:
            return dev_invalid_email(self.entered_user_email)
        return invalid_email(self.entered_user_email)

    @rx.var(cache=False)
    def signin_input_invalid(self) -> bool:
        """
        check for invalid email when signing in (can extend to other inputs as well)
        """
        return self.invalid_email

    @rx.var(cache=True)
    def is_admin(self) -> bool:
        if not self.user:
            return False
        # For reflex, you need to use rx.var for schema properties
        return self.user.is_admin

    @rx.event
    async def handle_login(self, data: dict[str, Any] = {}):
        if not data:
            return await rx.toast.warning("No data provided")

        email: str = data.get("email", None)

        if not email:
            return rx.window_alert("Email is required")

        user: User | None = query.find_user_by_email(email=email)
        console.log(f"User login: {user=}")
        if user:
            magic_link_token = query.get_magic_link_token(user=user)
            return await self._send_magic_link(email=user.email, token=magic_link_token)
        else:
            self.show_redirect_alert = True

    @rx.event
    def redirect_signin(self):
        """Redirect to the redirect_to route if logged in, or to the login page if not."""
        if not self.is_hydrated:
            console.log("redirect since not hydrated!!")
            # wait until after hydration to ensure auth_token is known
            return AuthState.redirect_signin()  # type: ignore
        page = self.router.page.path
        console.log(f"redirect_signin: {page=} and {self.session_token=} and {self.user=}<==|||")
        return rx.redirect(ROUTES.SIGNIN)

    def redirect_to_external_purchase(self):
        return rx.redirect(secrets.stripe_web_url + "?prefilled_email=" + self.entered_user_email)

    def redirect_alert_toggle(self):
        self.show_redirect_alert = not self.show_redirect_alert
        console.log("show redirect alsert")

    def on_load_verify(self, success_redirect: str = ROUTES.DASHBOARD):
        """
        Verify the magic link and authenticate the user.

        This method is called when the user clicks on a magic link sent to their email.
        It extracts the email, token, and redirect URL from the page parameters,
        verifies the magic link, and if valid, sets the user's session and redirects
        to the appropriate page.

        Returns:
            rx.Component: A toast notification or redirect response.
        """

        email = self.router.page.params.get("email")
        token = self.router.page.params.get("token")
        redir = self.router.page.params.get("redir", success_redirect)

        console.debug(f"Doing on_load_verify with {email=}, {token=}, {redir=}")

        if (not email) or (not token):
            return rx.toast("Invalid magic link, please try again.")

        if (magic_link := query.check_magic_link(email=email, token=token)) is not None:
            yield rx.toast("Login Successful, redirecting to dashboard...")
            self.user = query.find_user_by_email(email=magic_link.user_email)
            if not self.user:
                return rx.toast("User not found, please try again.")

            self.session_token = magic_link.session_token
            # self.user_email = magic_link.user_email
            console.log(f"show session: {self.session_token=}")
            # prefer redirect directly rather than the previous background task of redirect_timer
            return rx.redirect(redir)

    async def _send_magic_link(self, email: str, token: str):
        params = urllib.parse.urlencode({"email": email, "token": token})
        route_url = urllib.parse.urljoin(config.deploy_url, ROUTES.AUTH.VERIFY)
        url = f"{route_url}?{params}"

        if self.is_prod_mode:
            console.log(f"Sending email to: {email}")
            # send email to user email with the url
        else:
            console.log(f"Dev-mode, magic link: {url}")
            # do redirecting automatically for dev
            return rx.redirect(url)


class DashboardState(AuthState):
    """State for the dashboard page."""

    @rx.var(cache=False)
    def dashboard_user(self) -> User | None:
        """Get the current user for the dashboard."""
        return self.user

    @rx.var(cache=False)
    def user_payments(self) -> list:
        """Get the user's payment history."""
        if self.user:
            return query.get_user_payments(self.user.email)
        return []


require_login: Callable[[Callable[[], rx.Component]], Callable[[], rx.Component]] = make_require_login(
    AuthState
)
