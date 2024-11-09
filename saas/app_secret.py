from saas.rxext import SecretConfig

# ----
# demarcate keys that are empty and will cause silent issues with reflex deploy
_EMPTY = ""


class Secrets(SecretConfig):
    # keys without default values must be set in the environment
    stripe_secret_key: str = _EMPTY
    stripe_pub_key: str = _EMPTY

    # stripe webhook secret for verifying events
    stripe_webhook_secret: str = _EMPTY
    stripe_web_url: str = _EMPTY

    # for email sending
    resend_api_key: str = _EMPTY
    # for supabase
    supabase_url: str = _EMPTY
    supabase_key: str = _EMPTY

    # db info will change based on prod/test
    db_host: str = _EMPTY
    db_user: str = _EMPTY
    db_password: str = _EMPTY

    # keys with default values will be optionally overwritten
    # key for checking where the keys are coming from
    status_mode: str = "dev"
    db_type: str = "postgresql"
    loglevel: str = "default"


# # get from env or pass in with kwargs, returns dataclass instance
secrets = Secrets.setup()

