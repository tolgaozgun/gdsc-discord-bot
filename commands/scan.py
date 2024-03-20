
import discord

from db import get_all_users
from utils.scrape_badges import scrape_badges


async def scan_command(bot, interaction: discord.Interaction): 
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(f"Hata: {interaction.user.mention} bu komutu sadece adminler kullanabilir.")
        return

    await interaction.response.send_message("Lütfen bekleyin...")
    
    # Get all urls from the database
    result = get_all_users()
    
    # Turn this to a dictionary with the username as the key, and the url as the value
    # Username has the key username in result dictionary, and url has the key url in result dictionary
    urls = {user[0]: user[1] for user in result}
    
    async def update_progress(cur_count, total_count, success_count, failure_count):
        msg = await interaction.original_response()
        await msg.edit(content=f"İşlenen: {cur_count}/{total_count}.\nBaşarılı: {success_count}, Hatalı: {failure_count}")
    
    issues, success = await scrape_badges(urls, update_progress)
    
    msg = await interaction.original_response()
    await msg.edit(content=f"İşlem tamamlandı. {success} tane profil başarıyla tarandı. Hatalar:")
    
    # Send a message to the interaction channel with the result for each 2000 characters
    total_char = 0
    cur_issues = ""
    for issue in issues:
        # Get the length of the current issue
        cur_char = len(issue)
        # If the total length of the issues and the current issue is greater than 2000
        if total_char + cur_char > 2000:
            # Send the message
            await interaction.followup.send(cur_issues)
            # Reset the total_char and cur_issues
            total_char = cur_char
            cur_issues = issue
        else:
            # Add the current issue to the cur_issues
            cur_issues += issue + "\n"
            # Add the length of the current issue to the total_char
            total_char += cur_char
        
        