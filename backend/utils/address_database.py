import json
import os

DB_FILE = "backend/data/address_database.json"

database = {}


# =================================================
# LOAD
# =================================================

def load_database():

    global database

    try:

        if os.path.exists(DB_FILE):

            with open(
                DB_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                database = json.load(f)

        else:

            database = {}

    except:

        database = {}


# =================================================
# SAVE
# =================================================

def save_database():

    try:

        with open(
            DB_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                database,
                f,
                indent=2,
                ensure_ascii=False
            )

    except Exception as e:

        print("DATABASE SAVE ERROR:", e)


# =================================================
# GET
# =================================================

def get_database_address(key):

    return database.get(key)


# =================================================
# SET
# =================================================

def set_database_address(key, value):

    database[key] = value