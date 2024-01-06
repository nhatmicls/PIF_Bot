"""
Exception raised
"""


class noApiKey(Exception):
    """
    Exception raised when missing API key
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.args[0]} is missing API key"


class memberNoPermission(Exception):
    """
    Exception raised when member not have right permission
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "You do not have the permission"
