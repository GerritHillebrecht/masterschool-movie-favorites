from database.extensions import db
from schemas import User, Movie, Director
from .data_manager_interface import DataMangerInterface


class SQLiteDataManager(DataMangerInterface):

    def __init__(self, app=None):
        """
        Initializes the database using the current flask-app instance.
        :param app: The instance of the flask-app.
        """
        if app:
            db.init_app(app)

            with app.app_context():
                db.create_all()

    def get_all_users(self) -> list[User]:
        """
        Returns all users from the database.
        """
        return db.session.query(User).all()

    def get_user_movies(self, user_id) -> list[Movie]:
        """
        Returns all movies of specified user.
        :param user_id: The id of the user to fetch the movies for.
        :return: The movies of this user.
        """
        return db.session.query(Movie).join(Director).filter(Movie.user_id == user_id).all()

    def get_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        return db.session.query(User).filter(User.id == user_id).one()

    def add_user(self, user: User) -> User:
        """
        Adds a user to the database.
        :param user: A user item of type <User>
        :return: The newly created user as a json object.
        """
        return self._add_instance(user, User)

    def add_movie(self, movie: Movie) -> Movie:
        """
        Adds a movie to the database.
        :param movie: A movie item of type <Movie>
        :return: The newly created movie as a json object.
        """
        return self._add_instance(movie, Movie)

    def get_all_directors(self) -> list[Director]:
        """
        Fetches all directors and returns them.
        :return: list[dict]
        """
        return db.session.query(Director).join(Movie).all()

    def add_director(self, director: Director) -> Director:
        """
        Adds a director to the database.
        :param director: A director item of type <Director>
        :return: The newly created director as a json object.
        """
        return self._add_instance(director, Director)

    def update_movie(self, updated_movie_data, user_id: int, movie_id: int) -> Movie:
        db_movie = db.session.query(Movie).filter(Movie.id == movie_id).one()

        if not db_movie:
            raise ValueError(f"Movie {movie_id} not found!")

        for key, value in updated_movie_data.items():
            if hasattr(db_movie, key):
                setattr(db_movie, key, value)

        db.session.commit()

        return db_movie

    def delete_movie(self, movie_id):
        movie = db.session.query(Movie).filter(Movie.id == movie_id).one()

        if not movie:
            raise ValueError(f"Movie {movie_id} not found!")

        db.session.delete(movie)
        db.session.commit()

        return movie

    @staticmethod
    def _add_instance(item, item_type):
        # Validity check
        if not isinstance(item, item_type):
            raise ValueError(f"{item} is not of type {item_type}")

        # Add item to db
        db.session.add(item)
        db.session.commit()

        return item