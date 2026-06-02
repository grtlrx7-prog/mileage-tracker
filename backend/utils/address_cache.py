import json
import os

CACHE_FILE = "backend/exports/address_cache.json"

_cache = {}


def load_cache():
    global _cache

    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                _cache = json.load(f)
        except:
            _cache = {}


def save_cache():
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(_cache, f, indent=2)


def get_cached(key):
    return _cache.get(key)


def set_cached(key, value):
    _cache[key] = value