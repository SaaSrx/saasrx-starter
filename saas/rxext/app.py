import reflex as rx
from reflex.app import Admin, AdminDash, Model
from reflex.app import App as BaseApp

from saas.app_config import config
from saas.rxext import console


def make_admin_dash(
    models: list[Model],
    title: str = "AppAdmin",
    logo_url=None,
) -> AdminDash:
    # if models is None:
    #     # TODO: make rxext stuff work without any config/secrets
    #     from saas.models import Models as models

    if not logo_url:
        logo_url = f"{config.deploy_url}/saasrx-icon.png"
    admin = Admin(
        engine=Model.get_db_engine(),
        title=title,
        logo_url=logo_url,
    )
    return rx.AdminDash(models=models, admin=admin)


class App(BaseApp):
    # admin_dash = rx.AdminDash(models=Models)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _apply_decorated_pages(self):
        super()._apply_decorated_pages()
        self._apply_decorated_pages_api()

    def _apply_decorated_pages_api(self):
        from saas.rxext.endpoints import API_DECORATED_PAGES

        for route, route_handlers in API_DECORATED_PAGES.items():
            console.debug(f"Adding API route: {route=}")
            for route_kwargs in route_handlers:
                # Add the API route to the FastAPI app
                self.api.add_api_route(**route_kwargs)
