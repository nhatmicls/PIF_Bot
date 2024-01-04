import os
import json

from dotenv import load_dotenv

import discord

from typing import *


BOT_VERSION = 0.2


# ffmpeg tool's path
FFMPEG_PATH = "C:/Program Files/ffmpeg/bin/ffmpeg.exe"

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


def print_debug(instance, info):
    message = instance.__class__.__name__
    message += ": "
    message += info
    print(message)
