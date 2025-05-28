import os
from typing import Dict, List
from utilities.user import User
from utilities.movie import Movie

# global representing who is logged in
_CURRENT_USER = None

# fake DBs for testing
_USERS = []
_MOVIES = []

# constants
MAX_PASSWORD_LENGTH = 64
MAX_USERNAME_LENGTH = 32


class GoBackException(Exception):
    """Custom error type local to this function.
    Raised so that this function knows to quit out to home page
    """

    def __init__(self):
        super().__init__()


def set_up_database() -> None:
    """Create fake data for testing.
    In the real app, this is where we'd authenticate with SQL server.
    Passwords:
        brendan: hello
        randy: test
        dante: 123
    """

    # setup fake users
    b = User("brendan", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
    r = User("randy", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")
    d = User("dante", "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3")
    _USERS.append(b)
    _USERS.append(r)
    _USERS.append(d)

    # setup fake movies
    h = Movie(
        "Hatari!",
        ["Adventure, Comedy"],
        157,
        {
            "John Wayne": ["Actor", "Producer"],
            "Howard Hanks": ["Director", "Producer"],
            "Henry Mancini": ["Composer"],
        },
        [
            "Theme from 'Hatari!'",
            "Baby Elephant Walk",
            "Just for Tonight",
        ],
        [1.5, 4.5, 3.0],
        {
            1: ["I did not like it"],
            2: ["I'm a big fan!", "I still really love it, man"],
            3: [],
        },
    )
    u = Movie(
        "Unfrosted",
        ["Comedy", "Drama"],
        93,
        {
            "Jerry Seinfeld": ["Actor", "Producer", "Director"],
            "Melissa McCarthy": ["Actor"],
            "Jim Gaffigan": ["Actor"],
            "Christophe Beck": ["Composer"],
            "Jimmy Fallon": ["Composer"],  # THIS IS REAL!!!!
        },
        [
            'Sweet Morning Heat (from the Netflix Film "Unfrosted")',
            "Battle Creek, 1963",
            "Poop, Slap, and Smile",
            "The Bowl and Spoon Awards",
        ],
        [1.0],
        {},
    )
    _MOVIES.append(h)
    _MOVIES.append(u)


def clear_terminal() -> None:
    """Convienience function, clears the terminal on Windows & Linux"""
    os.system("cls" if os.name == "nt" else "clear")


def take_cli_input_with_options(options: List[Dict[str, callable]]) -> callable:
    """Displays a list of otions then handles CLI input.
    Uses a standard system where options are stored as a list of dictionaries

    Args:
        options - a list containing dictionaries, where each key-value pair is a string and a function

    Returns:
        the chosen function from the options list
    """
    while 1:
        for i, e in enumerate(options):
            print(f"{i + 1}. {list(e.keys())[0]}")
        try:
            choice = int(input(f"Enter a number 1-{i + 1}: ")) - 1
            if choice < 0:
                raise ValueError
            return list(options[choice].values())[0]
        except Exception:
            print("Unrecognized input, please try again")


def set_current_user(user: str) -> None:
    """Sets global current user, acts as a token for the session"""
    for u in _USERS:
        if u.get_username().lower() == user:
            _CURRENT_USER = u


def get_current_user() -> User | None:
    """Gets the user currently logged in"""
    return _CURRENT_USER


def delete_current_user() -> None:
    """Deletes the current user from the database and un-sets current user.
    Will break many parts of the homepage, use carefully
    """
    _USERS.remove(_CURRENT_USER)


def add_to_users(username: str, password: str) -> None:
    """Add to the username database

    Args:
        username - a str representing the queried username
        password - a str representing the entered password
    """
    _USERS.append(User(username, password))


def user_exists(username: str) -> bool:
    """Query if user is already in database

    Args:
        username - a string representing the queried username

    Returns:
        a bool representing if the user exists in the database
    """
    for u in _USERS:
        if u.get_username().lower() == username.lower():
            return True
    return False


def password_correct(username: str, password: str) -> bool:
    """Query if password is correct for the given username.
    Note: this does not check if username exists, use accordingly

    Args:
        username - a string representing the queried username
        password - a string representing the entered password

    Returns:
        a bool representing if the password is correct
    """
    for u in _USERS:
        if u.get_username().lower() == username.lower():
            return u.check_password(password)
    return False


def search_for_movie_by_title_exact(title: str) -> int | None:
    """Query if a given movie title is in the database (exact match)

    Args:
        title - a string representing the title of a movie

    Returns:
        an int indicating the movie ID if a matching title was found, else None
    """
    for m in _MOVIES:
        if m.get_name().lower() == title.lower():
            return m.get_id()
    return None


def search_for_movie_by_id(id: int) -> Movie | None:
    """Return a movie given its id

    Args:
        id - an int representing the id of a movie in the database

    Returns:
        a Movie object if the movie was found, else None
    """
    for m in _MOVIES:
        if m.get_id() == id:
            return m
    return None


def search_by_title_inexact(term: str) -> List[Movie] | None:
    """Returns search results that include the term in the move title (inexact match)
    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the title, may be None
    """
    return [m for m in _MOVIES if term.lower() in m.get_title().lower()]


def search_by_genre(term: str) -> List[Movie] | None:
    """Returns search results that include the term in the genre field

    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the genre field, may be None
    """
    return [m for m in _MOVIES if any(g.lower() == term.lower() for g in m.get_genres())]


def search_by_crew(term: str) -> List[Movie] | None:
    """Returns search results that include the term in the crew field

    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the crew field, may be None
    """
    return [m for m in _MOVIES if any(term.lower() in c.lower() for c in m.get_crew().keys())]


def search_by_score(term: str) -> List[Movie] | None:
    """Returns search results that include the term in any song titles of the score field

    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in a song in the score field, may be None
    """
    return [m for m in _MOVIES if any(term.lower() in s.lower() for s in m.get_score())]


def add_log(movie_id: int, rating: float, review: str) -> None:
    """Adds a log to a movie in the database
    Does not do any error checking

    Args:
        movie_id - an int representing the id of the movie we want
        rating - a float representing the rating given
        review - a string representing the text review
    """
    for m in _MOVIES:
        if m.get_id() == movie_id:
            m.add_star_rating(rating)
            m.add_text_review(user_id=_CURRENT_USER, review=review)


def add_movie_to_database(mov: Movie) -> None:
    """Adds a movie to the database

    Args:
        mov - a movie object to be added to database
    """
    _MOVIES.append(mov)
