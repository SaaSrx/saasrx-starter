from saas import pages
from saas.api import api_router
from saas.app_config import app_theme
from saas.models import Models
from saas.routes import ROUTES
from saas.rxext.app import App, make_admin_dash
from saas.state.state import AuthState

app = App(
    theme=app_theme,
    admin_dash=make_admin_dash(models=Models),
)

# add web pages here:
app.add_page(component=pages.index, route=ROUTES.INDEX)
app.add_page(component=pages.signin_page, route=ROUTES.SIGNIN)
app.add_page(component=pages.download_page, route=ROUTES.DOWNLOAD)
app.add_page(component=pages.dashboard_page, route=ROUTES.DASHBOARD)
app.add_page(component=pages.spinner, route="spinr")

# include the api router
app.api.include_router(api_router, prefix=ROUTES.API)

app.add_page(component=pages.verify_request_page, route=ROUTES.AUTH.VERIFY, on_load=AuthState.on_load_verify)
app.add_page(component=pages.payment_success, route=ROUTES.PAYMENT.SUCCESS)
