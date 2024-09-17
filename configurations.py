
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

db_pass = os.getenv("PASS")
uri = f"mongodb+srv://dbCRUD:{db_pass}@clustermatidev.wvdwb.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMatiDev"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db
collection = db["todo_data"]