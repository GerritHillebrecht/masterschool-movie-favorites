from sqlalchemy import Column, Integer, String, func

from database.extensions import db
from schemas.base_schema import BaseModel


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
    # movies = db.relationship('Movie', back_populates='director', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp())
