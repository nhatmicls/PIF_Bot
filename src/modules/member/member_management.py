from utils import *
from typing import *
from datetime import date, datetime
import logging

import discord
from discord.ext.commands import Cog, Bot
from discord import app_commands


from member_exception_handler import *
from database_handler import botDatabase


class botMemberManagement(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase) -> None:
        super().__init__()

        self.bot = bot
        self.database_handle = database_handle

    async def role_filter(self, interaction: discord.Interaction):
        discord_role = []
        PIFer_role = []

        for role_list in interaction.user.roles:
            discord_role.append(str(role_list))

            if str(role_list) in list(
                get_config_value(main_config="discord_config", config="admin_role")
            ):
                PIFer_role.append("admin")

            if str(role_list) in list(
                get_config_value(main_config="discord_config", config="accountant_role")
            ):
                PIFer_role.append("accountant")

            if str(role_list) in list(
                get_config_value(main_config="discord_config", config="mod_role")
            ):
                PIFer_role.append("mod")

        return discord_role, PIFer_role

    @app_commands.command(name="sign_up", description="Sign up your self to PIF bot")
    @app_commands.describe(
        name="Your name",
        birthday="Your birthday",
        mail="Your email address",
        phone="Your phone number",
        university_id="Your university ID (input if you from HCMUT)",
    )
    @app_commands.checks.has_any_role("PIFer")
    @app_commands.check(check_guild_id)
    async def sign_up_new_member(
        self,
        interaction: discord.Interaction,
        name: str,
        birthday: str,
        mail: str,
        phone: str,
        university_id: str = "",
    ):
        try:
            data_verify = await self.database_handle.check_data_exist(
                self.database_handle.member_database,
                {"discord_id": str(interaction.user.id)},
            )

            if data_verify == True:
                raise idAlreadySignUp

            discord_role, PIFer_role = await self.role_filter(interaction=interaction)

            await self.database_handle.add_new_people(
                name=name,
                birthday=birthday,
                email=mail,
                phone=phone,
                university_id=university_id,
                PIFer_Cxx="",
                PIFer_role=PIFer_role,
                discord_id=str(interaction.user.id),
                discord_role=discord_role,
            )
            await interaction.response.send_message("Complete sign in", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="change_data", description="Change data of member in PIF server"
    )
    @app_commands.describe(
        discord_id="Mention the user you want to change infomation",
        name="Name you want to change to",
        birthday="Birthday you want to change to",
        mail="Email address you want to change to",
        phone="Phone number you want to change to",
        university_id="University ID you want to change to",
        pifer_cxx="Course of C joining to PIF you want to change to",
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.check(check_guild_id)
    async def change_member_info(
        self,
        interaction: discord.Interaction,
        discord_id: str,
        name: str = "",
        birthday: str = "",
        mail: str = "",
        phone: str = "",
        university_id: str = "",
        pifer_cxx: str = "",
    ):
        try:
            discord_id_database = discord_id[2 : len(discord_id) - 1]

            data_verify = await self.database_handle.check_data_exist(
                self.database_handle.member_database,
                {"discord_id": discord_id_database},
            )

            if data_verify == False:
                raise idNotFound

            discord_role, PIFer_role = await self.role_filter(interaction=interaction)

            await self.database_handle.update_data_people(
                name=name,
                birthday=birthday,
                email=mail,
                phone=phone,
                university_id=university_id,
                PIFer_Cxx=pifer_cxx,
                PIFer_role=PIFer_role,
                discord_id=discord_id_database,
                discord_role=discord_role,
            )

            await interaction.response.send_message("Change completed", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @sign_up_new_member.error
    @change_member_info.error
    async def error_respone(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        try:
            if isinstance(
                error, (app_commands.MissingPermissions, app_commands.MissingAnyRole)
            ):
                await interaction.response.send_message(
                    memberNoPermission.__str__(self=self), ephemeral=True
                )
                raise memberNoPermission
        except Exception as e:
            print(e)
