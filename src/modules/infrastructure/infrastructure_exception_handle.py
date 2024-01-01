from typing import *


class memberNoPermission(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "You do not have the permission, please contact to admin or authority for more information"


class subcommandNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Subcommand is unavailable"


class idNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your discord ID you want to change info isn't exist in system, please contact to admin for more information"
