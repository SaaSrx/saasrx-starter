from dataclasses import dataclass

from reflex import config


@dataclass
class DownloadInfo:
    """
    A data class that holds information about a download.

    Attributes:
        filepath (str): The path where the file is to be downloaded.
        filename (str): The name of the file to be downloaded.
    """

    filepath: str
    filename: str


@dataclass
class ImageAssets:
    """
    A data class that holds information about image assets.

    Attributes:
        favicon (str): The path to the favicon.
        app_icon (str): The path to the app icon.
    """

    favicon: str
    app_icon: str


class Config(config.Config):
    """
    Config class that extends rx.Config.

    Properties:
        module (str): Returns the module path in dot notation if 'module_path' attribute exists,
            otherwise returns a string formed by joining 'app_name' with itself using a dot.
        reload_dirs (list[str]): Returns a list of directories to be reloaded. If 'reload_paths' attribute exists,
            it returns that list, otherwise it returns a list containing the first part of the module path.
    """

    @property
    def module(self) -> str:
        if hasattr(self, "module_path"):
            return self.module_path.replace("/", ".")
        return super().module

    @property
    def reload_dirs(self) -> list[str]:
        if hasattr(self, "reload_paths"):
            return self.reload_paths
        elif hasattr(self, "module_path"):
            return [self.module.split(".")[0]]
        else:
            return [self.app_name]
