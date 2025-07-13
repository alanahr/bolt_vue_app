import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import asyncio
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
        self.is_connected = False

    async def connect(self):
        """Connect to MongoDB"""
        try:
            uri = os.getenv("MONGODB_URI", "mongodb://admin:password123@mongodb:27017/vue_crud_db?authSource=admin")
            db_name = os.getenv("MONGODB_DB_NAME", "vue_crud_db")

            print("🔌 Connecting to MongoDB...")
            
            self.client = AsyncIOMotorClient(
                uri,
                maxPoolSize=10,
                serverSelectionTimeoutMS=5000,
                socketTimeoutMS=45000,
            )

            # Test the connection
            await self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.is_connected = True

            print("✅ Connected to MongoDB successfully")
            print("🏓 MongoDB ping successful")

            return self.db
        except ConnectionFailure as e:
            print(f"❌ MongoDB connection error: {e}")
            self.is_connected = False
            raise e

    async def disconnect(self):
        """Disconnect from MongoDB"""
        try:
            if self.client:
                self.client.close()
                self.is_connected = False
                print("🔌 Disconnected from MongoDB")
        except Exception as e:
            print(f"❌ Error disconnecting from MongoDB: {e}")
            raise e

    def get_db(self):
        """Get database instance"""
        if not self.is_connected or not self.db:
            raise ConnectionError("Database not connected. Call connect() first.")
        return self.db

    def is_ready(self):
        """Check if database is ready"""
        return self.is_connected and self.db is not None

# Create singleton instance
database = Database()