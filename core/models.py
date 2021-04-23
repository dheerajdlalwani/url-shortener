import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_CLIENT = os.getenv('CLIENT')
cluster = MongoClient(MONGO_CLIENT)
db = cluster["URL-Shortener"]
collection = db["url"]


new_url = {
    "long_url": "",
    "short_url": "",
    "click_count": 0
}

