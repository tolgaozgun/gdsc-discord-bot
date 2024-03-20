
import discord

from db import get_all_badge_info_as_xlsx
from datetime import datetime


import logging

logger = logging.getLogger(__name__)

async def badge_table_command(bot, interaction: discord.Interaction,): 
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(f"Hata: {interaction.user.mention} bu komutu sadece adminler kullanabilir.")
        return
    
    # Current day-time as string
    # in the format: 2021-09-28 12:00:00
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    
    file_name = current_time + "_badge_table.xlsx"
    
    file_path = get_all_badge_info_as_xlsx(file_name)
    
    if not file_path:
        await interaction.response.send_message(f"Hata: {interaction.user.mention} bir hata oluştu. Lütfen tekrar deneyin.")
        logger.error("Error creating the badge table, get_all_badge_info_as_xlsx returned None.")
        return
    
    # Send the file to the interaction channel
    await interaction.response.send_message(file=discord.File(file_path))
    