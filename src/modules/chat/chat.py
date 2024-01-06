import asyncio
import json
import os
import sys

import discord
from discord.ext.commands import Cog
from discord import app_commands

from utils import *
from typing import *

import openai
from openai import RateLimitError

from chat_exceptions_handle import *


class botChatGPT(Cog):
    def __init__(self, bot, api_key):
        super().__init__()

        self.bot = bot

        self.model_engine = "gpt-3.5-turbo"
        openai.api_key = api_key

    def get_response(self, prompt):
        try:
            completion = openai.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            generated_text = completion.choices[0].text.strip("\n")
        except RateLimitError:
            return "Rate Limit Error"
        except Exception as e:
            return e

        return generated_text

    @app_commands.command(
        name="gpt",
        description="Use GPT chat, it doesn't work right now",
    )
    @app_commands.describe(gpt_question="Question for GPT")
    async def gpt(self, interaction: discord.Interaction, gpt_question: str):
        generated_text = self.get_response(gpt_question)
        await interaction.response.send_message(generated_text)

    @app_commands.command(name="say", description="Say something")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(sentence="Random string")
    async def say(self, interaction: discord.Interaction, sentence: str):
        await interaction.response.send_message("OK", delete_after=1, ephemeral=True)
        await interaction.channel.send(sentence)

    @say.error
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
