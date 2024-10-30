import reflex.app as app

import saas.rxext.console as console
from saas.rxext.endpoints import API_DECORATED_PAGES


class App(app.App):
    def _apply_decorated_pages(self):
        self._apply_decorated_pages_api()
        return super()._apply_decorated_pages()

    def _apply_decorated_pages_api(self):
        for route, route_handlers in API_DECORATED_PAGES.items():
            console.debug(f"Adding API route: {route=}")
            for route_kwargs in route_handlers:
                # Add the API route to the FastAPI app
                self.api.add_api_route(**route_kwargs)
