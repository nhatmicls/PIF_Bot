import platform
import requests
import random
import ast
from pathlib import Path

import discord

import aiohttp

from discord.ext.commands import Cog, Bot
from discord import app_commands

from utils import *
from typing import *


class botCommands(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

    async def _info(self) -> discord.Embed:
        embed = discord.Embed(
            title="PIF Club's bot",
            description="Pay It Forward",
        )

        embed.add_field(name="**Bot Version:**", value=BOT_VERSION)
        embed.add_field(name="**Python Version:**", value=platform.python_version())
        embed.add_field(name="**Discord.Py Version**", value=discord.__version__)

        return embed

    async def _random_cat(self) -> Union[discord.Embed, str]:
        try:
            main_url = "https://random.cat/view/" + str(random.randint(1, 1000))
            # response = requests.get(main_url)
            async with aiohttp.ClientSession() as session:
                async with session.get(main_url) as response:
                    if response.status == 200:
                        data = response.content._buffer[0].decode("utf-8")
                        img_url_start_loc = data.find("https://purr.objects")
                        for x in range(img_url_start_loc, len(data)):
                            if data[x] == '"':
                                img_url = data[img_url_start_loc:x]
                                break

                        embed = discord.Embed(
                            title="Kitty Cat 🐈", colour=discord.Color.random()
                        )
                        embed.set_image(url=img_url)

                        return embed

            return "Error fetching data"
        except Exception as e:
            print(e)
            return "Some thing error"

    async def _random_anime_image(
        self, type: str, choices: app_commands.Choice[str]
    ) -> Union[discord.Embed, str]:
        try:
            main_url = "https://api.waifu.pics/" + type + "/" + choices.value
            async with aiohttp.ClientSession() as session:
                async with session.get(main_url) as response:
                    if response.status == 200:
                        response_body = await response.read()
                        response_url = ast.literal_eval(response_body.decode("utf-8"))
                        embed = discord.Embed(
                            title="Your waifu 🐈", colour=discord.Color.random()
                        )
                        embed.set_image(url=response_url["url"])

                        return embed

            return "Error fetching data"
        except Exception as e:
            print(e)
            return "Some thing error"

    async def _ping(self) -> discord.Embed:
        embed = discord.Embed(
            title="Pong!",
            description=f"Heartbeat: {round(self.bot.latency * 1000, 2)} ms",
            color=discord.Color.random(),
        )

        return embed

    async def _get_anime_image(self, type: str, choices: app_commands.Choice[str]):
        return_data = await self._random_anime_image(type=type, choices=choices)
        return return_data

    @app_commands.command(
        name="cat",
        description="Just cat",
    )
    async def cat(self, interaction: discord.Interaction):
        return_data = await self._random_cat()
        try:
            if type(return_data) == str:
                await interaction.response.send_message(return_data, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "", embed=return_data, ephemeral=False
                )
        except:
            await interaction.response.send_message("Some thing error", ephemeral=True)

    @app_commands.command(
        name="waifu",
        description="Just waifu",
    )
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="waifu", value="waifu"),
            app_commands.Choice(name="lick", value="lick"),
            app_commands.Choice(name="pat", value="pat"),
        ]
    )
    async def waifu(
        self, interaction: discord.Interaction, choices: app_commands.Choice[str]
    ):
        try:
            return_data = self._get_anime_image(type="sfw", choices=choices)
            if type(return_data) == str:
                await interaction.response.send_message(return_data, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "", embed=return_data, ephemeral=True
                )
        except:
            await interaction.response.send_message("Some thing error", ephemeral=True)

    @app_commands.command(
        name="nsfw",
        description="Just waifu",
    )
    @app_commands.choices(
        choices=[
            app_commands.Choice(name="waifu", value="waifu"),
            app_commands.Choice(name="lick", value="lick"),
            app_commands.Choice(name="pat", value="pat"),
        ]
    )
    async def nsfw(
        self, interaction: discord.Interaction, choices: app_commands.Choice[str]
    ):
        try:
            if (
                get_config_value(main_config="birthday_config", config="nsfw").lower()
                == "true"
            ):
                return_data = self._get_anime_image(type="nsfw", choices=choices)
                if type(return_data) == str:
                    await interaction.response.send_message(return_data, ephemeral=True)
                else:
                    await interaction.response.send_message(
                        "", embed=return_data, ephemeral=True
                    )
            else:
                embed_image = discord.File(
                    "/pif/bot-playground/image/wtfisthis.jpg", filename="wtfisthis.jpg"
                )
                return_embed = discord.Embed()
                return_embed.set_image(url="attachment://wtfisthis.jpg")
                await interaction.response.send_message(
                    "Ehhhh what do you finding hentai",
                    embed=return_embed,
                    file=embed_image,
                    ephemeral=True,
                )
        except:
            await interaction.response.send_message("Some thing error", ephemeral=True)

    @app_commands.command(
        name="info",
        description="Just info",
    )
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "", embed=await self._info(), ephemeral=True
        )

    @app_commands.command(
        name="ping",
        description="Just ping",
    )
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "", embed=await self._ping(), ephemeral=True
        )

    @app_commands.command(
        name="test",
        description="Just test",
    )
    async def test(self, interaction: discord.Interaction):
        print(interaction.user.roles)
        print(type(interaction.user.roles))
        print(interaction.user.roles[0])
        print(type(interaction.user.roles[0]))
        print(str(interaction.user.roles[0]))
        await interaction.response.send_message(
            "", embed=await self._ping(), ephemeral=True
        )
