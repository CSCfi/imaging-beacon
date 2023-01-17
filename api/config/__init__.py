"""Configuration Module."""
from os import getenv
from sys import exit
from json import loads
from distutils.util import strtobool
from datetime import datetime
from typing import Dict


def load_json(path: str) -> Dict:
    """Load JSON file to a dictionary object."""
    try:
        with open(path, "r") as f:
            info = loads(f.read())
            info["updateDateTime"] = datetime.now().replace(microsecond=0).isoformat()
            return info
    except Exception as e:
        exit(f"failed to read info file {path}, reason: {e}")


APP: Dict = {
    "host": getenv("APP_HOST", "0.0.0.0"),
    "port": getenv("APP_PORT", "8080"),
    "cors": bool(strtobool(getenv("APP_CORS", "False"))),
    "info": load_json(getenv("APP_INFO", "api/config/info.json")),
}

DB: Dict = {
    "host": getenv("DB_HOST", "localhost"),
    "port": getenv("DB_PORT", 27017),
    "name": getenv("DB_NAME", "beacon"),
    "auth": getenv("DB_AUTH", "admin"),
    "username": getenv("DB_USERNAME", "username"),
    "password": getenv("DB_PASSWORD", "password"),
}
DB["uri"] = f"mongodb://{DB['username']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['name']}?authSource={DB['auth']}"
