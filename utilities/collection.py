from typing import List
from utilities.movie import Movie


class Collection:

    def __init__(self, name: str, lst: List[int] = None):
        self._name = name
        self._lst = lst
        self._size = len(lst)

    def get_name(self) -> str:
        """Getter for collection name"""
        return self._name

    def get_lst(self) -> List[int]:
        """Getter for internal ranked list"""
        return self._lst

    def get_size(self) -> int:
        """Getter for size of collection"""
        return self._size

    def add_movie(self, movie_id: int, index: int) -> None:
        """Adds a movie to the collection

        Args:
            movie_id: an int representing the id of a movie in the database
            index: the index to insert the movie at
        """
        self._lst.insert(index, movie_id)
        self._size += 1
