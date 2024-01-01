import logging

import discord
from discord.ext.commands import Cog, Bot
from discord import app_commands

from utils import *
from typing import *

from datetime import date, datetime

from infrastructure_exception_handle import *
from database_handler import botDatabase


class botInfrastructureManagement(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase) -> None:
        super().__init__()

        self.bot = bot
        self.database_handle = database_handle

    async def infrastructure_borrow(self) -> None:
        pass

    async def infrastructure_return(self) -> None:
        pass

    @app_commands.command(
        name="infrastructure_borrow", description="Register to borrow stuff"
    )
    @app_commands.check(check_guild_id)
    async def infrastructure_borrow(
        self,
        interaction: discord.Interaction,
        object_name: str,
        expect_return_time: str,
    ) -> None:
        try:
            pass
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infrastructure_return", description="Register to return stuff"
    )
    @app_commands.check(check_guild_id)
    async def infrastructure_return(
        self,
        interaction: discord.Interaction,
    ) -> None:
        try:
            pass
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infrastructure_admin",
        description="Infrastructure command using for admin",
    )
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="remove", value="remove"),
            app_commands.Choice(name="add", value="add"),
        ]
    )
    @app_commands.check(check_guild_id)
    async def infrastructure_admin(
        self, interaction: discord.Interaction, choices: app_commands.Choice[str]
    ) -> None:
        if choices.value == "remove":
            pass
        elif choices.value == "add":
            pass
        else:
            await interaction.response.send_message(
                "Subcommand not found", ephemeral=False
            )
