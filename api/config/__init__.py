"""Configuration Module."""
from os import getenv
from distutils.util import strtobool

APP = {
    "host": getenv("APP_HOST", "0.0.0.0"),
    "port": getenv("APP_PORT", "8080"),
    "cors": bool(strtobool(getenv("APP_CORS", "False"))),
}

DB = {
    "host": getenv("DB_HOST", "localhost"),
    "port": getenv("DB_PORT", 27017),
    "name": getenv("DB_NAME", "beacon"),
    "auth": getenv("DB_AUTH", "admin"),
    "username": getenv("DB_USERNAME", "username"),
    "password": getenv("DB_PASSWORD", "password"),
}
DB["uri"] = f"mongodb://{DB['username']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['name']}?authSource={DB['auth']}"
