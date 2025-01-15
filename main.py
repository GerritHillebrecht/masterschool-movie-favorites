"""
This app took way longer than it should have, so no responsiveness is included, so I can finally finish it.
"""
import logging
from os import path

from flask import Flask, request
from flask_cors import CORS
from flask_login import LoginManager, current_user
from pbu import Logger

from config import load_config, get_log_folder
from datamanager import SQLiteDataManager
from routes import static_routes, api_routes, auth_routes
from schemas import User

logging.basicConfig()
logging.getLogger('sqlalchemy.engine')


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        flask_app (Flask): The configured Flask application.
    """
    config = load_config()

    basedir = path.abspath(path.dirname(__file__))
    filedir = f'sqlite:///{path.join(basedir, "database", "movie_library.sqlite")}'

    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = filedir
    flask_app.config["SECRET_KEY"] = config.get("SECRET_KEY")

    CORS(flask_app, resources={r"/routes/*": {"origins": "*"}})

    @flask_app.context_processor
    def inject_current_path():
        """
        Inject the current request path into the context.

        Returns:
            dict: A dictionary containing the current path.
        """
        return {'current_path': request.path}

    @flask_app.context_processor
    def inject_current_user():
        """
        Inject the current user into the context.

        Returns:
            dict: A dictionary containing the current user.
        """
        return {"current_user": current_user}

    flask_app.register_blueprint(static_routes)
    flask_app.register_blueprint(api_routes)
    flask_app.register_blueprint(auth_routes)

    login_manager = LoginManager()
    login_manager.init_app(flask_app)
    login_manager.login_view = "auth.get_login"
    flask_app.login_manager = login_manager

    @login_manager.user_loader
    def load_user(user_id):
        """
        Load a user by their user ID.

        Args:
            user_id (int): The ID of the user to load.

        Returns:
            User: The loaded user.
        """
        return User.query.get(int(user_id))

    data_manager = SQLiteDataManager(flask_app)
    flask_app.data_manager = data_manager

    return flask_app


app = create_app()

if __name__ == "__main__":
    logger = Logger("MAIN", log_folder=get_log_folder())
    logger.info("==========================================")
    logger.info("           Starting application")
    logger.info("==========================================")
    app.run("0.0.0.0", port=3000, debug=True)
