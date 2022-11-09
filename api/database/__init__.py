"""Database functions."""
from pymongo import MongoClient


def create_db_client(uri):
    """Connect to database and return db client."""
    return MongoClient(uri)
