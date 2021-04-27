import os
import pymongo
from pymongo import MongoClient


MONGO_CLIENT = os.getenv('CLIENT')
cluster = MongoClient(MONGO_CLIENT)

db = cluster["URL-Shortener"]
url_collection = db["url"]
user_collection = db["user"]
session_collection = db["session"]


new_url = {
    "long_url": "",
    "short_url": "",
    "click_count": 0
}

new_user = {
    "_id":  "",
    "email": "",
    "password":"",
    "authenticated":False
}

new_session = {
    "domain": "",
    "path": "",
    "expiration": ""
}