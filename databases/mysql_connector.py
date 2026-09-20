import mysql.connector as sql
from dotenv import load_dotenv
import os

load_dotenv() #get all creadentials from the .env file instead of hardcoding them here

def connect_db():
    return sql.connect(
        # host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),
        # port = int(os.getenv("DB_PORT", 3306)) #fallback set to default mysql port if the port isnt specified in the .env file
    )