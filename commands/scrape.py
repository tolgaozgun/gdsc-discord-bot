
import discord

from utils.scrape_badges import scrape_badges


async def scrape_command(bot, interaction: discord.Interaction): 
    await interaction.response.send_message("Lütfen bekleyin...")

    file_path = scrape_badges()

    msg = await interaction.original_response()
    await msg.edit(content="İşlem tamamlandı. İşte sonuçlar:", file=discord.File(file_path))