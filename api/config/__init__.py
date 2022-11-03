"""Configuration Module."""
from os import getenv

APP = {
    "host": getenv("APP_HOST", "0.0.0.0"),
    "port": getenv("APP_PORT", "8080"),
}

DB = {
    "host": getenv("DB_HOST", "localhost"),
    "port": getenv("DB_PORT", 27017),
    "name": getenv("DB_NAME", "beacon"),
    "auth": getenv("DB_AUTH", "admin"),
    "username": getenv("DB_USERNAME", "username"),
    "password": getenv("DB_PASSWORD", "password"),
}
