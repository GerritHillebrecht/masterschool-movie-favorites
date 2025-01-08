import requests
from flask import render_template, request, Blueprint, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound

from config import is_debug
from forms import MovieForm
from schemas import Movie

from utils.filter import filter_valid_fields
from dateutil import parser

static_routes = Blueprint("static_routes", __name__)


@static_routes.get("/")
@login_required
def get_index():
    """
    :return: the home.html as file
    """
    try:
        movies = current_app.data_manager.get_user_movies(current_user.id)
        movies_sorted_rating = list(sorted(movies, key=lambda m: m.rating, reverse=True))
        movies_sorted_upcoming = list(sorted(movies, key=lambda m: m.updated_at, reverse=True))
        return render_template(
            "user_movies.html",
            movies=movies,
            movies_sorted_rating=movies_sorted_rating[:10],
            movies_sorted_upcoming=movies_sorted_upcoming[:5],
            user=current_user
        )
    except NoResultFound as e:
        return redirect(url_for("static_routes.search_movies"))


@static_routes.get("/calendar")
@login_required
def get_calendar():
    return render_template("calendar.html")


@static_routes.get("/users")
@login_required
def get_users_view():
    users = current_app.data_manager.get_all_users()
    return render_template("users.html", users=users)


@static_routes.get('/docs')
@login_required
def custom_swagger_ui():
    return render_template('swagger_ui_with_navbar.html')


@static_routes.route("/add-movie", methods=["GET", "POST"])
@login_required
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

    form = MovieForm()

    if request.method == "GET":
        form.plot.data = movie["Plot"]

    if form.validate_on_submit():
        rating = next(
            float(rating["Value"].split("/")[0])
            for rating in movie["Ratings"]
            if rating["Source"] == "Internet Movie Database"
        )

        watch_date = parser.parse(f"{form.watch_date.data} {form.watch_time.data}")

        keys = ["Actors", "Writer", "Awards", "BoxOffice", "Genre", "Director", "Year"]
        valid_fields = filter_valid_fields(Movie, {
            **{
                key.lower(): movie.get(key, "")
                for key in keys
            },
            **{
                "name": form.name.data,
                "plot": form.plot.data,
                "poster": form.poster.data,
                "watch_date": watch_date,
                "runtime": movie.get("Runtime", 90),
                "rating": rating or 5,
            },
            "user_id": current_user.id
        })

        new_movie = Movie(**valid_fields)
        current_app.data_manager.add_movie(new_movie)
        return redirect(url_for("static_routes.get_index"))

    return render_template("add_movie.html", movie=movie, **movie, form=form)


@static_routes.get("/users/<int:user_id>")
@login_required
def get_user_movies(user_id: int):
    try:
        movies = current_app.data_manager.get_user_movies(user_id)
        user = current_app.data_manager.get_user(user_id)

        return render_template("user_movies.html", movies=movies, user=user)
    except NoResultFound as e:
        return render_template("user_movies.html", movies=[], user={})


@static_routes.get("/search")
@login_required
def search_movies():
    return render_template("search.html")


@static_routes.get("/movie/<int:movie_id>")
@login_required
def get_movie_by_id(movie_id: int):
    movie = current_app.data_manager.get_movie_by_id(movie_id)
    return render_template("movie_detail.html", movie=movie)


@static_routes.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# prevent caching of the frontend during development
if is_debug():
    @static_routes.after_request
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
