
import discord
import tqdm

from db import add_user_to_db
from utils.add_https_url import add_https_url
from utils.match_url import match_url
from utils.scrape_badges import scrape_badge
import openpyxl

import pandas as pd


async def ingest_command(bot, interaction: discord.Interaction, file: discord.Attachment): 
    await interaction.response.send_message("Lütfen bekleyin...")
    
    # Check if the file is a valid excel file
    if not file.filename.endswith('.xlsx'):
        msg = await interaction.original_response()
        await msg.edit(content="Hata: Dosya formatı geçersiz.")
        return
    

    await file.save(file.filename)
    
    df = pd.read_excel(file.filename)
    
    # Prepare for updating the progress
    total_rows = len(df)
    progress_message = await interaction.original_response()
    update_frequency = 5  # Determines how often to update the message (every 5 rows in this example)
    
    not_added = []
    
    added_amount = 0
    success_count = 0
    failure_count = 0
    for index, row in df.iterrows():
        email = row[0]
        url = row[1]
        username = row[2]
        
        username = str(username)
        
        url = url.strip()
        url = add_https_url(url)
        
        if not match_url(url):
            failure_count += 1
            not_added.append("Eposta: " + email + " satır: " + str(index + 2) + " (URL formatı hatalı): " + url)
            continue

        email = email.strip()
        username = username.strip()
        
        # Simulate adding user to database
        result, error_msg = add_user_to_db(str(username), username, url, email)
        
        added_amount += result
        
        if not result:
            failure_count += 1
            not_added.append(email + " satır: " + str(index + 2) + " (veritabani hatasi): " + error_msg + " (URL: <" + url + ">)")
        else:
            success_count += 1
            
        # Update the message periodically
        if (index + 1) % update_frequency == 0 or index == total_rows - 1:
            await progress_message.edit(content="Tarama ilerlemesi: " + str(index + 1) + "/" + str(total_rows) + ".\nBaşarılı: " + str(success_count) + ", Başarısız: " + str(failure_count))

    # Final update to indicate completion
    await progress_message.edit(content="Dokuman başarıyla işlendi. Toplam: " + str(added_amount) + " ekleme yapıldı. Hatalar:")
    
    
    # Send a message to the interaction channel with the result for each 2000 characters
    total_char = 0
    cur_issues = ""
    for issue in not_added:
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
        


        
        
        
    
    