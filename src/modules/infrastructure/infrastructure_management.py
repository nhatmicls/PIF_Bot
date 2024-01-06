import logging

import discord
from discord.ext.commands import Cog, Bot
from discord import app_commands

from utils import *
from typing import *

from datetime import date, datetime

from verify_data import *
from format_data import *
from infrastructure_exception_handle import *
from database_handler import botDatabase

from pymongo.cursor import Cursor
from bson.json_util import dumps


class botInfrastructureManagementRespondDefault:
    deny_expect_time_respone = (
        "You unable to borrow.\n"
        "Your expected return date EXCEEDED the maximum item borrowing duration.\n"
        "Please contact DIRECT to authority for borrow this item."
    )
    deny_out_of_quota_respone = (
        "You unable to borrow.\n"
        "Your borrow item quota is reach.\n"
        "Please contact DIRECT to authority for borrow any more item."
    )

    review_for_long_time_borrow_respone = (
        "You able to borrow.\n"
        "Your expected return date EXCEEDED the maximum item borrowing duration without need permission.\n"
        "But it will notice to our authority."
    )

    borrow_respone = "Your borrow ID is: <ID>\n" "Your remaining days is: <days>"


class botInfrastructureManagement(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase) -> None:
        super().__init__()

        self.bot = bot
        self.database_handle = database_handle

    async def infrastructure_borrow_embed(self) -> None:
        pass

    async def infrastructure_borrow_review_embed(self) -> None:
        pass

    async def infrastructure_list_embed(
        self, discord_name: str, data: list
    ) -> Sequence[discord.Embed]:
        sequence_embed: Sequence[discord.Embed] = []

        for each_data in data:
            embed = discord.Embed(
                title="Borrow list of " + discord_name,
                # description="Borrow list",
                color=discord.Color.random(),
            )

            embed.set_author(name="PIF Admin")
            embed.set_footer(text="Powered by Micls")

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
            sequence_embed.append(embed)

        return sequence_embed

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
        try:
            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {
                    "$and": [
                        {"borrower_discord_id": str(interaction.user.id)},
                        {
                            "status": {
                                "$in": [
                                    "BORROWING",
                                    "BORROWING - NEED REVIEW",
                                    "LATED",
                                    "EXTEND",
                                    "LOST",
                                ]
                            }
                        },
                    ],
                },
            )

            await expected_return_day_verify(date=expected_return_time)

            date_format = "%d/%m/%Y"
            timedelta = (
                datetime.strptime(expected_return_time, date_format).date()
                - datetime.today().date()
            )

            borrow_id = await self.database_handle.borrow_infrastructure(
                discord_id=str(interaction.user.id),
                object_name=object_name,
                expected_return_time=expected_return_time,
            )

            data = list(raw_data.clone()).copy()

            if (timedelta.days) > get_config_value(
                main_config="infrastructure_config", config="max_days_borrow_auto_deny"
            ):
                """
                Get respone when borrow to long
                """

                await self.database_handle.deny_infrastructure_status(
                    borrow_id=borrow_id
                )

                await interaction.response.send_message(
                    botInfrastructureManagementRespondDefault.deny_expect_time_respone,
                    ephemeral=True,
                )
            elif len(list(data)) > get_config_value(
                main_config="infrastructure_config",
                config="max_item_borrow",
            ):
                """
                Get respone when borrow too much
                """

                await self.database_handle.deny_infrastructure_status(
                    borrow_id=borrow_id
                )

                await interaction.response.send_message(
                    botInfrastructureManagementRespondDefault.deny_out_of_quota_respone,
                    ephemeral=True,
                )
            elif (timedelta.days) > get_config_value(
                main_config="infrastructure_config",
                config="max_days_borrow_without_confirm",
            ):
                """
                Get respone when borrow time longer than expect without confirm
                """

                await self.database_handle.borrow_review_infrastructure_status(
                    borrow_id=borrow_id
                )

                respond_id = (
                    botInfrastructureManagementRespondDefault.borrow_respone.replace(
                        "<ID>", json.loads(dumps(borrow_id))["$oid"]
                    )
                )
                respond_id = respond_id.replace("<days>", str(timedelta.days))

                await interaction.response.send_message(
                    botInfrastructureManagementRespondDefault.review_for_long_time_borrow_respone
                    + "\n"
                    + respond_id,
                    ephemeral=True,
                )

            else:
                """
                Get respone when borrow success
                """

                await self.database_handle.borrow_infrastructure_status(
                    borrow_id=borrow_id
                )

                respond_id = (
                    botInfrastructureManagementRespondDefault.borrow_respone.replace(
                        "<ID>", json.loads(dumps(borrow_id))["$oid"]
                    )
                )
                respond_id = respond_id.replace("<days>", str(timedelta.days))

                await interaction.response.send_message(
                    respond_id,
                    ephemeral=True,
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
            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {
                    "$and": [
                        {"borrower_discord_id": str(interaction.user.id)},
                        {
                            "status": {
                                "$in": [
                                    "BORROWING",
                                    "BORROWING - NEED REVIEW",
                                    "LATED",
                                    "EXTEND",
                                    "LOST",
                                ]
                            }
                        },
                    ],
                },
            )

            discord_name = await self.database_handle.find_with_filter(
                self.database_handle.member_database,
                {"discord_id": str(interaction.user.id)},
            )

            data = list(raw_data.clone())

            if len(data) == 0:
                await interaction.response.send_message(
                    "You are not borrowing any item from PIF LAB", ephemeral=True
                )
            else:
                return_embed = await self.infrastructure_list_embed(
                    discord_name[0]["name"], data.copy()
                )
                await interaction.response.send_message(
                    embeds=return_embed, ephemeral=True
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
                {"borrower_discord_id": str(interaction.user.id)},
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
