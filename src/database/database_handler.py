import sys
from pathlib import Path

from typing import *

import pymongo

parent_dir_path = str(Path(__file__).resolve().parents[0])
sys.path.append(parent_dir_path + "/modules")

from verify_data import *


class botDatabase:
    def __init__(
        self,
        url: str,
        database_name: str,
        member_database_name: str,
        infrastructure_database_name: str,
    ) -> None:
        self.mongo_database = pymongo.MongoClient(url)
        self.PIF_database = self.mongo_database[database_name]
        self.member_database = self.PIF_database[member_database_name]
        self.infrastructure_database = self.PIF_database[infrastructure_database_name]

        self.infrastructure_database_template = {
            "borrow_object_name": "1",
            "borrower_id": "2",
            "time_start_borrow": "3",
            "expect_return_time": "4",
            "image_borrow_path": "5",
            "image_return_path": "5",
            "status": "5",
        }
        self.member_database_template = {
            "name": "1",
            "birthday": "2",
            "mail": "3",
            "phone": "4",
            "university_id": "5",
            "PIFer_Cxx": "6",
            "PIFer_role": "7",
            "discord_id": "8",
            "discord_role": "9",
        }

    async def get_lastest_id(self):
        return self.member_database.count_documents({})

    """
    Member manager section
    
    Function:
    - Add
    - Update
    """

    async def add_new_people(
        self,
        name: str,
        birthday: str,
        email: str,
        phone: str,
        university_id: str,
        PIFer_Cxx: str,
        PIFer_role: List[str],
        discord_id: str,
        discord_role: List[str],
    ):
        # verify data
        await name_verify(name=name)
        await date_of_birth_verify(birthday=birthday)
        await email_verify(email=email)
        await phone_verify(phone=phone)
        await UID_verify(UID=university_id)

        # import data
        uint = self.member_database_template
        uint["name"] = name
        uint["birthday"] = birthday
        uint["mail"] = email
        uint["phone"] = phone
        uint["university_id"] = university_id
        uint["PIFer_Cxx"] = PIFer_Cxx
        uint["PIFer_role"] = PIFer_role
        uint["discord_id"] = discord_id
        uint["discord_role"] = discord_role

        # import data to database
        self.member_database.insert_one(uint)

    async def update_data_people(
        self,
        name: str,
        birthday: str,
        email: str,
        phone: str,
        university_id: str,
        PIFer_Cxx: str,
        PIFer_role: List[str],
        discord_id: str,
        discord_role: List[str],
    ):
        data = self.member_database.find_one({"discord_id": discord_id})

        if name != "":
            await name_verify(name=name)
            data["name"] = name

        if birthday != "":
            await date_of_birth_verify(birthday=birthday)
            data["birthday"] = birthday

        if email != "":
            await email_verify(email=email)
            data["mail"] = email

        if phone != "":
            await phone_verify(phone=phone)
            data["phone"] = phone

        if university_id != "":
            await UID_verify(UID=university_id)
            data["university_id"] = university_id

        if PIFer_Cxx != "":
            data["PIFer_Cxx"] = PIFer_Cxx

        if PIFer_role != [""]:
            data["PIFer_role"] = PIFer_role

        if discord_role != [""]:
            data["discord_role"] = discord_role

        self.member_database.find_one_and_replace(
            {"discord_id": discord_id},
            data,
        )

    """
    Infrastructure manager section
    
    Function:
    - Init borrow data
    - Update path
    - Update status
    """

    async def check_data_exist(self, key: str, value: str) -> bool:
        try:
            data = self.member_database.find_one({key: value})
            if data != None:
                return True
            else:
                return False
        except:
            data = None

    async def find_with_filter(self, key: str, value: str) -> dict:
        try:
            data = self.member_database.find({key: value})
            return data
        except:
            return None
