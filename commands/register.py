import discord
from discord.ext import commands
from utils.add_https_url import add_https_url
from utils.check_profile_exists import check_profile_exists
from db import add_user_to_db, db_connect
import mysql.connector

import logging

from utils.check_registered_email import check_registered_email
from utils.match_url import match_url

logger = logging.getLogger(__name__)


async def register_command(bot, interaction: discord.Interaction, url: str, email: str): 

    user_roles = interaction.user.roles
    
    if user_roles is not None:
        for role in user_roles:
            if role.name == "Attendee":
                await interaction.response.send_message("Hata: Zaten kayıt oldunuz.")
                logging.error(f"Error message: <You have already registered, username: {interaction.user.name}, user_id: {interaction.user.id}>")
                return
            
    if not check_registered_email(email, filename='emails.csv'):
        await interaction.response.send_message("Hata: E-posta adresiniz kayıtlı değil.")
        logging.error(f"Error: Email is not registered, email: {email}")
        return
    print("Email is registered.")
            
    url = add_https_url(url)
    
    # Validate URL format
    if not match_url(url):
        await interaction.response.send_message("Hata: URL gerekli formata uymuyor.")
        logging.error(f"Error: URL does not match the required format, url: {url}")
        return
    
    await interaction.response.send_message("Lütfen bekleyin...")
    
    if not check_profile_exists(url):
        msg = await interaction.original_response()
        await msg.edit(content="Hata: Bu profil ya da URL herkese açık değil.")
        logging.error(f"Error: Profile or URL is not public, url: {url}")
        return
    
    add_db_success, error_msg = add_user_to_db(
        str(interaction.user.id),
        interaction.user.name,
        url,
        email,
    )
    
    if not add_db_success:
        msg = await interaction.original_response()
        await msg.edit(content="URL kaydedilemedi. Lütfen yetkiliyle iletişime geçin. Hata: " + error_msg)
        logging.error(f"Error: URL could not be saved, url: {url}")
        return
        
    msg = await interaction.original_response()
    await msg.edit(content="Başarılı: URL başarıyla kaydedildi.")
    logging.info(f"URL registered successfully, url: {url}")
    
    
    role=discord.utils.get(interaction.guild.roles, name="Attendee")
    if role:
        await interaction.user.add_roles(role)
        msg = await interaction.original_response()
        await msg.edit(content="Başarılı: URL başarıyla kaydedildi ve rol atandı.")
        logging.info(f"URL registered successfully and role assigned, url: {url}, username: {interaction.user.name}, user_id: {interaction.user.id}")
    else:
        msg = await interaction.original_response()
        await msg.edit(content="Hata: URL başarıyla kaydedildi. Ancak belirtilen rol bulunamadı.")
        logging.error(f"Error: URL registered successfully but the specified role could not be found, url: {url}, username: {interaction.user.name}, user_id: {interaction.user.id}")
    
