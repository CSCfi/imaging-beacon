"""Big picture Python Application Configuration."""

import json
from os import environ
from configparser import ConfigParser
from collections import namedtuple
from distutils.util import strtobool
from pathlib import Path

from typing import Any, Dict, List, Union

def convert(dictionary: Dict) -> tuple:
    """Convert dictionary to Named tuple."""
    return namedtuple("Config", dictionary.keys())(**dictionary)

def parse_drspaths(paths: str) -> List[List[str]]:
    """Parse handover configuration."""
    return [p.strip().split(",", 2) for p in paths.split("\n") if p.split()]

def parse_config_file(path) -> Any:
    """Parse configuration file."""
    config = ConfigParser()
    config.read(path)
    config_vars: Dict[str, Union[str, int, List[List[str]]]] = {
        "title": config.get("beacon_general_info", "title"),
        "version": config.get("beacon_general_info", "version"),
        "author": config.get("beacon_general_info", "author"),
        "license": config.get("beacon_general_info", "license"),
        "copyright": config.get("beacon_general_info", "copyright"),
        "docs_url": config.get("beacon_general_info", "docs_url"),
        "handover_drs": config.get("handover_info", "drs", fallback=""),
        "handover_datasets": parse_drspaths(config.get("handover_info", "dataset_paths", fallback="")),
        "handover_beacon": parse_drspaths(config.get("handover_info", "beacon_paths", fallback="")),
        "handover_base": int(config.get("handover_info", "handover_base", fallback=0)),
        "apiVersion": config.get("beacon_api_info", "apiVersion"),
        "beaconId": config.get("beacon_api_info", "beaconId"),
        "description": config.get("beacon_api_info", "description"),
        "url": config.get("beacon_api_info", "url"),
        "alturl": config.get("beacon_api_info", "alturl"),
        "createtime": config.get("beacon_api_info", "createtime"),
        "service_group": config.get("beacon_api_info", "service_group"),
        "service_artifact": config.get("beacon_api_info", "service_artifact"),
        "environment": config.get("beacon_api_info", "environment"),
        "org_id": config.get("organisation_info", "org_id"),
        "org_name": config.get("organisation_info", "org_name"),
        "org_description": config.get("organisation_info", "org_description"),
        "org_address": config.get("organisation_info", "org_address"),
        "org_welcomeUrl": config.get("organisation_info", "org_welcomeUrl"),
        "org_contactUrl": config.get("organisation_info", "org_contactUrl"),
        "org_logoUrl": config.get("organisation_info", "org_logoUrl"),
        "org_info": config.get("organisation_info", "org_info"),
    }
    return convert(config_vars)


CONFIG_INFO = parse_config_file(environ.get("CONFIG_FILE", str(Path(__file__).resolve().parent.joinpath("config.ini"))))