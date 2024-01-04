from typing import *


class nameContainNumber(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your name contain number."


class yearOfBirthTooLowError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "You should be 18+ to sign up this."


class yearOfBirthTooHighError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Why you so old to sign up this."


class dateOfBirthFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your date of birth have wrong format, format should be DD/MM/YYYY."


class emailFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your email have wrong format."


class phoneFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your phone number have wrong format."


class UIDFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your university have wrong format."


class yearOfExpectedReturnDateError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "You should return this in future not the past."


class dateOfExpectedReturnDateFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return (
            "Your expected return time have wrong format, format should be DD/MM/YYYY."
        )
