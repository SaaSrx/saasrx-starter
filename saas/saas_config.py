# NOTE: only import from rxext here to avoid
from saas.rxext import Config

# ---- Fill in the following:
APP_NAME = "saas"  # this will be the folder containing the app
FORMATTED_APP_NAME = "SaaSrx"  # this will be the name displayed in the app


TAILWIND_CONFIG = {
    "theme": {
        "extend": {},
    },
    "plugins": [
        "@tailwindcss/typography",
    ],
}

config_kwargs = {
    "app_name": APP_NAME,
    "formated_app_name": FORMATTED_APP_NAME,
    # "tailwind": TAILWIND_CONFIG,
    # "loglevel": secrets.loglevel,
}


config = Config(**config_kwargs)
