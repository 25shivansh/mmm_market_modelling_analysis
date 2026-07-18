import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from dotenv import load_dotenv

class MongoDBManager:
    """Manages the MongoDB connection as a singleton instance."""
    
    _instance: Optional['MongoDBManager'] = None
    
    def __new__(cls) -> 'MongoDBManager':
        if cls._instance is None:
            cls._instance = super(MongoDBManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self) -> None:
        if self._initialized:
            return
            
        load_dotenv()
        self._uri = self._validate_connection_string()
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._db_name = "marketmind_ai"
        self._initialized = True

    def _validate_connection_string(self) -> str:
        """
        Validates that MONGODB_URI is present in the environment variables.
        
        Raises:
            ValueError: If MONGODB_URI is not set or is empty.
            
        Returns:
            str: The MongoDB connection string.
        """
        uri = os.environ.get("MONGODB_URI")
        if not uri or not uri.strip():
            raise ValueError("MONGODB_URI environment variable is not set or is empty.")
        return uri.strip()

    def connect(self) -> Database:
        """
        Establishes connection to MongoDB and verifies connectivity using ping.
        Reuses the existing connection if already connected.
        
        Returns:
            Database: The connected database instance.
            
        Raises:
            ConnectionError: If connection or authentication fails.
        """
        if self._client is not None and self._db is not None:
            return self._db

        try:
            self._client = MongoClient(self._uri)
            # Verify connectivity
            self._client.admin.command('ping')
            self._db = self._client[self._db_name]
            return self._db
        except OperationFailure as e:
            self._client = None
            raise ConnectionError(f"MongoDB authentication failed: {e}") from e
        except (ConnectionFailure, ConfigurationError) as e:
            self._client = None
            raise ConnectionError(f"Failed to connect to MongoDB: {e}") from e
        except Exception as e:
            self._client = None
            raise ConnectionError(f"An unexpected error occurred during MongoDB connection: {e}") from e

    def get_database(self) -> Database:
        """
        Returns the connected database instance.
        
        Returns:
            Database: The active database instance.
            
        Raises:
            ConnectionError: If the connection has not been established yet.
        """
        if self._db is None:
            raise ConnectionError("Database connection not established. Call connect() first.")
        return self._db

    def get_collection(self, collection_name: str) -> Collection:
        """
        Returns the requested MongoDB collection.
        
        Args:
            collection_name (str): The name of the collection to retrieve.
            
        Returns:
            Collection: The requested collection.
            
        Raises:
            TypeError: If collection_name is not a string.
            ValueError: If collection_name is invalid or empty.
            ConnectionError: If the connection has not been established.
        """
        if not isinstance(collection_name, str):
            raise TypeError(f"collection_name must be a string, got {type(collection_name).__name__}.")
        if not collection_name or not collection_name.strip():
            raise ValueError("collection_name cannot be empty or whitespace.")
            
        db = self.get_database()
        return db[collection_name.strip()]

    def close(self) -> None:
        """Closes the MongoClient cleanly."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
