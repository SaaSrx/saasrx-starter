from functools import cache

from reflex.utils.exec import is_prod_mode as _is_prod_mode
from reflex.utils.exec import is_testing_env as _is_testing_env


@cache
def is_prod_mode() -> bool:
    """Check if running in production mode."""
    return _is_prod_mode()


@cache
def is_testing_env() -> bool:
    """Check if running in testing environment."""
    return _is_testing_env()


@cache
def get_environment_info() -> dict[str, bool]:
    """Get comprehensive environment information."""
    return {
        "production": is_prod_mode(),
        "testing": is_testing_env(),
        "development": not is_prod_mode() and not is_testing_env(),
    }
