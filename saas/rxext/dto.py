from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Literal, TypeAlias

MenuTypeLiteral: TypeAlias = Literal["link", "button"]


class MenuType(StrEnum):
    LINK = auto()  # "link"
    BUTTON = auto()  # "button"


@dataclass
class MenuItem:
    text: str
    link: str
    typeof: MenuTypeLiteral | MenuType


@dataclass
class MenuLink(MenuItem):
    typeof: MenuTypeLiteral = MenuType.LINK


@dataclass
class MenuButton(MenuItem):
    typeof: MenuTypeLiteral = MenuType.BUTTON
