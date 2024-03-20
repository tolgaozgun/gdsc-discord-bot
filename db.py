import json
import os
import typing
import mysql.connector
from config import DB_CONFIG
import logging
import pandas as pd


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


def get_all_badge_info_as_xlsx(file_name="badge_info.xlsx"):
    # Connect to the database (assuming db_connect is defined elsewhere)
    connection = db_connect()
    cursor = connection.cursor()
    
    # Write a query to get all the badge info and right join it with the user_urls table
    # Use username as the key to join the tables
    # And get email from user_urls table
    query = "SELECT badge_info.username, badge_info.name, user_urls.url, badge_info.badge_info, badge_info.badge_count, badge_info.error_info, badge_info.lastChecked, user_urls.email FROM badge_info RIGHT JOIN user_urls ON badge_info.username = user_urls.username"
    cursor.execute(query)
    result = cursor.fetchall()

    # # Execute the query
    # query = "SELECT * FROM badge_info"
    # cursor.execute(query)
    # result = cursor.fetchall()

    # Check if the result is empty
    if not result:
        logging.error("get_all_badge_info_as_xlsx: result returned None.")
        return None

    # Process each row to parse the JSON in the fourth column and extend it
    extended_rows = []
    for row in result:
        # Assuming the fourth column contains the JSON string
        badge_list = json.loads(row[3])  # Parse JSON string
        extended_row = list(row[:3]) + list(row[4:])  # Exclude the original JSON string column

        # Add JSON key-value pairs to the row
        for key, value in badge_list.items():
            extended_row.append(value)

        extended_rows.append(extended_row)

    # Define column names, assuming the first part of the header is static
    headers = ["Discord Kullanıcı Adı", "Ad Soyad", "Profil URL", "Badge Sayısı", "Hata Bilgisi", "Son Kontrol Tarihi"]
    # Dynamically add JSON keys as headers. Assuming all rows have the same keys in the JSON part
    json_keys = list(json.loads(result[0][3]).keys())  # Parse JSON from the first row to get keys
    headers.extend(json_keys)

    # Convert the list of extended rows into a DataFrame
    df = pd.DataFrame(extended_rows, columns=headers)

    # Delete the file if it exists
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass

    # Export DataFrame to an XLSX file
    df.to_excel(file_name, index=False)

    # Return the absolute path of the file
    return os.path.abspath(file_name)
