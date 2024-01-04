import sys
from pathlib import Path
from datetime import date

from typing import *

import json

import pymongo
from pymongo.cursor import Cursor
from bson import ObjectId

parent_dir_path = str(Path(__file__).resolve().parents[0])
sys.path.append(parent_dir_path + "/modules")

from verify_data import *


class botDatebaseTemplate:
    infrastructure_database_template = {
        "borrow_discord_id": "0",
        "borrowed_object_name": "1",
        "time_start_borrow": "2",
        "expected_return_time": "3",
        "image_borrow_path": "4",
        "image_return_path": "5",
        "status": "6",
    }
    member_database_template = {
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

    async def get_lastest_id(self):
        return self.member_database.count_documents({})

    """
    Utils section
    
    Function:
    - Check is data exist
    - Find data in database
    """

    async def check_data_exist(self, collector: Collection, data: dict) -> bool:
        try:
            data = collector.find_one(data)
            if data != None:
                return True
            else:
                return False
        except:
            data = None
            return False

    async def find_with_filter(self, collector: Collection, data: dict) -> Cursor:
        try:
            data = collector.find(data)
            return data
        except:
            return None

    async def auto_fill_missing_date(self, old_date: str) -> str:
        new_date = ""
        count = 0
        try:
            data = old_date.split("/")
            for x in data:
                if count < 2:
                    if len(x) < 2:
                        new_date = new_date + "0" + x
                    else:
                        new_date += x
                    new_date += "/"
                else:
                    new_date += x

                count += 1

            return new_date
        except Exception as e:
            print(e)

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
        uint = botDatebaseTemplate.member_database_template.copy()
        uint["name"] = name
        uint["birthday"] = await self.auto_fill_missing_date(old_date=birthday)
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
            data["birthday"] = await self.auto_fill_missing_date(old_date=birthday)

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

    async def borrow_infrastructure(
        self, discord_id: str, object_name: str, expected_return_time: str
    ) -> ObjectId:
        result = None
        today = date.today()

        await expected_return_day_verify(date=expected_return_time)

        data = botDatebaseTemplate.infrastructure_database_template.copy()

        data["borrow_discord_id"] = discord_id
        data["borrowed_object_name"] = object_name
        data["time_start_borrow"] = today.strftime("%d/%m/%Y")
        data["expected_return_time"] = expected_return_time
        data["image_borrow_path"] = "NA"
        data["image_return_path"] = "NA"
        data["status"] = "NA"

        result = self.infrastructure_database.insert_one(data).inserted_id
        return result

    async def update_infrastructure_status(self, borrow_id: ObjectId, status: str):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["status"] = status
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)

    async def update_image_borrow_path(
        self, borrow_id: ObjectId, image_borrow_path: str
    ):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["image_borrow_path"] = image_borrow_path
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)

    async def update_image_return_path(
        self, borrow_id: ObjectId, image_return_path: str
    ):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["image_borrow_path"] = image_return_path
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)

    async def borrow_infrastructure_status(self, borrow_id: ObjectId):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["status"] = "BORROWING"
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)

    async def borrow_review_infrastructure_status(self, borrow_id: ObjectId):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["status"] = "BORROWING - NEED REVIEW"
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)

    async def late_infrastructure_status(self, borrow_id: ObjectId):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["status"] = "LATE"
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)

    async def extend_infrastructure_status(self, borrow_id: ObjectId):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["status"] = "EXTEND"
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)

    async def return_infrastructure_status(self, borrow_id: ObjectId):
        data = self.infrastructure_database.find_one({"_id": borrow_id})
        data["status"] = "RETURNED"
        self.infrastructure_database.find_one_and_replace({"_id": borrow_id}, data)
