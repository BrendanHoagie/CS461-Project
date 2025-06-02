from typing import Dict, List
import utilities.utils as utils


class Movie:

    def __init__(
        self,
        id: int,
        title: str,
        runtime: int,
        avg_rating: float,
        num_ratings: int,
        score_id: int = -1,
        crew: Dict[str, List[str]] = None,
        score: List[str] = None,
    ):
        self._id = id
        self._title = title
        self._runtime = runtime
        self._avg_rating = avg_rating
        self._num_ratings = num_ratings
        self._crew = crew
        self._score = score
        self._score_id = score_id

    def get_id(self) -> int:
        """Getter for id"""
        return self._title

    def get_title(self) -> str:
        """Getter for title"""
        return self._title

    def get_runtime(self) -> int:
        """Getter for runtime"""
        return self._runtime

    def get_avg_rating(self) -> float:
        """Getter for star avg_ratings"""
        return self._avg_rating

    def get_num_rating(self) -> int:
        """Getter for number of ratings"""
        return self._num_ratings

    def get_crew(self) -> Dict[str, List[str]]:
        """Getter for crew"""
        return self._crew

    def set_crew(self, crew: Dict[str, List[str]]) -> None:
        """Setter for crew

        Args:
            crew - a dictionary with "crew_name" : ["crew_job1", ...] pairs
        """
        self._crew = crew

    def get_score(self) -> List[str]:
        """Getter for score"""
        return self._score

    def get_score_id(self) -> int:
        """Getter for score id"""
        return self._score_id

    def set_score(self, score_id: int, score: List[str]) -> None:
        """Setter for score

        Args:
            score_id - an int representing the score ID
            score - a list of song titles
        """
        self._score_id = score_id
        self._score = score

    def add_rating(self, rating: float) -> None:
        """Adds a rating

        Args:
            rating - a float representing a new rating
        """
        total_score = self._avg_rating * self._num_ratings
        new_total_score = total_score + rating
        self._num_ratings += 1
        self._avg_rating = new_total_score / self._num_ratings

    def display_movie(self) -> None:
        """Pretty print the movie class"""
        print(f"ID: {self._id}")
        print(f"Title: {self._title}")
        print(f"Run time: {self._runtime}")
        print(f"Crew:")
        for k, v in self._crew.items():
            print(f"\t{k}: {v}")
        print(f"Score:")
        for s in self._score:
            print(f"\t {s}")
        print(f"Star Rating: {self._avg_rating}")
        print()
