import io
from PIL import Image
import imageio
import disnake
from disnake.ext import commands
# from config import bot
import json

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


class predloshka(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        settings = load_settings()
        # print(settings)
        if str(message.author.id) in settings:
            await message.channel.send("Вы замучены в боте!")
            return
        
        if isinstance(message.channel, disnake.DMChannel):
            # Проверяем, что сообщение отправлено в личные сообщения и содержит текст или вложения
            if message.attachments:
                attachment = message.attachments[0]
                await self.ask_conversion_type(attachment=attachment, message=message)
            elif message.content:
                await self.ask_conversion_type(message=message)

    async def ask_conversion_type(self, attachment=None, message=None):
        try:
            # Отправляем сообщение с кнопками
            msg = await message.channel.send(
                embed=disnake.Embed(title="Правила:", description="Не постить говно"),
                components=[
                    disnake.ui.ActionRow(
                        disnake.ui.Button(
                            style=disnake.ButtonStyle.primary, 
                            label="✅Согласен"
                        )
                    )
                ]
            )
            # Ожидаем нажатия кнопки
            interaction = await self.bot.wait_for(
                "button_click", check=lambda i: i.user == message.author
            )
            # Обрабатываем нажатие кнопки
            if interaction.component.label == "✅Согласен":
                await interaction.response.edit_message(components=[
                    disnake.ui.ActionRow(
                        disnake.ui.Button(
                            style=disnake.ButtonStyle.primary,
                            label="✅Согласен",
                            disabled=True
                        )
                    )
                ])
                await self.process_message(attachment=attachment, message=message)
                
                
        except Exception as e:
            await message.channel.send(f"Ошибка: {e}")

    async def process_message(self, attachment=None, message=None):
        try:
            if attachment and message.content:
                description = message.content
                emb = disnake.Embed(description=description).set_author(
                    name=message.author.name, 
                    icon_url=message.author.avatar.url
                ).set_image(url=attachment.url)
            elif attachment:
                emb = disnake.Embed().set_author(
                    name=message.author.name, 
                    icon_url=message.author.avatar.url
                ).set_image(url=attachment.url)
            else:
                emb = disnake.Embed(description=message.content).set_author(
                    name=message.author.name, 
                    icon_url=message.author.avatar.url
                )
                
            await message.channel.send(embed=emb)
            msg = await message.channel.send(
                embed=disnake.Embed(title="Опубликовать сообщение?", description="Ваше сообщение будет сразу отправлено в выбранный канал"),
                components=[
                    disnake.ui.ActionRow(
                        disnake.ui.Button(
                            style=disnake.ButtonStyle.primary, 
                            label="✉️Отправить?"
                        )
                    )
                ]
            )
            
            # Ожидаем нажатия кнопки
            interaction = await self.bot.wait_for(
                "button_click", check=lambda i: i.user == message.author
            )
            # Обрабатываем нажатие кнопки
            if interaction.component.label == "✉️Отправить?":
                await interaction.response.edit_message(components=[
                    disnake.ui.ActionRow(
                        disnake.ui.Button(
                            style=disnake.ButtonStyle.primary,
                            label="✉️Отправить?",
                            disabled=True
                        )
                    )
                ])
                
                channelsend = self.bot.get_channel(1269335033265524861)
                
                reactmessage = await channelsend.send(embed=emb)
                
                await reactmessage.add_reaction("👍")
                await reactmessage.add_reaction("👎")
                
                # Send a success message only here
                await message.channel.send(embed=disnake.Embed(title="Сообщение опубликовано", color=disnake.Colour.green()))
                
        except Exception as e:
            await message.channel.send(f"Ошибка: {e}")

def setup(bot):
    bot.add_cog(predloshka(bot))
