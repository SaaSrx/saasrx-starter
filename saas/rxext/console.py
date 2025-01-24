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


def setup_log_level(config_kwargs: dict, keep_with_config: bool = False) -> dict:
    if log_level := config_kwargs.pop("loglevel", None):
        app_log_level(log_level)

        if keep_with_config:
            config_kwargs["loglevel"] = log_level

    return config_kwargs


# def app_log_level(log_level: Optional[Union[str, LogLevel]] = None) -> None:
#     """Set the application log level with proper validation.

#     This function sets the global log level for the application. It handles both string
#     and LogLevel enum inputs, with proper validation and error handling.

#     Args:
#         log_level: The desired log level. Can be either:
#             - A string (case-insensitive) matching LogLevel enum values
#             - A LogLevel enum value
#             - None to keep the current log level

#     Raises:
#         ValueError: If the provided string is not a valid log level
#         TypeError: If the provided log_level is neither string, LogLevel, nor None

#     Examples:
#         >>> app_log_level("debug")  # Set to debug level
#         >>> app_log_level(LogLevel.INFO)  # Set to info level
#         >>> app_log_level()  # Keep current level
#     """
#     if log_level is None:
#         return

#     if isinstance(log_level, str):
#         try:
#             log_level = LogLevel[log_level.upper()]
#         except KeyError:
#             valid_levels = ", ".join(level.name.lower() for level in LogLevel)
#             raise ValueError(
#                 f"Invalid log level: '{log_level}'. Valid levels are: {valid_levels}"
#             )
#     elif not isinstance(log_level, LogLevel):
#         raise TypeError(
#             f"Log level must be a string or LogLevel enum, got {type(log_level).__name__}"
#         )

#     set_log_level(log_level)


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
