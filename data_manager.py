from abc import ABC, abstractmethod

from flask import jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, DataError, OperationalError

from data_schemas import User, Movie, Director
from database.extensions import db


class DataMangerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def add_movie(self, movie: Movie):
        pass

    @abstractmethod
    def add_director(self, director: Director):
        pass

    @abstractmethod
    def update_movie(self, movie: Movie):
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        pass


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

    def add_director(self, director: Director) -> Director:
        """
        Adds a director to the database.
        :param director: A director item of type <Director>
        :return: The newly created director as a json object.
        """
        return self._add_instance(director, Director)

    def update_movie(self, movie: Movie):
        db_movie = db.session.query(Movie).filter(Movie.id == movie.id).one()

        if not db_movie:
            return jsonify({"message": "User not found!"}), 404

        for key, value in db_movie.items():
            if hasattr(db_movie, key):
                setattr(db_movie, key, value)

        db.session.commit()

    def delete_movie(self, movie_id):
        movie = db.session.query(Movie).filter(Movie.id == movie_id).one()

        if not movie:
            return jsonify({"message": "User not found!"}), 404

        self._database_operation(db.session.delete, movie)

        return jsonify({
            "message": f"Movie with id {movie_id} deleted successfully"
        }), 200

    def _add_instance(self, item, item_type):
        # Validity check
        if not isinstance(item, item_type):
            raise ValueError(f"{item} is not of type {item_type}")

        # Add item to db
        self._database_operation(db.session.add, item)

        # Return updated item (including id and datestamps)
        return item

    def _database_operation(self, db_operation, item):
        try:
            db_operation(item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Integrity error - Possible duplicate entry"}), 400
        except DataError:
            db.session.rollback()
            return jsonify({"error": "Data error - Invalid data format or value"}), 400
        except OperationalError:
            db.session.rollback()
            return jsonify({"error": "Operational error - Operational issue such as NOT NULL constraint"}), 500
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

        return item
