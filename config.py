import os

from dotenv import load_dotenv

DEFAULTS = {
    # "MYSQL_HOST": "localhost",
    # "MYSQL_USERNAME": "myuser",
    # "MYSQL_PASSWORD": "mypassword",
    # "MYSQL_DATABASE": "mydatabase",
    # "MONGO_URL": "mongodb://localhost:27017",
    # "MONGO_DB": "mydatabase",

    "LOG_FOLDER": "_logs",
    "IS_DEBUG": False,
}

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


def load_config():
    # read out existing os environment
    load_dotenv()
    config = {
        "API_PATH": os.getenv("API_PATH"),
        "API_VERSION": os.getenv("API_VERSION"),
        # "MYSQL_HOST": os.getenv("MYSQL_HOST", "localhost"),
        # "MYSQL_USERNAME": os.getenv("MYSQL_USERNAME"),
        # "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
        # "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE"),
        # "MONGO_URL": os.getenv("MONGO_URL"),
        # "MONGO_DB": os.getenv("MONGO_DB"),
        "SQLITE_DATABASE_FILE": os.environ.get("SQLITE_DATABASE_FILE"),

        "LOG_FOLDER": os.getenv("LOG_FOLDER"),
        "IS_DEBUG": os.getenv("IS_DEBUG") == "1",
    }

    # apply defaults for missing config params
    for key in DEFAULTS:
        if key not in config or config[key] is None:
            config[key] = DEFAULTS[key]

    # check if log folder exists
    if not os.path.isdir(config["LOG_FOLDER"]):
        os.mkdir(config["LOG_FOLDER"])

    return config


def get_log_folder():
    config = load_config()
    return config["LOG_FOLDER"]


def get_mysql_config():
    config = load_config()
    return config["MYSQL_HOST"], config["MYSQL_DATABASE"], config["MYSQL_USERNAME"], config["MYSQL_PASSWORD"]


def get_mongodb_config():
    config = load_config()
    return config["MONGO_URL"], config["MONGO_DB"]


def is_debug():
    config = load_config()
    return config["IS_DEBUG"]
