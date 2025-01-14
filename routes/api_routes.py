import requests
from flask import request, jsonify, Blueprint, current_app, render_template, redirect, url_for
from flask_login import current_user, login_required
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import BadRequest

from forms import MovieForm

from config import load_config
from schemas import Movie, Director, User
from utils.decorators import handle_exceptions
from utils.filter import filter_valid_fields

from dateutil import parser
from datetime import timedelta

config = load_config()

SWAGGER_URL = '/api/v1/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Filmster API"}
)

api_path = f'/{config.get("API_PATH")}/{config.get("API_VERSION")}'
api_routes = Blueprint("routes", __name__)
api_routes.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@api_routes.post(f"{api_path}/movies")
@handle_exceptions
def add_movie_to_db():
    form = MovieForm()

    if form.validate_on_submit():
        try:
            movie_title = request.args.get("title")
            response = requests.get(f"http://www.omdbapi.com/?apikey=6999413f&t={movie_title}")
            response.raise_for_status()
            movie = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error accessing API: {e}")
            return render_template("add_movie.html", error=e)
        except ValueError as e:
            print(f"Error accessing movie title: {e}")
            return render_template("add_movie.html", not_found=True)

        valid_fields = filter_valid_fields(Movie, {
            **{
                "actors": movie.Actors,
                "writers": movie.Writers,
                "awards": movie.Awards,
                "boxOffice": movie.BoxOffice,
                "genre": movie.Genre,
                "directors": movie.Directors,
                "release_year": movie.Year
            },
            **form,
            "user_id": current_user.id
        })

        current_app.data_manager.add_movie(valid_fields)

        return redirect(url_for("static_routes.add_movie_form"))

    return redirect(url_for("static_routes.get_index"))


@api_routes.get(f"{api_path}/users")
@handle_exceptions
def get_users():
    users = current_app.data_manager.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


@api_routes.get(f"{api_path}/calendar")
@handle_exceptions
@login_required
def get_calendar_evets():
    movies = current_app.data_manager.get_user_movies(current_user.id)

    return jsonify([
        {
            "movie_id": movie.id,
            "title": movie.name,
            "start": str(movie.watch_date),
            "end": str(parser.parse(movie.watch_date.isoformat()) + timedelta(minutes=int(movie.runtime))),
            "editable": True
        }
        for movie in movies
    ]), 200


@api_routes.post(f"{api_path}/calendar/update")
@handle_exceptions
def update_movie_by_calendar():
    body = request.get_json()
    movie_id = body.get("movie_id")
    movie_date = body.get("movie_date")

    if not movie_id or not movie_date:
        return jsonify({
            "message": "Missing data in your request"
        }), 404

    movie_date = parser.parse(movie_date)

    print(movie_id, current_user.id, movie_date)
    updated_movie = current_app.data_manager.update_movie({"watch_date": movie_date}, current_user.id, movie_id)

    print(updated_movie)
    return jsonify(updated_movie.to_dict()), 200


@api_routes.post(f"{api_path}/users")
@handle_exceptions
def add_user():
    body = request.get_json()

    if not body:
        raise BadRequest("No JSON content found in the request.")

    # Filter valid fields for the Movie model
    valid_fields = filter_valid_fields(User, body)

    # Create a new Movie using the filtered fields
    user = User(**valid_fields)

    return jsonify(current_app.data_manager.add_user(user).to_dict()), 201


@api_routes.get(f"{api_path}/users/<int:user_id>")
@handle_exceptions
def get_movies(user_id: int):
    movies = current_app.data_manager.get_user_movies(user_id)
    return jsonify([movie.to_dict() for movie in movies]), 200


@api_routes.post(f"{api_path}/users/<int:user_id>")
# @handle_exceptions
def add_movie(user_id: int):
    body = request.get_json()

    try:
        user = current_app.data_manager.get_user(user_id)
    except Exception:
        return jsonify({
            "message": "User id does not exist."
        })

    if not user:
        return jsonify({
            "message": "User id does not exist."
        })

    if not body:
        raise BadRequest("No JSON content found in the request.")

    # Filter valid fields for the Movie model
    valid_fields = filter_valid_fields(Movie, {
        **body,
        "user_id": user_id
    })

    # Create a new Movie using the filtered fields
    movie = Movie(**valid_fields)

    print(movie)

    return jsonify(current_app.data_manager.add_movie(movie).to_dict()), 201


@api_routes.put(f"{api_path}/users/<int:user_id>/update_movie/<int:movie_id>")
@handle_exceptions
def update_movie(user_id: int, movie_id: int):
    body = request.get_json()
    updated_movie = current_app.data_manager.update_movie(body, user_id, movie_id)

    return jsonify(updated_movie.to_dict()), 200


@api_routes.delete(f"{api_path}/delete_movie/<int:movie_id>")
@handle_exceptions
def delete_movie(movie_id: int):
    return jsonify(current_app.data_manager.delete_movie(movie_id).to_dict()), 204


@api_routes.get(f"{api_path}/directors")
@handle_exceptions
def get_directors():
    directors = current_app.data_manager.get_all_directors()

    return jsonify([director.to_dict() for director in directors]), 200


@api_routes.post(f"{api_path}/directors")
@handle_exceptions
def add_director():
    body = request.get_json()

    if not body:
        raise BadRequest("No JSON content found in the request.")

    # Filter valid fields for the Movie model
    valid_fields = filter_valid_fields(Director, body)

    # Create a new Movie using the filtered fields
    director = Director(**valid_fields)

    return jsonify(current_app.data_manager.add_director(director).to_dict()), 200
