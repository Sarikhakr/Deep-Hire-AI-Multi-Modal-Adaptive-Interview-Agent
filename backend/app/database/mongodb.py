from pymongo import MongoClient

# MongoDB Connection URL
MONGO_URI = "mongodb://localhost:27017"

# Create MongoDB Client
try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")   # Check connection
    db = client["deephire_ai"]
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)