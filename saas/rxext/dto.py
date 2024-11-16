from dataclasses import dataclass
from enum import StrEnum, auto


class MenuType(StrEnum):
    LINK = auto()  # "link"
    BUTTON = auto()  # "button"


@dataclass
class MenuItem:
    text: str
    link: str
    typeof: MenuType


@dataclass
class MenuLink(MenuItem):
    typeof: MenuType = MenuType.LINK


@dataclass
class MenuButton(MenuItem):
    typeof: MenuType = MenuType.BUTTON
