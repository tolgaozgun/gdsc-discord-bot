
import discord

from db import get_all_badge_info_as_xlsx



import logging

logger = logging.getLogger(__name__)

async def badge_table_command(bot, interaction: discord.Interaction,): 
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(f"Hata: {interaction.user.mention} bu komutu sadece adminler kullanabilir.")
        return
    
    file_path = get_all_badge_info_as_xlsx()
    
    if not file_path:
        await interaction.response.send_message(f"Hata: {interaction.user.mention} bir hata oluştu. Lütfen tekrar deneyin.")
        logger.error("Error creating the badge table, get_all_badge_info_as_xlsx returned None.")
        return
    
    # Send the file to the interaction channel
    await interaction.response.send_message(file=discord.File(file_path))
    