from typing import Dict, List
import utilities.utils as utils


class Movie:
    _movie_id_counter = 0

    def __init__(
        self,
        title: str,
        genres: List[str],
        runtime: int,
        crew: Dict[str, List[str]],
        score: List[str],
        star_ratings: List[float] = None,
        text_reviews: Dict[int, List[str]] = None,
    ):
        self._movie_id_counter += 1
        self._id = self._movie_id_counter
        self._title = title
        self._genres = genres
        self._runtime = runtime
        self._crew = crew
        self._score = score
        self._star_ratings = star_ratings
        self._text_reviews = text_reviews

    def get_id(self) -> int:
        """Getter for id"""
        return self._title

    def get_title(self) -> str:
        """Getter for title"""
        return self._title

    def get_genres(self) -> List[str]:
        """Getter for genre"""
        return self._genres

    def get_runtime(self) -> int:
        """Getter for runtime"""
        return self._runtime

    def get_crew(self) -> Dict[str, List[str]]:
        """Getter for crew"""
        return self._crew

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
        try:
            return sum(self._star_ratings) / len(self._star_ratings)
        except ZeroDivisionError:
            return 0.0

    def get_review_by_user_id(self, user_id: int) -> List[str]:
        """Given a user ID, return any reviews by that account

        Args:
            user_id - an int representing which user we're looking at
        """
        return self._text_reviews.get(user_id, None)

    def display_movie(self) -> None:
        """Pretty print the movie class"""
        print(f"ID: {self._id}")
        print(f"Title: {self._title}")
        print(f"Genres:")
        for g in self._genres:
            print(f"\t{g}")
        print(f"Run time: {self._runtime}")
        print(f"Crew:")
        for k, v in self._crew.items():
            print(f"\t{k}: {v}")
        print(f"Score:")
        for s in self._score:
            print(f"\t {s}")
        print(f"Star Rating (calculated): {self.calculate_rating()}")
        print(f"Star Rating (raw):", end=" ")
        for r in self._star_ratings:
            print(r, end=" ")
        print()
        print("Text Reviews: ")
        for k, v in self._text_reviews.items():
            print(f"\tReviews from user {k}:")
            for i, r in enumerate(v):
                print(f"\t\t{i}. {r}")
