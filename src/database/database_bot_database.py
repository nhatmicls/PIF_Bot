import pymongo
from typing import *


class botDatabase:
    def __init__(self, url: str, database_name: str, collection_name: str) -> None:
        self.mongo_database = pymongo.MongoClient(url)
        self.member_PIF = self.mongo_database[database_name]
        self.discord_database = self.member_PIF[collection_name]
        self.uint_template = {
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
        return self.discord_database.count_documents({})

    async def add_new_people(
        self,
        name: str,
        birthday: str,
        mail: str,
        phone: str,
        university_id: str,
        PIFer_Cxx: str,
        PIFer_role: List[str],
        discord_id: str,
        discord_role: List[str],
    ):
        uint = self.uint_template
        uint["name"] = name
        uint["birthday"] = birthday
        uint["mail"] = mail
        uint["phone"] = phone
        uint["university_id"] = university_id
        uint["PIFer_Cxx"] = PIFer_Cxx
        uint["PIFer_role"] = PIFer_role
        uint["discord_id"] = discord_id
        uint["discord_role"] = discord_role

        self.discord_database.insert_one(uint)

    async def update_data_people(
        self,
        name: str,
        birthday: str,
        mail: str,
        phone: str,
        university_id: str,
        PIFer_Cxx: str,
        PIFer_role: List[str],
        discord_id: str,
        discord_role: List[str],
    ):
        data = self.discord_database.find_one({"discord_id": discord_id})

        if name != "":
            data["name"] = name

        if birthday != "":
            data["birthday"] = birthday

        if mail != "":
            data["mail"] = mail

        if phone != "":
            data["phone"] = phone

        if university_id != "":
            data["university_id"] = university_id

        if PIFer_Cxx != "":
            data["PIFer_Cxx"] = PIFer_Cxx

        if PIFer_role != [""]:
            data["PIFer_role"] = PIFer_role

        if discord_role != [""]:
            data["discord_role"] = discord_role

        self.discord_database.find_one_and_replace(
            {"discord_id": discord_id},
            data,
        )

    async def check_data_exist(self, key: str, value: str) -> bool:
        try:
            data = self.discord_database.find_one({key: value})
            if data != None:
                return True
            else:
                return False
        except:
            data = None

    async def find_with_filter(self, key: str, value: str) -> dict:
        try:
            data = self.discord_database.find({key: value})
            return data
        except:
            # data = None
            return None
