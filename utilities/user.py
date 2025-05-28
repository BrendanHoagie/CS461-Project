from typing import List
from utilities.collection import Collection


class User:
    _user_id_counter = 0

    def __init__(
        self,
        username: str,
        password: str,
        fav_movie_id: int = None,
        collections: List[Collection] = [],
    ):
        self._user_id_counter += 1
        self._id = self._user_id_counter
        self._username = username
        self._password = password
        self._fav_movie_id = fav_movie_id
        self._collections = collections

    def get_id(self) -> int:
        """Getter for user ID"""
        return self._id

    def get_username(self) -> str:
        """Getter for username"""
        return self._username

    def check_password(self, password: str) -> bool:
        """Checks to see if a given password is the user's password
        Offloads repsponsibility of checking passwords to the User object, obscuring implementation

        Args:
            password - a string containing a possible password to be checked
        """
        return self._password == password

    def set_password(self, password):
        """Setter for password.
        This function does not hash, always pass in a hashed string

        Args:
            password - a string containing the new password.
        """
        self._password = password

    def get_fav_movie_id(self) -> int:
        """Getter for favorite movie id"""
        return self._fav_movie_id

    def set_fav_movie_id(self, movie_id: int) -> None:
        """Setter for favorite movie

        Args:
            movie_id - an int representing the movie that is your favorite
        """
        self._fav_movie_id = movie_id

    def get_collections(self) -> List[Collection]:
        """Getter for collections"""
        return self._collections

    def set_collections(self, collections: List[Collection]) -> None:
        """setter for collections

        Args:
            collection - a list of Collection objects
        """
        self._collections = collections

    def add_new_collection(self, collections: List[Collection]) -> None:
        """Adds a new collection to the user's collections

        Args:
            collection - a list of Collection objects
        """
        self._collections.append(collections)

    def delete_collection(self, collection: Collection) -> None:
        """Deletes a collection from the user's collections.
        Does no error checking

        Args:
            collection - a Collection object from collections to be removed
        """
        self._collections.remove(collection)

    def pprint(self) -> None:
        """Pretty print the user class"""
        print(f"ID: {self._id}")
        print(f"Username: {self._username}")
        print(f"Favorite Movie: {self._fav_movie}\n")
