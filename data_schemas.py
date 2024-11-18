from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, func
from sqlalchemy.orm import relationship
from utils.base_model_schema import ToDictMixin

db = SQLAlchemy()

PLACEHOLDER_MOVIE_POSTER = "https://critics.io/img/movies/poster-placeholder.png"


class BaseModel(ToDictMixin, db.Model):
    """
    Custom Parent-class to extend from, easily extendable, especially useful
    for scalability.
    """
    __abstract__ = True


class User(BaseModel):
    __tablename__ = "users"

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())


class Movie(BaseModel):
    __tablename__ = "movies"

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    poster = Column(String, nullable=True, default=PLACEHOLDER_MOVIE_POSTER)
    rating = Column(Float, nullable=False)
    director_id = Column(Integer, db.ForeignKey('directors.id'), nullable=False)
    director = relationship("Director", back_populates="movies")
    release_year = Column(Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())


class Director(BaseModel):
    __tablename__ = "directors"

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    movies = db.relationship('Movie', back_populates='directors', lazy=True, cascade="all, delete-orphan")
