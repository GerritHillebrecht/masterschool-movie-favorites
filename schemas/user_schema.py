from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, func
from werkzeug.security import generate_password_hash, check_password_hash

from database.extensions import db
from schemas.base_schema import BaseModel


class User(BaseModel, UserMixin):
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
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)
    movies = db.relationship('Movie', back_populates='user', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
