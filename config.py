from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
# ========== db ==========

def get_db(db_name):
    connection_string = f"mongodb+srv://{os.getenv('DB_USER')}:1q2w3e4r@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    client = MongoClient(connection_string) # MongoClient 객체 생성

    db = client[db_name]

    return db