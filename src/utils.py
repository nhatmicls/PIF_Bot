import os
import json

from dotenv import load_dotenv

import discord

from typing import *


BOT_VERSION = 0.2

DEFAULT_CONFIG_FILE_PATH = "./config/default/product_config.json"


def get_env_data(env: str):
    load_dotenv()

    return os.getenv(env, None)


def get_config_value(main_config: str, config: str) -> Union[str, int]:
    with open(DEFAULT_CONFIG_FILE_PATH) as default_config_file:
        default_config_file_contents = json.loads(default_config_file.read())

    return default_config_file_contents[main_config][config]


async def check_guild_id(interaction: discord.Interaction) -> bool:
    if interaction.guild_id == get_config_value(
        main_config="discord_config", config="guild_id"
    ):
        return True
    else:
        await interaction.response.send_message(
            "This command not support your server !!!", ephemeral=True
        )
        return False


def check_admin_role(role: List[str]) -> bool:
    def predicate(interaction: discord.Interaction) -> bool:
        if isinstance(interaction.user, discord.User):
            raise discord.app_commands.errors.NoPrivateMessage()

        user_role = interaction.user.roles
        for user_each_role in user_role:
            if user_each_role.name in role:
                return True

        raise discord.app_commands.errors.MissingAnyRole(role)

    return discord.app_commands.check(predicate)


async def read_text_file(path: str) -> str:
    f = open(path, "r")
    return f.read()


def print_debug(instance, info):
    message = instance.__class__.__name__
    message += ": "
    message += info
    print(message)
