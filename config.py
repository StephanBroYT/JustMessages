from disnake.ext import commands
import disnake

intents = disnake.Intents.all()
intents.message_content = True

bot = commands.Bot(
    command_prefix = "/",
    intents = intents,
    activity = disnake.Game("Принмаю предложения"),
    status = disnake.Status.do_not_disturb
)


OWNERS = [
    986355526948515870, # Genes1us
    973169875419795488
]

TOKEN = ""


DevServers = 1146127100236026026