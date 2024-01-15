import logging

import discord
from discord.ext.commands import Cog, Bot
from discord import app_commands
from discord.ext.tasks import loop

from utils import *
from typing import *

from datetime import date, datetime, timezone, time, timedelta

from pymongo.cursor import Cursor
from bson.json_util import dumps
from bson import ObjectId

from infrastructure_exception_handle import *
from infrastructure_default_response import *

from verify_data import *
from format_data import *
from database_handler import botDatabase

utc = timezone.utc
infrastructure_task_time = time(
    hour=get_config_value(
        main_config="infrastructure_config", config="warning_check_hour_utc"
    ),
    minute=get_config_value(
        main_config="infrastructure_config", config="warning_check_minute_utc"
    ),
    tzinfo=utc,
)


class botInfrastructureManagement(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase) -> None:
        super().__init__()

        self.bot = bot
        self.database_handle = database_handle

    """
    Utils sector
    """

    async def replace_respond_via_dm(
        self,
        respond: str,
        name: str = "",
        item_name: str = "",
        expected_return_day: str = "",
        max_return_time: str = "",
    ) -> str:
        respond = respond.replace("<Name>", name)
        respond = respond.replace("<Item_name>", item_name)
        respond = respond.replace("<Expected_return_day>", expected_return_day)
        respond = respond.replace("<Max_return_time>", max_return_time)

        return respond

    async def check_user_id(self, discord_id: str) -> bool:
        data_verify = await self.database_handle.check_data_exist(
            self.database_handle.member_database,
            {"discord_id": str(discord_id)},
        )

        if not data_verify:
            raise idNotFound

    """
    Generator embed sector
    """

    async def infrastructure_borrow_embed(
        self, discord_name: str, data: list
    ) -> discord.Embed:
        embed = discord.Embed(
            title="Borrow register",
            color=discord.Color.random(),
        )

    async def infrastructure_borrow_review_embed(
        self, discord_name: str, data: list
    ) -> discord.Embed:
        embed = discord.Embed(
            title="Borrow register",
            color=discord.Color.random(),
        )

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
            embed.add_field(
                name="State",
                value=each_data["status"],
                inline=False,
            )

            # Embed line break
            embed.add_field(name="\u200B", value="\u200B", inline=False)
            sequence_embed.append(embed)

        return sequence_embed

    async def infrastructure_return(self) -> None:
        pass

    """
    API Discord sector
    """

    @app_commands.command(name="infra_borrow", description="Register to borrow stuff")
    @app_commands.describe(
        object_name="Item name",
        expected_return_time="Return day",
    )
    async def infrastructure_borrow(
        self,
        interaction: discord.Interaction,
        object_name: str,
        expected_return_time: str,
    ) -> None:
        """infrastructure_borrow Create borrow item register

        Create borrow item register

        Args:
            interaction (discord.Interaction): Discord interaction
            object_name (str): name of item
            expected_return_time (str): return date format DD/MM/YYYY
        """

        try:
            await self.check_user_id(discord_id=interaction.user.id)
            await expected_return_day_verify(date=expected_return_time)

            borrow_id = await self.database_handle.borrow_infrastructure(
                discord_id=str(interaction.user.id),
                object_name=object_name,
                expected_return_time=expected_return_time,
            )

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
            data = list(raw_data.clone()).copy()

            date_format = "%d/%m/%Y"
            timedelta = (
                datetime.strptime(expected_return_time, date_format).date()
                - datetime.today().date()
            )

            if (timedelta.days) > get_config_value(
                main_config="infrastructure_config", config="max_days_borrow_auto_deny"
            ):
                """
                Get response when borrow to long
                """

                await self.database_handle.deny_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )

                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.deny_expect_time_response,
                    ephemeral=True,
                )
            elif len(list(data)) >= get_config_value(
                main_config="infrastructure_config",
                config="max_item_borrow",
            ):
                """
                Get response when borrow too much
                """

                await self.database_handle.deny_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )

                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.deny_out_of_quota_response,
                    ephemeral=True,
                )
            elif (timedelta.days) > get_config_value(
                main_config="infrastructure_config",
                config="max_days_borrow_without_confirm",
            ):
                """
                Get response when borrow time longer than expect without confirm
                """

                await self.database_handle.borrow_review_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )

                respond_id = (
                    botInfrastructureManagementResponseDefault.borrow_response.replace(
                        "<ID>", json.loads(dumps(borrow_id))["$oid"]
                    )
                )
                respond_id = respond_id.replace("<days>", str(timedelta.days))

                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.review_for_long_time_borrow_response
                    + "\n"
                    + respond_id,
                    ephemeral=True,
                )

            else:
                """
                Get response when borrow success
                """

                await self.database_handle.borrow_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )

                respond_id = (
                    botInfrastructureManagementResponseDefault.borrow_response.replace(
                        "<ID>", json.loads(dumps(borrow_id))["$oid"]
                    )
                )
                respond_id = respond_id.replace("<days>", str(timedelta.days))

                await interaction.response.send_message(
                    respond_id,
                    ephemeral=True,
                )

                dm_content = await read_text_file(
                    get_config_value(
                        main_config="infrastructure_config",
                        config="borrow_infrastructure_response_path",
                    )
                )

                dm_content = await self.replace_respond_via_dm(
                    dm_content,
                    name=str(interaction.user.display_name),
                    item_name=object_name,
                    expected_return_day=expected_return_time,
                )

                await interaction.user.send(dm_content)
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(name="infra_list", description="List stuff you are borrowing")
    async def infrastructure_list(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """infrastructure_list Show borrow list

        Show borrow list return as embed

        Args:
            interaction (discord.Interaction): Discord Interaction
        """

        try:
            await self.check_user_id(discord_id=interaction.user.id)

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
                                    "RETURNED",
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
                    botInfrastructureManagementResponseDefault.no_borrow_item_response,
                    ephemeral=True,
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

    @app_commands.command(name="infra_extend", description="Extended return day")
    @app_commands.describe(borrow_id="Borrow ID", expected_return_time="Return day")
    async def infrastructure_extend(
        self,
        interaction: discord.Interaction,
        borrow_id: str,
        expected_return_time: str,
    ) -> None:
        """infrastructure_extend Extend borrow duration

        Make a request to delay return day

        Args:
            interaction (discord.Interaction): Discord Interaction
            borrow_id (str): Borrower ID
            expected_return_time (str): New expected return day
        """

        try:
            await self.check_user_id(discord_id=interaction.user.id)
            await expected_return_day_verify(date=expected_return_time)

            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {
                    "$and": [
                        {"borrower_discord_id": str(interaction.user.id)},
                        {"_id": ObjectId(borrow_id)},
                    ],
                },
            )

            data = list(raw_data.clone())

            if len(data) > 0:
                if data[0]["status"] == "EXTEND":
                    await interaction.response.send_message(
                        botInfrastructureManagementResponseDefault.deny_extend_expected_return_day_response,
                        ephemeral=True,
                    )
                    return

                date_format = "%d/%m/%Y"

                start_day = await self.database_handle.get_start_borrow_date(
                    borrow_id=ObjectId(borrow_id)
                )

                timedelta = (
                    datetime.strptime(expected_return_time, date_format).date()
                    - datetime.strptime(start_day, date_format).date()
                )

                if timedelta.days > get_config_value(
                    main_config="infrastructure_config",
                    config="max_days_borrow_auto_deny",
                ):
                    await interaction.response.send_message(
                        botInfrastructureManagementResponseDefault.deny_extend_long_expected_return_day_response,
                        ephemeral=True,
                    )
                else:
                    await self.database_handle.extend_infrastructure_status(
                        borrow_id=ObjectId(borrow_id),
                        expected_return_time=expected_return_time,
                    )
                    await interaction.response.send_message(
                        botInfrastructureManagementResponseDefault.extend_expected_return_day_response,
                        ephemeral=True,
                    )

                    dm_content = await read_text_file(
                        get_config_value(
                            main_config="infrastructure_config",
                            config="extend_infrastructure_response_path",
                        )
                    )

                    dm_content = await self.replace_respond_via_dm(
                        dm_content,
                        name=str(interaction.user.display_name),
                        item_name=data[0]["borrowed_object_name"],
                        expected_return_day=expected_return_time,
                    )

                    await interaction.user.send(dm_content)
            else:
                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.borrow_id_not_found_response,
                    ephemeral=True,
                )
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(name="infra_return", description="Register to return stuff")
    @app_commands.describe(borrow_id="Borrow ID")
    async def infrastructure_return(
        self, interaction: discord.Interaction, borrow_id: str
    ) -> None:
        """infrastructure_return Send return request

        Send return request

        Args:
            interaction (discord.Interaction): Discord Interaction
            borrow_id (str): borrow id
        """

        try:
            await self.check_user_id(discord_id=interaction.user.id)
            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {
                    "$and": [
                        {"borrower_discord_id": str(interaction.user.id)},
                        {"_id": ObjectId(borrow_id)},
                    ],
                },
            )

            data = list(raw_data.clone())

            if len(data) > 0:
                await self.database_handle.return_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )

                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.return_response,
                    ephemeral=True,
                )

                dm_content = await read_text_file(
                    get_config_value(
                        main_config="infrastructure_config",
                        config="return_infrastructure_response_path",
                    )
                )

                dm_content = await self.replace_respond_via_dm(
                    dm_content,
                    name=str(interaction.user.display_name),
                    item_name=data[0]["borrowed_object_name"],
                )

                await interaction.user.send(dm_content)
            else:
                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.borrow_id_not_found_response,
                    ephemeral=True,
                )

        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    """
    Admin sector
    """

    @app_commands.command(
        name="infra_admin_borrow",
        description="Command for admin to register to borrow stuff",
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        discord_id="Discord User ID who borrow item",
        object_name="Item name",
        expected_return_time="Return day",
    )
    async def infrastructure_admin_borrow(
        self,
        interaction: discord.Interaction,
        discord_id: discord.User,
        object_name: str,
        expected_return_time: str,
    ) -> None:
        """infrastructure_admin_borrow Create borrow item register bypass everything

        Create borrow item register

        Args:
            interaction (discord.Interaction): Discord interaction
            object_name (str): name of item
            expected_return_time (str): return date format DD/MM/YYYY
        """

        try:
            await self.check_user_id(discord_id=str(discord_id.id))
            await expected_return_day_verify(date=expected_return_time)

            borrow_id = await self.database_handle.borrow_infrastructure(
                discord_id=str(discord_id.id),
                object_name=object_name,
                expected_return_time=expected_return_time,
            )

            date_format = "%d/%m/%Y"
            timedelta = (
                datetime.strptime(expected_return_time, date_format).date()
                - datetime.today().date()
            )

            """
            Get response when borrow success
            """

            await self.database_handle.borrow_infrastructure_status(
                borrow_id=ObjectId(borrow_id)
            )

            respond_id = (
                botInfrastructureManagementResponseDefault.borrow_response.replace(
                    "<ID>", json.loads(dumps(borrow_id))["$oid"]
                )
            )
            respond_id = respond_id.replace("<days>", str(timedelta.days))

            await interaction.response.send_message(
                respond_id,
                ephemeral=True,
            )

            dm_content = await read_text_file(
                get_config_value(
                    main_config="infrastructure_config",
                    config="borrow_infrastructure_response_path",
                )
            )

            dm_content = await self.replace_respond_via_dm(
                dm_content,
                name=str(discord_id.display_name),
                item_name=object_name,
                expected_return_day=expected_return_time,
            )

            await discord_id.send(dm_content)

        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infra_admin_list",
        description="Command for admin to extract borrow list from someone",
    )
    @app_commands.describe(
        discord_id="Discord ID borrow item",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def infrastructure_admin_list(
        self, interaction: discord.Interaction, discord_id: discord.User
    ) -> None:
        """infrastructure_list Show borrow list

        Show borrow list return as embed

        Args:
            interaction (discord.Interaction): Discord Interaction
        """

        try:
            await self.check_user_id(discord_id=str(discord_id.id))

            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {
                    "$and": [
                        {"borrower_discord_id": str(discord_id.id)},
                        {
                            "status": {
                                "$in": [
                                    "BORROWING",
                                    "BORROWING - NEED REVIEW",
                                    "LATED",
                                    "EXTEND",
                                    "LOST",
                                    "RETURNED",
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
                    botInfrastructureManagementResponseDefault.no_borrow_item_response,
                    ephemeral=True,
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
        name="infra_admin_extend",
        description="Command for admin to extend returned day for someone",
    )
    @app_commands.describe(
        borrow_id="Borrow ID",
        expected_return_time="Return day",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def infrastructure_admin_extend(
        self,
        interaction: discord.Interaction,
        borrow_id: str,
        expected_return_time: str,
    ) -> None:
        """infrastructure_admin_extend Command for extend borrow

        Command for extend borrow

        Args:
            interaction (discord.Interaction): _description_
            borrow_id (str): Borrow ID
            expected_return_time (str): expected return time
        """

        try:
            await self.check_user_id(discord_id=interaction.user.id)
            await expected_return_day_verify(date=expected_return_time)

            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"_id": ObjectId(borrow_id)},
            )

            data = list(raw_data.clone())

            if len(data) > 0:
                await self.database_handle.extend_infrastructure_status(
                    borrow_id=ObjectId(borrow_id),
                    expected_return_time=expected_return_time,
                )

                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.extend_expected_return_day_response,
                    ephemeral=True,
                )

                discord_id = await self.bot.fetch_user(
                    int(data[0]["borrower_discord_id"])
                )

                dm_content = await read_text_file(
                    get_config_value(
                        main_config="infrastructure_config",
                        config="extend_infrastructure_response_path",
                    )
                )

                dm_content = await self.replace_respond_via_dm(
                    dm_content,
                    name=discord_id.display_name,
                    item_name=data[0]["borrowed_object_name"],
                    expected_return_day=expected_return_time,
                )

                await discord_id.send(dm_content)
            else:
                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.borrow_id_not_found_response,
                    ephemeral=True,
                )
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infra_borrow_admin_affirm",
        description="Command for admin to confirm item is borrowed",
    )
    @app_commands.describe(borrow_id="Borrow ID")
    @app_commands.checks.has_permissions(administrator=True)
    async def infrastructure_borrow_admin_affirm(
        self, interaction: discord.Interaction, borrow_id: str
    ) -> None:
        try:
            await self.check_user_id(discord_id=interaction.user.id)

            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"_id": ObjectId(borrow_id)},
            )

            data = list(raw_data.clone())

            if len(data) > 0:
                await self.database_handle.borrow_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )

                respond_id = botInfrastructureManagementAdminResponseDefault.borrow_admin_affirm_response.replace(
                    "<ID>", borrow_id
                )

                await interaction.response.send_message(
                    respond_id,
                    ephemeral=True,
                )

                discord_id = await self.bot.fetch_user(
                    int(data[0]["borrower_discord_id"])
                )

                dm_content = await read_text_file(
                    get_config_value(
                        main_config="infrastructure_config",
                        config="borrow_infrastructure_response_path",
                    )
                )

                dm_content = await self.replace_respond_via_dm(
                    dm_content,
                    name=str(discord_id.display_name),
                    item_name=data[0]["borrowed_object_name"],
                    expected_return_day=data[0]["expected_return_time"],
                )

                await discord_id.send(dm_content)
            else:
                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.borrow_id_not_found_response,
                    ephemeral=True,
                )
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infra_borrow_admin_deny",
        description="Command for admin to deny this borrow",
    )
    @app_commands.describe(borrow_id="Borrow ID")
    @app_commands.checks.has_permissions(administrator=True)
    async def infrastructure_borrow_admin_deny(
        self, interaction: discord.Interaction, borrow_id: str
    ) -> None:
        try:
            await self.check_user_id(discord_id=interaction.user.id)

            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"_id": ObjectId(borrow_id)},
            )

            data = list(raw_data.clone())

            if len(data) > 0:
                await self.database_handle.late_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )

                respond_id = botInfrastructureManagementAdminResponseDefault.borrow_admin_deny_response.replace(
                    "<ID>", borrow_id
                )

                await interaction.response.send_message(
                    respond_id,
                    ephemeral=True,
                )

                discord_id = await self.bot.fetch_user(
                    int(data[0]["borrower_discord_id"])
                )

                dm_content = await read_text_file(
                    get_config_value(
                        main_config="infrastructure_config",
                        config="infrastructure_borrow_admin_deny_response_path",
                    )
                )

                dm_content = await self.replace_respond_via_dm(
                    dm_content,
                    name=discord_id.display_name,
                    item_name=data[0]["borrowed_object_name"],
                    max_return_time=get_config_value(
                        main_config="infrastructure_config", config="max_return_days"
                    ),
                )

                await discord_id.send(dm_content)
            else:
                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.borrow_id_not_found_response,
                    ephemeral=True,
                )
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infra_return_admin_affirm",
        description="Command for admin to confirm item is returned",
    )
    @app_commands.describe(borrow_id="Borrow ID")
    @app_commands.checks.has_permissions(administrator=True)
    async def infrastructure_return_admin_affirm(
        self, interaction: discord.Interaction, borrow_id: str
    ) -> None:
        try:
            await self.check_user_id(discord_id=interaction.user.id)

            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"_id": ObjectId(borrow_id)},
            )

            data = list(raw_data.clone())

            if len(data) > 0:
                await self.database_handle.confirm_return_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )
                respond_id = botInfrastructureManagementAdminResponseDefault.return_admin_affirm_response.replace(
                    "<ID>", borrow_id
                )

                await interaction.response.send_message(
                    respond_id,
                    ephemeral=True,
                )

                discord_id = await self.bot.fetch_user(
                    int(data[0]["borrower_discord_id"])
                )

                dm_content = await read_text_file(
                    get_config_value(
                        main_config="infrastructure_config",
                        config="return_confirm_infrastructure_response_path",
                    )
                )

                dm_content = await self.replace_respond_via_dm(
                    dm_content,
                    name=discord_id.display_name,
                    item_name=data[0]["borrowed_object_name"],
                )

                await discord_id.send(dm_content)
            else:
                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.borrow_id_not_found_response,
                    ephemeral=True,
                )
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="infra_return_admin_fail",
        description="Command for admin to confirm item is returned",
    )
    @app_commands.describe(borrow_id="Borrow ID")
    @app_commands.checks.has_permissions(administrator=True)
    async def infrastructure_return_admin_fail(
        self, interaction: discord.Interaction, borrow_id: str
    ) -> None:
        try:
            await self.check_user_id(discord_id=interaction.user.id)

            raw_data = await self.database_handle.find_with_filter(
                self.database_handle.infrastructure_database,
                {"_id": ObjectId(borrow_id)},
            )

            data = list(raw_data.clone())

            if len(data) > 0:
                await self.database_handle.lost_infrastructure_status(
                    borrow_id=ObjectId(borrow_id)
                )
                respond_id = botInfrastructureManagementAdminResponseDefault.return_admin_not_found_response.replace(
                    "<ID>", borrow_id
                )

                await interaction.response.send_message(
                    respond_id,
                    ephemeral=True,
                )

                discord_id = await self.bot.fetch_user(
                    int(data[0]["borrower_discord_id"])
                )

                dm_content = await read_text_file(
                    get_config_value(
                        main_config="infrastructure_config",
                        config="infrastructure_return_admin_fail_response_path",
                    )
                )

                dm_content = await self.replace_respond_via_dm(
                    dm_content,
                    name=discord_id.display_name,
                    item_name=data[0]["borrowed_object_name"],
                )

                await discord_id.send(dm_content)
            else:
                await interaction.response.send_message(
                    botInfrastructureManagementResponseDefault.borrow_id_not_found_response,
                    ephemeral=True,
                )
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    """
    Error handle
    """

    @infrastructure_admin_borrow.error
    @infrastructure_admin_list.error
    @infrastructure_admin_extend.error
    @infrastructure_borrow_admin_affirm.error
    @infrastructure_borrow_admin_deny.error
    @infrastructure_return_admin_affirm.error
    @infrastructure_return_admin_fail.error
    async def error_admin_response(
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

    """
    Infrastructure task
    """

    @loop(time=infrastructure_task_time)
    async def infrastructure_warning_return_task(self):
        today: date = datetime.date.today() + datetime.timedelta(
            days=get_config_value(
                main_config="infrastructure_config",
                config="warning_return_day_before_days",
            )
        )
        search_topic = today.strftime("%d/%m/%Y")
        search_request = {"$regex": search_topic}
        search_result = await self.database_handle.find_with_filter(
            self.database_handle.infrastructure_database,
            {
                "$and": [
                    {"expected_return_time": search_request},
                    {
                        "status": {
                            "$in": [
                                "LATED",
                                "LOST",
                            ]
                        }
                    },
                ],
            },
        )

        if len(list(search_result.clone())) > 0:
            for cursor in search_result:
                if cursor["status"] == "LATED":
                    response_msg = await read_text_file(
                        get_config_value(
                            main_config="infrastructure_config",
                            config="borrow_infrastructure_response_path",
                        )
                    )
                elif cursor["status"] == "LOST":
                    response_msg = await read_text_file(
                        get_config_value(
                            main_config="infrastructure_config",
                            config="lost_infrastructure_response_path",
                        )
                    )

    @infrastructure_warning_return_task.before_loop
    async def infrastructure_warning_return_task_before(self):
        await self.bot.wait_until_ready()

    """
    Test section
    """

    @app_commands.command(
        name="infra_admin_test",
        description="Command for admin to test function",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def infrastructure_admin_test(self, interaction: discord.Interaction) -> None:
        await self.infrastructure_warning_return_task()
        # pass
