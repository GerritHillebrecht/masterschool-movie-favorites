"""
The data-structure has a one-to-many relationship between user and movie. This means that
Movies can have only one user/creator. This is on purpose, since the movies are pulled from an
external source and copied into the database. Duplications may happen this way, but this is not
a movie library, but an external "favorites list", kind of like the "my list" feature on netflix.
A duplication test could be done, but for this task it will stay one-to-many.
"""

from sqlalchemy import Column, Integer, Float, String, func
from sqlalchemy.orm import relationship

from database.extensions import db
from utils.base_model_schema import ToDictMixin

PLACEHOLDER_MOVIE_POSTER = "https://critics.io/img/movies/poster-placeholder.png"


class BaseModel(ToDictMixin, db.Model):
    """
    Custom Parent-class to extend from, easily extendable, especially useful
    for scalability. Inherits to_dict functionality.
    """
    __abstract__ = True


class User(BaseModel):
    """
    Represents a user in the system.

    Attributes:
        id (int): Unique ID of the user.
        firstname (str): First name of the user.
        lastname (str): Last name of the user.
        movies (list): List of movies associated with the user.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime):Timestamp when the user was last updated.
    """
    __tablename__ = "users"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"<User(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, created_at={self.created_at}, updated_at={self.updated_at})>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    movies = db.relationship('Movie', back_populates='user', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())


class Movie(BaseModel):
    """
    Represents a movie in the system.

    Attributes:
        id (int): Unique ID of the movie.
        user_id (int): Foreign key to the ID of the user who owns the movie.
        user (User): User who owns the movie.
        name (str): Name of the movie.
        poster (str): URL to the movie poster.
        rating (float): Rating of the movie.
        director_id (int): Foreign key to the ID of the director.
        director (Director): Director of the movie.
        release_year (int): Release year of the movie.
        created_at (datetime): Timestamp when the movie was created.
        updated_at (datetime): Timestamp when the movie was last updated.
    """
    __tablename__ = "movies"

    def __str__(self):
        return f"{self.name} ({self.release_year})"

    def __repr__(self):
        return f"<Movie(id={self.id}, name={self.name}, user_id={self.user_id}, director_id={self.director_id}, rating={self.rating}, release_year={self.release_year}, created_at={self.created_at}, updated_at={self.updated_at})>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="movies")
    name = Column(String, nullable=False)
    poster = Column(String, nullable=True, default=PLACEHOLDER_MOVIE_POSTER)
    rating = Column(Float, nullable=False)
    director_id = Column(Integer, db.ForeignKey('directors.id'), nullable=False)
    director = relationship("Director", back_populates="movies")
    release_year = Column(Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())


class Director(BaseModel):
    """
    Represents a director in the system.

    Attributes:
        id (int): Unique ID of the director.
        firstname (str): First name of the director.
        lastname (str): Last name of the director.
        movies (list): List of movies associated with the director.
        created_at (datetime): Timestamp when the director was created.
        updated_at (datetime): Timestamp when the director was last updated.
    """
    __tablename__ = "directors"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"<Director(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, created_at={self.created_at}, updated_at={self.updated_at})>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    movies = db.relationship('Movie', back_populates='director', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())
