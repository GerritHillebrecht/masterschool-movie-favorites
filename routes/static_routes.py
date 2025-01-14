import string
from datetime import datetime

import humanize
import requests
from dateutil import parser
from flask import render_template, request, Blueprint, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound

from config import is_debug
from forms import MovieForm, UpdateMovieForm
from schemas import Movie
from utils.decorators import handle_no_search_results
from utils.filter import filter_valid_fields

static_routes = Blueprint("static_routes", __name__)


@static_routes.before_request
def check_browser():
    user_agent = request.headers.get('User-Agent')
    if 'Firefox' in user_agent:
        return render_template("/no_firefox.html")


@static_routes.get("/movies")
@login_required
def get_index():
    """
    :return: the home.html as file
    """
    try:
        movies = current_app.data_manager.get_user_movies(current_user.id)
        if len(movies) == 0:
            return redirect(url_for("static_routes.search_movies"))

        movies_sorted_rating = list(sorted(movies, key=lambda m: m.rating, reverse=True))
        movies_sorted_upcoming = list(
            sorted(
                [
                    movie
                    for movie in movies
                    if movie.watch_date > datetime.today()
                ],
                key=lambda m: m.watch_date,
                reverse=False
            )
        )

        relative_times = [
            humanize.naturaltime(datetime.now() - movie.watch_date)
            for movie in movies_sorted_upcoming
        ]

        return render_template(
            "user_movies.html",
            movies=movies,
            movies_sorted_rating=movies_sorted_rating[:10],
            movies_sorted_upcoming=movies_sorted_upcoming[:8],
            relative_times=relative_times,
            user=current_user
        )
    except NoResultFound as e:
        return redirect(url_for("static_routes.search_movies"))


@static_routes.get("/movies/all")
@login_required
def get_all_movies():
    movies = current_app.data_manager.get_user_movies(current_user.id)
    if len(movies) == 0:
        return redirect(url_for("static_routes.search_movies"))

    alphabet = string.ascii_letters
    sorted_movies = [
        item
        for item in [
            {
                "letter": letter,
                "movies": [movie for movie in movies if movie.name.startswith(letter)]
            }
            for letter in alphabet
        ]
        if item["movies"]
    ]

    print(sorted_movies)

    return render_template("all_movies.html", movies_list=sorted_movies)


@static_routes.get("/")
def get_landing_page():
    if current_user.is_anonymous:
        return render_template("home.html")

    return redirect("/movies")


@static_routes.get("/calendar")
@login_required
def get_calendar():
    return render_template("calendar.html")


@static_routes.get("/users")
@login_required
@handle_no_search_results
def get_users_view():
    users = current_app.data_manager.get_all_users()
    return render_template("users.html", users=users)


@static_routes.get('/docs')
@login_required
@handle_no_search_results
def custom_swagger_ui():
    return render_template('swagger_ui_with_navbar.html')


@static_routes.route("/add-movie", methods=["GET", "POST"])
@login_required
@handle_no_search_results
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

        response = requests.get(f'https://api.kinocheck.de/movies?imdb_id={movie.get("imdbID")}')
        response_json = response.json()
        trailer_data = response_json.get("trailer") or {}
        youtube_video_id = trailer_data.get("youtube_video_id", "")

        watch_date = parser.parse(f"{form.watch_date.data} {form.watch_time.data}")

        print("movie", movie)

        keys = ["Actors", "Writer", "Awards", "Genre", "Director"]
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
                "release_year": movie.get("Year", 0),
                "boxOffice": movie.get("BoxOffice", 0),
                "runtime": int(movie.get("Runtime", "90 min").split(" ")[0]),
                "rating": rating or 5,
                "youtube_video_id": youtube_video_id,
                "imdbId": movie.get("imdbID")
            },
            "user_id": current_user.id
        })

        new_movie = Movie(**valid_fields)
        current_app.data_manager.add_movie(new_movie)
        return redirect(url_for("static_routes.get_movie_by_id", movie_id=new_movie.id))

    return render_template("add_movie.html", movie=movie, **movie, form=form)


@static_routes.get("/users/<int:user_id>")
@login_required
@handle_no_search_results
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
@handle_no_search_results
def get_movie_by_id(movie_id: int):
    movie = current_app.data_manager.get_movie_by_id(movie_id)
    return render_template("movie_detail.html", movie=movie)


@static_routes.route("/movie/update/<int:movie_id>", methods=["GET", "POST"])
@login_required
@handle_no_search_results
def update_movie(movie_id: int):
    movie = current_app.data_manager.get_movie_by_id(movie_id)
    form = UpdateMovieForm()

    if request.method == "GET":
        form.name.data = movie.name
        form.director.data = movie.director
        form.poster.data = movie.poster
        form.genre.data = movie.genre
        form.actors.data = movie.actors
        form.writer.data = movie.writer
        form.awards.data = movie.awards
        form.boxOffice.data = movie.boxOffice
        form.plot.data = movie.plot
        form.youtube_video_id.data = movie.youtube_video_id
        form.runtime.data = movie.runtime
        form.imdbId.data = movie.imdbId
        form.release_year.data = movie.release_year

    if form.validate_on_submit():
        valid_fields = filter_valid_fields(Movie, form.data)
        current_app.data_manager.update_movie(valid_fields, current_user.id, movie_id)
        return redirect(url_for(f"static_routes.get_movie_by_id", movie_id=movie_id))

    return render_template("update_movie.html", movie=movie, form=form)


@static_routes.get("/movie/delete/<int:movie_id>")
@login_required
@handle_no_search_results
def delete_movie(movie_id: int):
    movie = current_app.data_manager.get_movie_by_id(movie_id)

    if movie.user_id == current_user.id:
        current_app.data_manager.delete_movie(movie_id)
        return redirect("/movies")

    return redirect("https://letmegooglethat.com/?q=Try+not+to+be+an+asshole")


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
