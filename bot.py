import asyncio
import json
import os
import sys

import discord

from typing import *
from pathlib import Path

parent_dir_path = str(Path(__file__).resolve().parents[0])
sys.path.append(parent_dir_path + "/src")
sys.path.append(parent_dir_path + "/lib")

from client import bot
from utils import *

bot.run(token=get_config_value(main_config="default_config", config="discord_token"))
