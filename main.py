import logging
from os import path, environ

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from data_manager import SQLiteDataManager
from data_schemas import Movie, Director, User
from database.extensions import db
from utils.filter import filter_valid_fields

logging.basicConfig()
logging.getLogger('sqlalchemy.engine')
load_dotenv()


def create_app():
    basedir = path.abspath(path.dirname(__file__))
    filedir = f'sqlite:///{path.join(basedir, "database", environ.get("SQLITE_DATABASE_FILE"))}'

    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = filedir

    CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

    return flask_app


app = create_app()
dataManager = SQLiteDataManager(app)


@app.get("/")
def home():
    return render_template("home.html"), 200


@app.get("/api/v1/users")
def get_users():
    return dataManager.get_all_users(), 200


@app.post("/api/v1/users")
def add_user():
    body = request.get_json()

    if not body:
        raise BadRequest("No JSON content found in the request.")

    # Filter valid fields for the Movie model
    valid_fields = filter_valid_fields(User, body)

    # Create a new Movie using the filtered fields
    user = User(**valid_fields)

    print("[DEBUG] [FLASK API] user: ", user)

    return jsonify(dataManager.add_user(user).to_dict()), 200


@app.get("/api/v1/movies")
def get_movies():
    return db.session.query(Movie).join(Director).all(), 200


@app.post("/api/v1/movies")
def add_movie():
    body = request.get_json()

    if not body:
        raise BadRequest("No JSON content found in the request.")

    # Filter valid fields for the Movie model
    valid_fields = filter_valid_fields(Movie, body)

    # Create a new Movie using the filtered fields
    movie = Movie(**valid_fields)

    return dataManager.add_movie(movie), 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=5002, debug=True)
