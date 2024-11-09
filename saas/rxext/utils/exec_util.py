from functools import cache

from reflex.utils.exec import is_prod_mode as _is_prod_mode
from reflex.utils.exec import is_testing_env as _is_testing_env


@cache
def is_prod_mode():
    return _is_prod_mode()


@cache
def is_testing_env():
    return _is_testing_env()
