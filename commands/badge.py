
import json
import typing
import discord

from db import get_badge_info_with_username
from utils.scrape_badges import scrape_badges


async def badge_command(bot, interaction: discord.Interaction, user: discord.User = None): 
    if user is None:
        user = interaction.user
    else:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"Hata: {interaction.user.mention} sadece kendi badge'lerinizi görebilirsiniz.")
            return
        
        
    
    # Get user roles
    target_user = await interaction.guild.fetch_member(user.id)
    
    user_roles = target_user.roles
    
    # Check if the user has the "Attendee" role
    if not any(role.name == "Attendee" for role in user_roles):
        await interaction.response.send_message(f"Hata: {user.mention} 'Attendee' rolünüz yok. Lütfen önce /register komutu ile kayıt olun.")
        return
        
    info = get_badge_info_with_username(user.name)
    
    if not info:
        await interaction.response.send_message(f"Hata: {user.mention} bot henüz profilinize bakmamış, birkaç saat içerisinde tekrar deneyin.")
        return
    
    # Print the info for the following database table:
    #    cursor.execute("CREATE TABLE IF NOT EXISTS badge_info (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), name VARCHAR(511), url VARCHAR(1023), badge_info TEXT, badge_count INT, error_info TEXT, lastChecked VARCHAR(255))")
    # Only use integer indexes for the info dictionary
    
    badges: typing.Dict[str:bool] = json.loads(info[3])
    badge_str = ""
    index = 0
    for key, value in badges.items():
        index += 1
        res = "Kazanıldı" if value else "Kazanılmadı"
        badge_str += f"{index}- {key}: {res}\n"
    
    message_str = ""
    message_str += f"{user.mention}:\n"
    if info[1]:
        message_str += f"İsim: {info[1]}\n"
    if info[2]:
        message_str += f"URL: <{info[2]}>\n"
    if info[5]:
        message_str += f"Hata: {info[5]}\n"
    if info[4]:
        message_str += f"Total badge sayısı: {info[4]}\n"
    else:
        message_str += f"Total badge sayısı: 0\n"
    if badge_str:
        message_str += f"Badge durumu:\n{badge_str}\n"
    if info[6]:
        # Remove last 7 characters from the info[6] string
        message_str += f"Son kontrol tarihi: {info[6][:-7]}\n"
    
    await interaction.response.send_message(message_str)
    