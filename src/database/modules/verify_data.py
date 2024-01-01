from typing import *
import re
from datetime import datetime

from verify_exception_handle import *

""" 
Name verify section
"""


async def name_verify(name: str) -> None:
    if any(char.isdigit() for char in name):
        raise nameContainNumber


""" 
Date verify section
"""


async def date_verify(date: str) -> bool:
    date_spliter = date.split("/")

    if len(date_spliter) != 3:
        return False

    date_of_month = int(date_spliter[0])
    month_of_year = int(date_spliter[1])

    if date_of_month > 31 or month_of_year > 12:
        return False

    return True


async def date_of_birth_verify(birthday: str) -> None:
    if not await date_verify(date=birthday):
        raise dateOfBirthFormatError

    date_spliter = birthday.split("/")
    year = int(date_spliter[2])

    if year < 1950:
        raise yearOfBirthTooHighError

    if year > datetime.now().year - 18:
        raise yearOfBirthTooLowError


async def expect_return_day_verify(date: str) -> None:
    if not await date_verify(date=date):
        raise dateOfExpectReturnDateFormatError

    date_spliter = date.split("/")
    year = int(date_spliter[2])

    if year < datetime.now().year:
        raise yearOfExpectReturnDateError


""" 
Email verify section
"""


async def email_verify(email: str) -> None:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not (re.fullmatch(regex, email)):
        raise emailFormatError


""" 
Phone verify section
"""


async def phone_verify(phone: str) -> None:
    if not phone.isnumeric():
        raise phoneFormatError


""" 
UID verify section
"""


async def UID_verify(UID: str) -> None:
    if UID == "":
        return

    if not UID.isnumeric():
        raise UIDFormatError
