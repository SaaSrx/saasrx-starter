from saas.rxext import Config, SecretConfig


class Secrets(SecretConfig):
    # keys without default values must be set in the environment
    stripe_secret_key: str
    stripe_pub_key: str

    # stripe webhook secret for verifying events
    stripe_webhook_secret: str

    # for email sending
    resend_api_key: str

    # db info will change based on prod/test
    db_host: str
    db_user: str
    db_password: str

    # keys with default values will be optionally overwritten
    # key for checking where the keys are coming from
    status_mode: str = "dev"
    db_type: str = "postgresql"
    loglevel: str = "default"


# get from env or pass in with kwargs, returns dataclass instance
secrets = Secrets.setup()


config = Config(
    app_name="saas",
    formated_app_name="SaaSrx",
    loglevel=secrets.loglevel,
    tailwind={},
)
