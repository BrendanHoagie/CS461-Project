from typing import List
import utilities.utils as utils
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

    def set_name(self, name: str) -> None:
        """Sets the name field

        Args:
            name - a string representing the new name of the collection
        """
        self._name = name

    def add_movie(self, movie_id: int, index: int) -> None:
        """Adds a movie to the collection

        Args:
            movie_id: an int representing the id of a movie in the database
            index: the index to insert the movie at
        """
        self._lst.insert(index, movie_id)
        self._size += 1

    def display_collection(self) -> None:
        """Version of pretty print, shows each ranking next to each movie title"""
        print(f"|-- {self._name} --|")
        for i, movie_id in enumerate(self._lst):
            mov = utils.search_for_movie_by_id(movie_id)
            if mov is None:
                continue
            print(f"{i + 1}. {mov.get_title()}")

    def change_index(self, current_index: int, new_index: int) -> None:
        """Changes the order of items by swapping id at current to new

        Args:
            current_index - an int representing the item we want to move
            new_index - an int representing the new ranking of that item
        """
        self._lst.insert(new_index, self._lst.pop(current_index))
