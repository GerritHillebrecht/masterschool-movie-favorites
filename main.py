import logging
from os import path

from flask import Flask
from flask_cors import CORS
from pbu import Logger

from api import static_routes, api_routes
from config import load_config, get_log_folder
from datamanager import SQLiteDataManager

logging.basicConfig()
logging.getLogger('sqlalchemy.engine')
config = load_config()


def create_app():
    basedir = path.abspath(path.dirname(__file__))
    filedir = f'sqlite:///{path.join(basedir, "database", config.get("SQLITE_DATABASE_FILE"))}'
    api_path = f'/{config.get("API_PATH")}/{config.get("API_VERSION")}'

    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = filedir

    CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

    data_manager = SQLiteDataManager(flask_app)

    static_routes.register_endpoints(flask_app, data_manager)
    api_routes.register_endpoints(flask_app, api_path, data_manager)

    return flask_app


app = create_app()

if __name__ == "__main__":
    logger = Logger("MAIN", log_folder=get_log_folder())
    logger.info("==========================================")
    logger.info("           Starting application")
    logger.info("==========================================")
    app.run("0.0.0.0", port=5002, debug=True)
