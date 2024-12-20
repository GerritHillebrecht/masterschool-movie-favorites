from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from schemas import Movie, Director, User
from utils.decorators import handle_exceptions
from utils.filter import filter_valid_fields


def register_endpoints(app, api_path: str, data_manager):
    @app.get(f"{api_path}/users")
    @handle_exceptions
    def get_users():
        users = data_manager.get_all_users()
        return jsonify([user.to_dict() for user in users]), 200

    @app.post(f"{api_path}/users")
    @handle_exceptions
    def add_user():
        body = request.get_json()

        if not body:
            raise BadRequest("No JSON content found in the request.")

        # Filter valid fields for the Movie model
        valid_fields = filter_valid_fields(User, body)

        # Create a new Movie using the filtered fields
        user = User(**valid_fields)

        return jsonify(data_manager.add_user(user).to_dict()), 201

    @app.get(f"{api_path}/users/<int:user_id>")
    @handle_exceptions
    def get_movies(user_id: int):
        movies = data_manager.get_user_movies(user_id)
        return jsonify([movie.to_dict() for movie in movies]), 200

    @app.post(f"{api_path}/users/<int:user_id>")
    @handle_exceptions
    def add_movie(user_id: int):
        body = request.get_json()

        if not body:
            raise BadRequest("No JSON content found in the request.")

        # Filter valid fields for the Movie model
        valid_fields = filter_valid_fields(Movie, {
            **body,
            "user_id": user_id
        })

        # Create a new Movie using the filtered fields
        movie = Movie(**valid_fields)

        return jsonify(data_manager.add_movie(movie).to_dict()), 201

    @app.put(f"{api_path}/users/<int:user_id>/update_movie/<int:movie_id>")
    @handle_exceptions
    def update_movie(user_id: int, movie_id: int):
        body = request.get_json()
        updated_movie = data_manager.update_movie(body, user_id, movie_id)

        return jsonify(updated_movie.to_dict()), 200

    @app.delete(f"{api_path}/users/<int:user_id>/delete_movie/<int:movie_id>")
    @handle_exceptions
    def delete_movie(user_id: int, movie_id: int):
        return data_manager.delete_movie(movie_id), 204

    @app.get(f"{api_path}/directors")
    @handle_exceptions
    def get_directors():
        directors = data_manager.get_all_directors()

        return jsonify([director.to_dict() for director in directors]), 200

    @app.post(f"{api_path}/directors")
    @handle_exceptions
    def add_director():
        body = request.get_json()

        if not body:
            raise BadRequest("No JSON content found in the request.")

        # Filter valid fields for the Movie model
        valid_fields = filter_valid_fields(Director, body)

        # Create a new Movie using the filtered fields
        director = Director(**valid_fields)

        return jsonify(data_manager.add_director(director).to_dict()), 200
