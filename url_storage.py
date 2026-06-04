import os
import json

URLS_STORAGE_FILE = "urls_storage.json"

def load_urls_storage():
    if os.path.exists(URLS_STORAGE_FILE):
        with open(URLS_STORAGE_FILE, "r") as file:
            return json.load(file)
    return {}


def save_urls_storage(data):
    with open(URLS_STORAGE_FILE, "w") as file:
        json.dump(data, file)

urls_storage = load_urls_storage()