
import discord

from db import get_total_badge_count


async def total_command(bot, interaction: discord.Interaction,): 
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(f"Hata: {interaction.user.mention} bu komutu sadece adminler kullanabilir.")
        return

        
    count = get_total_badge_count()
    
    await interaction.response.send_message(interaction.user.mention + "Toplam badge sayısı: " + str(count))
    