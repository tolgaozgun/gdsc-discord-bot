
import discord

from db import get_total_badge_count


async def total_command(bot, interaction: discord.Interaction,): 
        
    count = get_total_badge_count()
    
    await interaction.response.send_message(interaction.user.mention + "Toplam badge sayısı: " + str(count))
    