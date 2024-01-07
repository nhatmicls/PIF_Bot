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
        return (
            "Your Discord ID is not yet registered on this server.\n"
            "Kindly complete the registration process to access this feature."
        )
