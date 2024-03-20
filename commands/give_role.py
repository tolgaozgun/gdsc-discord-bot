
import discord

from db import get_all_users
from utils.scrape_badges import scrape_badges


async def give_role_command(bot, interaction: discord.Interaction): 
    await interaction.response.send_message("Lütfen bekleyin...")

    # Get all urls from the database
    result = get_all_users()
    
    # Turn this to a list of discord usernames
    usernames = [user[0] for user in result]
    
    update_frequency = 5  # Determines how often to update the message (every 5 rows in this example)
    
    msg = await interaction.original_response()
    
    success_count = 0
    failure_count = 0
    total_count = 0
    members_given = []
    members_not_given = []
    # Check if username exists in the server, if it does, add the role named "Attendee"
    for username in usernames:
        total_count += 1
        member = interaction.guild.get_member_named(username)
        if member is not None:
            success_count += 1
            role = discord.utils.get(interaction.guild.roles, name="Attendee")
            members_given.append(usernames)
            await member.add_roles(role)
        else:
            members_not_given.append(username)
            failure_count += 1
        
        if total_count % update_frequency == 0:
            await msg.edit(content=f"İşlenen: {total_count}/{len(usernames)}.\nBaşarılı: {success_count}, Hatalı: {failure_count}")
        
    await msg.edit(content=f"İşlem tamamlandı. {success_count} tane kullanıcıya rol verildi. {failure_count} tane kullanıcı bulunamadı.")
    # if members_given:
    #     await interaction.followup.send("Rol verilen kullanıcılar:" + ', '.join(members_given))
    # else:
    #     await interaction.followup.send("Rol verilen kullanıcı bulunamadı.")
        
    if members_not_given:
        await interaction.followup.send("Rol verilemeyen kullanıcılar:" + ', '.join(members_not_given))
        