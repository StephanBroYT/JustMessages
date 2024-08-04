import io
from PIL import Image
import imageio
import disnake
from disnake.ext import commands
import json
import config
# from config import bot

SETTINGS_FILE = 'mutes.json'

def save_settings(settings, filename=SETTINGS_FILE):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def load_settings(filename=SETTINGS_FILE):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


class unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Анмут в преддложке")
    async def ummute(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        if inter.author.id not in config.OWNERS:
            await inter.response.send_message(embed=disnake.Embed(
                colour=disnake.Color.red(),
                description="У вас нет прав",
            ), ephemeral=True)
            return
        
        settings = load_settings()
        # print(settings)
        if not str(user.id) in settings:
            await inter.response.send_message("Пользователь не в муте")
            return
        
        settings = load_settings()
        # settings[user.id] = {}
        settings.pop(str(user.id))
        save_settings(settings)
        await inter.response.send_message(f'({user.id}), {user.name} разамучен')
        
        

def setup(bot):
    bot.add_cog(unmute(bot))
