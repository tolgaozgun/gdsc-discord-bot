import mysql.connector
from config import DB_CONFIG
import logging

import logging

logger = logging.getLogger(__name__)

def db_connect():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection

def create_db_tables():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user_urls (id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(255), username VARCHAR(255), url VARCHAR(1024))")
    connection.commit()
    cursor.close()
    connection.close()


def add_user_to_db(
    user_id: str,
    username: str,
    profile_url: str,
    email: str
):
    
    # Connect to the database
    connection = db_connect()
    cursor = connection.cursor()
    
    # Check if the URL already exists in the database
    query = "SELECT * FROM user_urls WHERE url = %s"
    data = (profile_url)

    # Insert the URL and user information into the database
    query = "INSERT INTO user_urls (user_id, username, url, email) VALUES (%s, %s, %s, %s)"
    data = (user_id, username, profile_url, email)
    
    error = False
    
    try:
        cursor.execute(query, data)
        connection.commit()
    except mysql.connector.Error as error:
        logging.error(f"DB Error: {error}")
        error = True
    finally: 
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return not error
    
    