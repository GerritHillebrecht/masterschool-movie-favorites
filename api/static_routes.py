from flask import render_template, request, jsonify
from sqlalchemy.exc import NoResultFound
from config import is_debug
import requests


def register_endpoints(app, datamanager):
    """
    Registers all the endpoints used by the frontend to deliver the index.html in all cases.
    :param app: the flask app
    :param datamanager: Class to access database.
    """

    @app.get("/")
    def get_index():
        """
        :return: the home.html as file
        """
        users = datamanager.get_all_users()
        return render_template("home.html", users=users), 200

    @app.get("/users")
    def get_users_view():
        users = datamanager.get_all_users()
        return render_template("users.html", users=users)

    @app.get("/users/add")
    def add_user_form():
        return render_template("add_user.html")

    @app.get("/add-movie")
    def add_movie_form():
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

        users = datamanager.get_all_users()

        return render_template("add_movie.html", movie=movie, **movie, users=users)

    @app.get("/users/<int:user_id>")
    def get_user_movies(user_id: int):
        try:
            movies = datamanager.get_user_movies(user_id)
            user = datamanager.get_user(user_id)

            return render_template("user_movies.html", movies=movies, user=user)
        except NoResultFound as e:
            return render_template("user_movies.html", movies=[], user={})

    @app.get("/search")
    def search_movies():
        return render_template("search.html")

    @app.get("/movie/<int:movie_id>")
    def get_movie_by_id(movie_id: int):
        movie = datamanager.get_movie_by_id(movie_id)
        return render_template("movie_detail.html", movie=movie)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # prevent caching of the frontend during development
    if is_debug():
        @app.after_request
        def add_header(r):
            """
            Add headers to both force latest IE rendering engine or Chrome Frame,
            and also to cache the rendered page for 10 minutes.
            """
            r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            r.headers["Pragma"] = "no-cache"
            r.headers["Expires"] = "0"
            r.headers['Cache-Control'] = 'public, max-age=0'
            return r
