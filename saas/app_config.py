import reflex as rx

from saas.app_secret import secrets
from saas.rxext import Config, DownloadInfo
from saas.rxext.console import setup_log_level

# ---- Fill in the following:
application_name = "saas"  # this will be the folder containing the app
formatted_application_name = "SaaSrx"  # this will be the name displayed in the app
image_assets = {
    "favicon": "/favicon.ico",
    "app_icon": "/saasrx-icon.png",
}

# ---- Configure other settings related to theme/style
release_download = DownloadInfo(
    filepath="/releases/starter.zip",
    filename="saasrx.zip",
)

tailwind_config = {
    "theme": {
        "extend": {},
    },
    "plugins": [
        "@tailwindcss/typography",
    ],
}


config_kwargs = {
    "app_name": application_name,
    "formatted_application_name": formatted_application_name,
    "loglevel": "debug",
    "tailwind": tailwind_config,
    "db_url": secrets.db_url,
    # "loglevel": secrets.loglevel, # or LogLevel.DEBUG,
}


theme_config = {
    "appearance": "light",
    "radius": "large",
    "accent_color": "iris",
}
# config kwargs and possibly pop
setup_log_level(config_kwargs)
app_theme = rx.theme(**theme_config)
config: Config = Config(**config_kwargs)
