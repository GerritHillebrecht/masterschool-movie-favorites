import os

from dotenv import load_dotenv

DEFAULTS = {
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
        "SECRET_KEY": os.environ.get('SECRET_KEY') or 'MY_GOD_THIS_IS_SO_SECRET_HOW_WILL_THEY_KNOW',
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


def is_debug():
    config = load_config()
    return config["IS_DEBUG"]
