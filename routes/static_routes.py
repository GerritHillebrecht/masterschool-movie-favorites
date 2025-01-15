import string
from datetime import datetime, timedelta
from os import environ

import humanize
import requests
from dateutil import parser
from flask import render_template, request, Blueprint, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound

from forms import MovieForm, UpdateMovieForm
from schemas import Movie
from utils.decorators import handle_no_search_results
from utils.filter import filter_valid_fields

static_routes = Blueprint("static_routes", __name__)


@static_routes.before_request
def check_browser():
    """
    Checks the user's browser and renders a specific template if the browser is Firefox.
    """
    user_agent = request.headers.get('User-Agent')
    if 'Firefox' in user_agent:
        return render_template("/no_firefox.html")


@static_routes.get("/movies")
@login_required
def get_index():
    """
    Retrieves and sorts the user's movies for display on the home page.
    Returns:
        Rendered template with sorted movies and relative times.
    """
    try:
        movies = current_app.data_manager.get_user_movies(current_user.id)
        if len(movies) == 0:
            return redirect(url_for("static_routes.search_movies"))

        today = datetime.now()
        one_month_ago = today - timedelta(days=30)
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&language=en-US&page=1&primary_release_date.gte={one_month_ago.strftime('%Y-%m-%d')}&sort_by=popularity.desc"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {environ.get("TMDB_TOKEN")}"
        }

        response = requests.get(url, headers=headers)
        recommendations = [
            {
                "name": movie["title"],
                "poster": f"https://image.tmdb.org/t/p/original/{movie["poster_path"]}",
                "genre": "",
                "plot": movie["overview"]
            }
            for movie in response.json()["results"]
        ]

        print(recommendations)

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
        movies_sorted_seen = list(
            sorted(
                [
                    movie
                    for movie in movies
                    if movie.watch_date < datetime.today()
                ],
                key=lambda m: m.watch_date,
                reverse=True
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
            movies_sorted_upcoming=movies_sorted_upcoming[:10],
            movies_sorted_seen=movies_sorted_seen[:10],
            relative_times=relative_times,
            recommendations=recommendations,
            user=current_user
        )
    except NoResultFound as e:
        return redirect(url_for("static_routes.search_movies"))


@static_routes.get("/movies/all")
@login_required
def get_all_movies():
    """
    Retrieves all movies of the current user and sorts them alphabetically.
    Returns:
        Rendered template with sorted movies.
    """
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
    """
    Renders the landing page or redirects to the movies page if the user is authenticated.
    Returns:
        Rendered template or redirect.
    """
    if current_user.is_anonymous:
        return render_template("home.html")

    return redirect("/movies")


@static_routes.get("/calendar")
@login_required
def get_calendar():
    """
    Renders the calendar page.
    Returns:
        Rendered template for the calendar.
    """
    return render_template("calendar.html")


@static_routes.get("/users")
@login_required
@handle_no_search_results
def get_users_view():
    """
    Retrieves and displays all users.
    Returns:
        Rendered template with user data.
    """
    users = current_app.data_manager.get_all_users()
    return render_template("users.html", users=users)


@static_routes.get('/docs')
@login_required
@handle_no_search_results
def custom_swagger_ui():
    """
    Renders the custom Swagger UI with navbar.
    Returns:
        Rendered template for Swagger UI.
    """
    return render_template('swagger_ui_with_navbar.html')


@static_routes.route("/add-movie", methods=["GET", "POST"])
@login_required
@handle_no_search_results
def add_movie_form():
    """
    Adds a movie to the database using data from an external API and a form.
    Returns:
        Rendered template or redirect based on the result.
    """
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
    """
    Retrieves and displays movies for a specific user.
    Returns:
        Rendered template with the user's movies.
    """
    try:
        movies = current_app.data_manager.get_user_movies(user_id)
        user = current_app.data_manager.get_user(user_id)

        return render_template("user_movies.html", movies=movies, user=user)
    except NoResultFound as e:
        return render_template("user_movies.html", movies=[], user={})


@static_routes.get("/search")
@login_required
def search_movies():
    """
    Renders the movie search page.
    Returns:
        Rendered template for the search page.
    """
    return render_template("search.html")


@static_routes.get("/movie/<int:movie_id>")
@login_required
@handle_no_search_results
def get_movie_by_id(movie_id: int):
    """
    Retrieves and displays details for a specific movie.
    Returns:
        Rendered template with movie details.
    """
    movie = current_app.data_manager.get_movie_by_id(movie_id)
    return render_template("movie_detail.html", movie=movie)


@static_routes.route("/movie/update/<int:movie_id>", methods=["GET", "POST"])
@login_required
@handle_no_search_results
def update_movie(movie_id: int):
    """
    Updates details of a specific movie.
    Returns:
        Rendered template or redirect based on the result.
    """
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
