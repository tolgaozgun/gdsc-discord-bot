import discord
from discord.ext import commands
from commands.badge import badge_command
from commands.badge_table import badge_table_command
from commands.give_role import give_role_command
from commands.ingest import ingest_command
from commands.scan import scan_command
from commands.total import total_command
from db import create_db_tables
from config import DISCORD_TOKEN
from commands.register import register_command
import logging
import os 

os.environ['TZ'] = 'Europe/Istanbul'

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

    
@bot.tree.command(name="scan", description="Check badge status")
@commands.has_permissions(administrator=True)
async def register(interaction: discord.Interaction):
    await scan_command(bot, interaction,)

@bot.tree.command(name="badge", description="Check your own badge status")
async def register(interaction: discord.Interaction):
    await badge_command(bot, interaction)

@bot.tree.command(name="badge-admin", description="Check someone else's status")
@commands.has_permissions(administrator=True)
async def register(interaction: discord.Interaction, user: discord.User):
    await badge_command(bot, interaction, user)
    
@bot.tree.command(name="total", description="Check total badge count")
@commands.has_permissions(administrator=True)
async def register(interaction: discord.Interaction):
    await total_command(bot, interaction)

@bot.tree.command(name="ingest", description="Add users to the db from an excel file")
@commands.has_permissions(administrator=True)
async def register(interaction: discord.Interaction, file: discord.Attachment):
    await ingest_command(bot, interaction, file)


@bot.tree.command(name="giverole", description="Give Attendee role to users")
@commands.has_permissions(administrator=True)
async def register(interaction: discord.Interaction):
    await give_role_command(bot, interaction)


@bot.tree.command(name="badge-table", description="Badge table as a csv file")
@commands.has_permissions(administrator=True)
async def register(interaction: discord.Interaction):
    await badge_table_command(bot, interaction)
    
bot.run(DISCORD_TOKEN)
