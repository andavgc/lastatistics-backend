from model import User
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
CONNECTION_STRING = os.getenv("DB")

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://andresdgarcia96:FBYrl5ZaALWTl3i0@cluster0.4pladlx.mongodb.net/test"
    
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
    return client['MusicApp']
  
# This is added so that many files can reuse the function get_database()

# Get the database
database = get_database()
collection = database['track']

async def fetch_user(user):
    document = collection.find_one({"user":user})
    return document

async def fetch_all_users():
    users = []
    cursor = collection.find({})
    for document in cursor:
        users.append(User(**document))
    return users

async def create_user(document):
    
    new_user = collection.insert_one(document)
    return document

async def update_user(document):
    collection.update_one({"user":document["user"]},{"$set":{
        "period": document["period"],
        "length": document["length"],
        "tracklist": document["tracklist"]}})
    document = collection.find_one({"user":document["user"]})
    return document
