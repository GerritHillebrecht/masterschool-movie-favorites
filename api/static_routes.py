from flask import render_template

from config import is_debug
from utils.decorators import handle_exceptions


def register_endpoints(app, datamanger):
    """
    Registers all the endpoints used by the frontend to deliver the index.html in all cases.
    :param app: the flask app
    """

    @app.route("/", methods=["GET"])
    def get_index():
        """
        :return: the home.html as file
        """
        return render_template("home.html"), 200

    @app.get("/users")
    def get_users_view():
        users = datamanger.get_all_users()
        return render_template("users.html", users=users)

    @app.get("/users/<int:user_id>")
    @handle_exceptions
    def get_user_movies(user_id: int):
        try:
            movies = datamanger.get_user_movies(user_id)
            user = datamanger.get_user(user_id)

            return render_template("user_movies.html", movies=movies, user=user)
        except Exception:
            return render_template("user_movies.html", movies=[], user={})

    @app.get("/search")
    def get_ai_recommendation():
        return render_template("search.html")

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
