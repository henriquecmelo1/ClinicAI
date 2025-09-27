import os
from dotenv import load_dotenv

from pymongo import AsyncMongoClient



load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

client = AsyncMongoClient(MONGO_URI)
db = client.ClinicAI

