import logging

import discord
from discord.ext.commands import Cog, Bot
from discord import app_commands

from utils import *
from typing import *

from datetime import date, datetime

from infrastructure_exception_handle import *
from database_handler import botDatabase

from pymongo.cursor import Cursor
from bson.json_util import dumps


class botInfrastructureManagement(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase) -> None:
        super().__init__()

        self.bot = bot
        self.database_handle = database_handle

    async def infrastructure_borrow_embed(self) -> None:
        pass

    async def infrastructure_list_embed(
        self, discord_name: str, data: Cursor
    ) -> discord.Embed:
        embed = discord.Embed(
            title="Borrow list of " + discord_name,
            # description="Borrow list",
            color=discord.Color.random(),
        )

        embed.set_author(name="PIF Admin")
        embed.set_footer(text="Powered by Micls")

        for each_data in data:
            embed.add_field(name="Borrow ID", value=each_data["_id"], inline=True)
            embed.add_field(
                name="Borrowed item name",
                value=each_data["borrowed_object_name"],
                inline=True,
            )
            embed.add_field(
                name="Expected return day",
                value=each_data["expected_return_time"],
                inline=True,
            )

            # Embed line break
            embed.add_field(name="\u200B", value="\u200B", inline=False)

        return embed

    async def infrastructure_return(self) -> None:
        pass

    @app_commands.command(
        name="infrastructure_borrow", description="Register to borrow stuff"
    )
    @app_commands.describe(
        object_name="Item name",
        expected_return_time="Return day",
    )
    @app_commands.check(check_guild_id)
    async def infrastructure_borrow(
        self,
        interaction: discord.Interaction,
        object_name: str,
        expected_return_time: str,
    ) -> None:
        await interaction.response.defer()
        try:
            data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"borrow_discord_id": str(interaction.user.id)},
            )

            borrow_id = await self.database_handle.borrow_infrastructure(
                discord_id=str(interaction.user.id),
                object_name=object_name,
                expected_return_time=expected_return_time,
            )

            if len(list(data)) > 5:
                await self.database_handle.borrow_review_infrastructure_status(
                    borrow_id=borrow_id
                )

                await interaction.followup.send(
                    "You will able to borrow but it will be send to admin to review it",
                    ephemeral=False,
                )
            else:
                await self.database_handle.borrow_infrastructure_status(
                    borrow_id=borrow_id
                )

            await interaction.followup.send(
                "Your borrow ID is: " + json.loads(dumps(borrow_id))["$oid"],
                ephemeral=False,
            )

        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infrastructure_list", description="List stuff you are borrowing"
    )
    @app_commands.check(check_guild_id)
    async def infrastructure_list(
        self,
        interaction: discord.Interaction,
    ) -> None:
        try:
            data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"borrow_discord_id": str(interaction.user.id)},
            )

            discord_name = await self.database_handle.find_with_filter(
                self.database_handle.member_database,
                {"discord_id": str(interaction.user.id)},
            )

            if len(list(data)) == 0:
                await interaction.response.send_message(
                    "You are not borrowing any item from PIF LAB", ephemeral=True
                )
            else:
                return_embed = await self.infrastructure_list_embed(
                    discord_name[0]["name"], data.clone()
                )
                await interaction.response.send_message(
                    embed=return_embed, ephemeral=False
                )
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infrastructure_extend", description="List stuff you are borrowing"
    )
    @app_commands.check(check_guild_id)
    async def infrastructure_extend(
        self,
        interaction: discord.Interaction,
    ) -> None:
        try:
            data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"borrow_discord_id": str(interaction.user.id)},
            )
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
