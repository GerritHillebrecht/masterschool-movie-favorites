from abc import ABC, abstractmethod
from schemas import User, Movie, Director


class DataMangerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def add_movie(self, movie: Movie):
        pass

    @abstractmethod
    def get_all_directors(self):
        pass

    @abstractmethod
    def add_director(self, director: Director):
        pass

    @abstractmethod
    def update_movie(self, updated_movie_data, user_id, movie_id):
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        pass
