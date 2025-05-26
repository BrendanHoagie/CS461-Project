from typing import Dict, List, Self
import utils


class Movie:
    def __init__(
        self,
        id: int,
        name: str = None,
        genres: List[str] = None,
        runtime: int = None,
        crew: Dict[str, List[str]] = None,
        score: List[str] = None,
        star_ratings: List[float] = None,
        text_reviews: Dict[int, List[str]] = None,
    ):
        self._id = id
        self._name = name
        self._genres = genres
        self.runtime = runtime
        self._crew = crew
        self._score = score
        self._star_ratings = star_ratings
        self._text_reviews = text_reviews

    def get_id(self) -> int:
        """Getter for id"""
        return self._name

    def get_name(self) -> str:
        """Getter for name"""
        return self._name

    def get_genres(self) -> List[str]:
        """Getter for genre"""
        return self._genres

    def get_runtime(self) -> int:
        """Getter for runtime"""
        return self._runtime

    def get_crew(self) -> Dict[str, List[str]]:
        """Getter for crew"""
        return self._genres

    def get_score(self) -> List[str]:
        """Getter for score"""
        return self._score

    def get_star_ratings(self) -> List[float]:
        """Getter for star ratings"""
        return self._star_ratings

    def get_text_reviews(self) -> Dict[int, str]:
        """Getter for text reviews"""
        return self._text_reviews

    def add_star_rating(self, rating: float) -> None:
        """Adds a new rating to the movie

        Args:
            rating - a float representing a new star rating
        """
        self._star_ratings.append(rating)

    def add_text_review(self, user_id: int, review: str) -> None:
        """Adds a new review to the movie

        Args:
            user_id - an int representing which user left the review
            review - the text of the review
        """
        if self._text_reviews.get(user_id, None) == None:
            self._text_reviews[user_id] = []
        self._text_reviews[user_id].append(review)  # A user can review a movie n times

    def calculate_rating(self) -> float:
        """Determines aggregated star rating"""
        return sum(self._star_ratings) / len(self._star_ratings)

    def get_review_by_user_id(self, user_id: int) -> List[str] | None:
        """Given a user ID, return any reviews by that account

        Args:
            user_id - an int representing which user we're looking at
        """
        return self._text_reviews.get(user_id, None)
