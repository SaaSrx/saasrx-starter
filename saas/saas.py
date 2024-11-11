from saas import pages
from saas.api import api_router
from saas.app_config import app_theme
from saas.models import Models
from saas.rxext.app import App, make_admin_dash

app = App(
    theme=app_theme,
    admin_dash=make_admin_dash(models=Models),
)

# add web pages here:
app.add_page(component=pages.index, route="/")
app.add_page(component=pages.signin_page, route="/signin")
app.add_page(component=pages.download_page, route="/download")

# include the api router
app.api.include_router(api_router, prefix="/api")

app.add_page(component=pages.verify_request_page, route="/auth/verify")
app.add_page(component=pages.payment_success, route="/payment/success")
# app.add_page(component=pages.verify_request_page, route="/auth/verify", on_load=AuthState.on_load_verify)
# app.add_page(component=pages.auth_verify_page, route="/auth", on_load=AuthState.on_load_verify)
# app.add_page(create_document, route="/docs")
