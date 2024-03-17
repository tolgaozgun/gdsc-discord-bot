
import json
import typing
import discord

from db import get_badge_info_with_username
from utils.scrape_badges import scrape_badges


async def badge_command(bot, interaction: discord.Interaction, user: discord.User = None): 
    # TODO: Add database or local .xlsx file check
    # Should return the latest check date, which badges are earned and which are not
    # Should also return the total badge count
    
    if user is None:
        user = interaction.user
        
    info = get_badge_info_with_username(user.name)
    
    if not info:
        await interaction.response.send_message(f"Hata: {user.mention} kullanıcı bulunamadı. Lütfen önce /register komutu ile kayıt olun.")
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
    if badge_str:
        message_str += f"Badge durumu:\n{badge_str}\n"
    if info[6]:
        message_str += f"Son kontrol tarihi: {info[6]}\n"
    
    await interaction.response.send_message(message_str)
    