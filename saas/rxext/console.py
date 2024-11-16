from typing import Any, Dict, Optional, Union

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


def app_log_level(log_level: Optional[Union[str, LogLevel]] = None) -> None:
    """Set the application log level with proper validation.

    This function sets the global log level for the application. It handles both string
    and LogLevel enum inputs, with proper validation and error handling.

    Args:
        log_level: The desired log level. Can be either:
            - A string (case-insensitive) matching LogLevel enum values
            - A LogLevel enum value
            - None to keep the current log level

    Raises:
        ValueError: If the provided string is not a valid log level
        TypeError: If the provided log_level is neither string, LogLevel, nor None

    Examples:
        >>> app_log_level("debug")  # Set to debug level
        >>> app_log_level(LogLevel.INFO)  # Set to info level
        >>> app_log_level()  # Keep current level
    """
    if log_level is None:
        return

    if isinstance(log_level, str):
        try:
            log_level = LogLevel[log_level.upper()]
        except KeyError:
            valid_levels = ", ".join(level.name.lower() for level in LogLevel)
            raise ValueError(f"Invalid log level: '{log_level}'. Valid levels are: {valid_levels}")
    elif not isinstance(log_level, LogLevel):
        raise TypeError(f"Log level must be a string or LogLevel enum, got {type(log_level).__name__}")

    set_log_level(log_level)


def setup_log_level(config_kwargs: Dict[str, Any], keep_with_config: bool = False) -> Dict[str, Any]:
    """Configure application log level from config kwargs.

    This function processes log level configuration from the provided config dictionary.
    It can optionally preserve or remove the log level setting from the config.

    Args:
        config_kwargs: Configuration dictionary that may contain a 'loglevel' key
        keep_with_config: If True, preserves the loglevel in config_kwargs;
                         if False, removes it after processing

    Returns:
        Dict[str, Any]: Modified configuration dictionary

    Examples:
        >>> config = {"loglevel": "debug", "other_setting": True}
        >>> setup_log_level(config)  # Removes loglevel after setting it
        {'other_setting': True}
        >>> setup_log_level(config, keep_with_config=True)  # Keeps loglevel in config
        {'loglevel': 'debug', 'other_setting': True}
    """
    config_kwargs = config_kwargs.copy()  # Create a copy to avoid modifying the original

    if log_level := config_kwargs.get("loglevel"):
        try:
            app_log_level(log_level)
            if not keep_with_config:
                config_kwargs.pop("loglevel")
        except (ValueError, TypeError) as e:
            warn(f"Invalid log level configuration: {e}")
            config_kwargs.pop("loglevel", None)  # Remove invalid setting

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
