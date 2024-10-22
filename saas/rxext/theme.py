from typing import Optional

import tomllib
from pydantic import BaseModel


class ThemeConfig(BaseModel):
    accent_color: str = None  #  "blue"
    appearance: str = "inherit"
    gray_color: str = "gray"
    has_background: bool = False
    radius: str = "large"
    scaling: str = "100%"

    @classmethod
    def from_file(cls, file_path: Optional[str] = None):
        # Usage example:
        # theme = ThemeDefaults.from_file('/path/to/your/file.toml')
        # If the file is not found or invalid, it will use the default values.
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    data = tomllib.load(file)
                return cls(**data)
            except (FileNotFoundError, tomllib.TOMLDecodeError):
                pass
        return cls()
