import discord
from discord.ext import commands
from db import create_db_tables
from config import DISCORD_TOKEN
from commands.register import register_command
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logging.info("Application start")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    logging.info("Bot Ready!")
    create_db_tables()
    await bot.tree.sync()
    logging.info("Bot Commands Synced!")

@bot.tree.command(name="register", description="Register a Google Developer Profile URL")
async def register(interaction: discord.Interaction, url: str, email: str):
    await register_command(bot, interaction, url, email)

bot.run(DISCORD_TOKEN)
