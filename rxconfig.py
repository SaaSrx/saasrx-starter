from saas.rxext import Config
from saas.saas_secrets import config_kwargs

# get config from config_kwargs to allow hot reloading
config = Config(**config_kwargs)
