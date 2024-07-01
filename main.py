from decouple import Config, RepositoryEnv
from discord.ext import commands
from discord import Intents
import os
import asyncio

# Conexión con la key|clave de mi archivo .env
config = Config(RepositoryEnv('./private/.env'))
TOKEN = config('DISCORD_TOKEN')

# Lista de IDs de los canales permitidos (asegúrate de que sean números enteros)
ALLOWED_CHANNELS = list(map(int, config('DISCORD_ALLOWED_CHANNELS').split(',')))

intents = Intents.default()  # Permisos
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

def is_allowed_channel():
    def predicate(ctx):
        return ctx.channel.id in ALLOWED_CHANNELS
    return commands.check(predicate)

# Agregar una verificación global para todos los comandos
@bot.check
async def globally_allowed_channel(ctx):
    if ctx.channel.id not in ALLOWED_CHANNELS:
        await ctx.send("Este comando solo se puede usar en canales permitidos.")
        return False
    return True

@bot.command()
async def test(ctx):
    await ctx.send("Este comando solo se puede usar en canales permitidos.")

async def load():
    for filename in os.listdir("./app"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"app.{filename[:-3]}")
            except Exception as e:
                print(f"Error cargando el archivo {filename}: {e}")

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
