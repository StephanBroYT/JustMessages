from disnake.ext import commands
import disnake
import os
import io
import imageio

import config
from PIL import Image
import logging

bot = config.bot

logging.basicConfig(level=logging.INFO)





@bot.event
async def on_ready():
    bot.load_extension("cogs.messages")
    bot.load_extension("cogs.mute")
    bot.load_extension("cogs.unmute")
    bot.load_extension("cogs.admin_tools")
    print(f"Logged in as {bot.user} ({bot.user.id})")




bot.run(config.TOKEN)
