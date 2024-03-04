import discord
from discord.ext import commands
import mysql.connector
import dotenv
import re
import os
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



dotenv.load_dotenv()
# discord.Intents.message_content = True #v2

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Database configuration - Replace these with your actual database details
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT')
}

# Connect to the database
def db_connect():
    connection = mysql.connector.connect(**db_config)
    return connection

def create_db_tables():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user_urls (id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(255), username VARCHAR(255), url VARCHAR(1024))")
    connection.commit()
    cursor.close()
    connection.close()

@bot.event
async def on_ready():
    # print "ready" in the console when the bot is ready to work
    print("Bot Ready!")
    # Create tables
    create_db_tables()
    await bot.tree.sync()
    print("Bot Commands Synced!")
    
def fix_regex(url: str):
    # Fix URL format
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
    if not url.startswith("https://"):
        url = "https://" + url
    return url
    

def match_regex(url):
    # Match following URLS:
    # https://developers.google.com/profile/u/\w+
    # https://g.dev/\w+
    # http://developers.google.com/profile/u/\w+
    # http://g.dev/\w+
    # developers.google.com/profile/u/\w+
    # g.dev/\w+
    urls_to_match = [
        r'https://developers.google.com/profile/u/\w+',
        r'https://g.dev/\w+',
        r'http://developers.google.com/profile/u/\w+',
        r'http://g.dev/\w+']
    
    return any(re.match(url_to_match, url) for url_to_match in urls_to_match)
    

# Register command implementation
@bot.tree.command(name="register", description="Register a Google Developer Profile URL", )
async def register(interaction:discord.Interaction, url: str):
    
    user_roles = interaction.user.roles
    
    if user_roles is not None:
        for role in user_roles:
            if role.name == "Attendee":
                await interaction.response.send_message("Hata: Zaten kayıt oldunuz.")
                print("You have already registered.")
                return
            
    url = fix_regex(url)
    
    # Validate URL format
    if not match_regex(url):
        await interaction.response.send_message("Hata: URL gerekli formata uymuyor.")
        print("Error: URL does not match the required format.")
        return
    
    await interaction.response.send_message("Lütfen bekleyin...")
    
    # Check for devsite-profiles-splash--text class in the page
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    wd = webdriver.Chrome(options=options)
    wd.get(url)
    time.sleep(8)  # Allow time for the page to load
    soup = BeautifulSoup(wd.page_source, 'lxml')
    wd.quit()  # Close the browser

    # Check for the presence of the specific class
    if soup.find_all('div', {'class': 'devsite-profiles-splash--text'}):
        msg = await interaction.original_response()
        await msg.edit(content="Hata: Bu profil ya da URL halka açık değil.")
        print("Error: This profile is either not public or URL is wrong.")
        return
    
    # Connect to the database
    connection = db_connect()
    cursor = connection.cursor()
    
    # Check if the URL already exists in the database
    query = "SELECT * FROM user_urls WHERE url = %s"
    data = (url)

    # Insert the URL and user information into the database
    query = "INSERT INTO user_urls (user_id, username, url) VALUES (%s, %s, %s)"
    data = (str(interaction.user.id), interaction.user.name, url)

    try:
        cursor.execute(query, data)
        connection.commit()
        msg = await interaction.original_response()
        await msg.edit(content="Başarılı: URL başarıyla kaydedildi.")
        print("URL registered successfully.")
        
        
        role=discord.utils.get(interaction.guild.roles, name="Attendee")
        if role:
            await interaction.user.add_roles(role)
            msg = await interaction.original_response()
            await msg.edit(content="Başarılı: URL başarıyla kaydedildi ve rol atandı.")
            print("URL registered successfully and role assigned.")
        else:
            msg = await interaction.original_response()
            await msg.edit(content="Hata: URL başarıyla kaydedildi. Ancak belirtilen rol bulunamadı.")
            print("URL registered successfully. However, the specified role could not be found.")
    except mysql.connector.Error as error:
        msg = await interaction.original_response()
        await msg.edit(content=f"MYSQL Hata: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(DISCORD_TOKEN)
