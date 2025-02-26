from sqlalchemy import Column, Integer, String, Float, func
from sqlalchemy.orm import relationship

from database.extensions import db
from schemas.base_schema import BaseModel

PLACEHOLDER_MOVIE_POSTER = "https://critics.io/img/movies/poster-placeholder.png"


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
        # director_id (int): Foreign key to the ID of the director.
        # director (Director): Director of the movie.
        release_year (int): Release year of the movie.
        created_at (datetime): Timestamp when the movie was created.
        updated_at (datetime): Timestamp when the movie was last updated.
    """
    __tablename__ = "movies"

    def __str__(self):
        return f"{self.name} ({self.release_year})"

    def __repr__(self):
        return f"<Movie(id={self.id}, name={self.name}, user_id={self.user_id}, rating={self.rating}, release_year={self.release_year}, created_at={self.created_at}, updated_at={self.updated_at})>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="movies", lazy=True)
    name = Column(String, nullable=False)
    actors = Column(String, nullable=True)
    writer = Column(String, nullable=True)
    awards = Column(String, nullable=True)
    boxOffice = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    director = Column(String, nullable=True)
    poster = Column(String, nullable=True, default=PLACEHOLDER_MOVIE_POSTER)
    rating = Column(Float, nullable=False)
    plot = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    imdbId = Column(String, nullable=True)
    youtube_video_id = Column(String, nullable=True)
    runtime = Column(Integer)
    watch_date = Column(db.DateTime, server_default=func.current_timestamp())
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())
