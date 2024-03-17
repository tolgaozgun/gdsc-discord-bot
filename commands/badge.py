
import discord

from utils.scrape_badges import scrape_badges


async def badge_command(bot, interaction: discord.Interaction): 
    # TODO: Add database or local .xlsx file check
    # Should return the latest check date, which badges are earned and which are not
    # Should also return the total badge count
    await interaction.response.send_message("Komut devre dışı...")