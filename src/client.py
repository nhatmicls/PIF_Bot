import asyncio
import json
import os
import sys
from pathlib import Path

import discord
from discord.ext.commands import Bot

from utils import *
from typing import *


parent_dir_path = str(Path(__file__).resolve().parents[1])
sys.path.append(parent_dir_path + "/src")
sys.path.append(parent_dir_path + "/src/modules/chat")
sys.path.append(parent_dir_path + "/src/modules/command")
sys.path.append(parent_dir_path + "/src/modules/event")
sys.path.append(parent_dir_path + "/src/modules/member")
sys.path.append(parent_dir_path + "/src/modules/infrastructure")
sys.path.append(parent_dir_path + "/src/database")
sys.path.append(parent_dir_path + "/src/handler")

sys.path.append(parent_dir_path + "/lib/data_verify")
sys.path.append(parent_dir_path + "/lib/data_format")

from member_management import botMemberManagement
from infrastructure_management import botInfrastructureManagement
from database_handler import botDatabase
from command import botCommands
from chat import botChatGPT

from handler_task_handle import botTasks
from handler_event_handle import botEvents

from utils import *

GUILD_ID = discord.Object(
    id=get_config_value(main_config="discord_config", config="guild_id")
)


class botDiscord(Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
        )

        self.database_handle = botDatabase(
            url=get_config_value(main_config="default_config", config="database_url"),
            database_name=get_config_value(
                main_config="default_config", config="database_name"
            ),
            member_database_name=get_config_value(
                main_config="member_config", config="collection_name"
            ),
            infrastructure_database_name=get_config_value(
                main_config="infrastructure_config", config="collection_name"
            ),
        )

    async def setup_hook(self):
        print(f"{self.user} has connected to Discord!")

        await bot.add_cog(botCommands(bot=bot))
        await bot.add_cog(
            botChatGPT(
                bot=bot,
                api_key=get_config_value(
                    main_config="default_config", config="openai_key"
                ),
            )
        )
        await bot.add_cog(
            botMemberManagement(bot=bot, database_handle=self.database_handle)
        )
        await bot.add_cog(
            botInfrastructureManagement(bot=bot, database_handle=self.database_handle)
        )
        await bot.add_cog(botEvents(bot=bot))
        await bot.add_cog(botTasks(bot=bot, database_handle=self.database_handle))

        # bot.tree.copy_global_to(guild=GUILD_ID)
        await bot.tree.sync()

    async def close(self) -> None:
        await super().close()


bot = botDiscord()
