from reflex.utils.console import (
    LogLevel,
    debug,
    error,
    info,
    log,
    print,
    set_log_level,
    warn,
)


def app_log_level(log_level: str | LogLevel = None):
    """
    NOTE:
        - Setting the log level in the config is extremely verbose and WILL NOT print out for something like console.debug in an event handler,
        - Using set_log_level seems like its more aligned with what I want to do as it will print out console.debug in an event handler

    Sets the application log level.
    This function sets the log level for the application. The log level can be
    provided as a string or as a LogLevel enum. If a string is provided, it is
    converted to the corresponding LogLevel enum.
    Args:
        log_level (str | LogLevel, optional): The desired log level. It can be
        a string representing the log level (e.g., 'info', 'debug', 'error')
        or a LogLevel enum. If not provided, the default log level is used.
    Raises:
        KeyError: If the provided string does not correspond to a valid LogLevel.
    """

    if isinstance(log_level, str):
        log_level = LogLevel[log_level.upper()]

    set_log_level(log_level)


def setup_log_level(config_kwargs: dict):
    if log_level := config_kwargs.pop("loglevel", None):
        app_log_level(log_level)
    return config_kwargs


__all__ = [
    "LogLevel",
    "debug",
    "error",
    "info",
    "log",
    "print",
    "set_log_level",
    "setup_log_level",
    "warn",
]
