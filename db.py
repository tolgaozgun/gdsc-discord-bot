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
    cursor.execute("CREATE TABLE IF NOT EXISTS user_urls (username VARCHAR(255) PRIMARY KEY, url VARCHAR(1023), email VARCHAR(255))")
    connection.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS badge_info (username VARCHAR(255) PRIMARY KEY, name VARCHAR(511), url VARCHAR(1023), badge_info TEXT, badge_count INT, error_info TEXT, lastChecked VARCHAR(255))")
    cursor.close()
    connection.close()

def get_total_badge_count():
    connection = db_connect()
    cursor = connection.cursor()
    
    # SUM the badge_count column
    query = "SELECT SUM(badge_count) FROM badge_info"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        return result[0]
    return -1
    
def add_badge_info_to_db(
    username: str,
    name: str,
    url: str,
    badge_info: dict,
    badge_count: int,
    error_info: str,
    time: str
):
    connection = db_connect()
    cursor = connection.cursor()
    
    query = "INSERT INTO badge_info (username, name, url, badge_info, badge_count, error_info, lastChecked) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = %s, url = %s, badge_info = %s, badge_count = %s, error_info = %s, lastChecked = %s"
    data = (username, name, url, str(badge_info), badge_count, error_info, time, name, url, str(badge_info), badge_count, error_info, time)

    is_error = False
    try:
        cursor.execute(query, data)
        connection.commit()
    except mysql.connector.Error as error:
        logging.error(f"DB Error: {error}")
        is_error = True
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
    return not is_error

def get_badge_info_from_db(username: str):
    connection = db_connect()
    cursor = connection.cursor()
    
    query = "SELECT * FROM badge_info WHERE username = %s"
    data = (username,)
    cursor.execute(query, data)
    result = cursor.fetchone()
    
    if result:
        return {
            "username": result[1],
            "url": result[2],
            "badge_info": eval(result[3]),
            "badge_count": result[4],
            "error_info": result[5],
            "lastChecked": result[6]
        }
    return None


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
    data = (profile_url,)

    try: 
        cursor.execute(query, data)
        result = cursor.fetchone()
        # Check if result is not None
        if result:
            if connection.is_connected():
                cursor.close()
                connection.close()
            return False, "URL already exists in the database"
    except mysql.connector.Error as error:
        logging.error(f"DB Error: {error}")
        if connection.is_connected():
            cursor.close()
            connection.close()
        return False, str(error)
    

    # Insert the URL and user information into the database
    query = "INSERT INTO user_urls (username, url, email) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE url = %s, username = %s, email = %s"
    data = (username, profile_url, email, username, profile_url, email)
    
    is_error = False
    error_msg = ""
    
    try:
        cursor.execute(query, data)
        connection.commit()
    except mysql.connector.Error as error:
        logging.error(f"DB Error: {error}")
        error_msg = str(error)
        is_error = True
    finally: 
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return not is_error, error_msg
    
def get_all_users():
    connection = db_connect()
    cursor = connection.cursor()
    
    query = "SELECT * FROM user_urls"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if result:
        return result
    return None

def get_badge_info_with_username(username: str):
    connection = db_connect()
    cursor = connection.cursor()
    
    query = "SELECT * FROM badge_info WHERE username = %s"
    data = (username,)
    cursor.execute(query, data)
    result = cursor.fetchone()
    
    if result:
        return result
    return None

