# main.py

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
from config_manager import config

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Logging
if config.get("debug_mode"):
    handler = logging.FileHandler(filename=config.get("log_file"), encoding='utf-8', mode='w')
    logging.basicConfig(level=logging.INFO, handlers=[handler])

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        # ✅ This is where cogs are loaded
        await self.load_extension("cogs.config_commands")

bot = MyBot(command_prefix=config.get("prefix"), intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

bot.run(token)
