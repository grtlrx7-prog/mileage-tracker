import json
import os

CACHE_PATH = "backend/exports/clean_trips.json"

_cache = {}


# =================================================
# LOAD CACHE
# =================================================

def load_clean_cache():

    global _cache

    try:

        if os.path.exists(CACHE_PATH):

            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                _cache = json.load(f)

        else:
            _cache = {}

    except:
        _cache = {}


# =================================================
# SAVE CACHE
# =================================================

def save_clean_cache():

    try:

        # ensure exports folder exists
        os.makedirs(
            os.path.dirname(CACHE_PATH),
            exist_ok=True
        )

        with open(CACHE_PATH, "w", encoding="utf-8") as f:

            json.dump(
                _cache,
                f,
                indent=2,
                ensure_ascii=False
            )

    except Exception as e:

        print("CACHE SAVE ERROR:", e)


# =================================================
# GET
# =================================================

def get_cached_address(key):

    return _cache.get(key)


# =================================================
# SET
# =================================================

def set_cached_address(key, value):

    _cache[key] = value