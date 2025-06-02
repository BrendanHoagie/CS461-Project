import os
import sys
from typing import Dict, List
from utilities.user import User
from utilities.movie import Movie
import mysql.connector

# global database object
_DB = None

# list of all the tables in properly configured database
_TABLES = [
    "account",
    "account_collections",
    "collections",
    "crew",
    "crew_job",
    "crew_movie",
    "entry",
    "movie",
    "score",
    "score_songs",
]

# global representing who is logged in
_CURRENT_USER = None

# constants
MAX_PASSWORD_LENGTH = 32
MAX_USERNAME_LENGTH = 32
DEFAULT_MOVIE_ID = 25  # fake/default movie, check when displaying profile


class GoBackException(Exception):
    """Custom error type local to this function.
    Raised so that this function knows to quit out to home page
    """

    def __init__(self):
        super().__init__()


def set_up_database() -> None:
    """Sets up the database. Asks for host, username, and password for who is running the SQL database"""
    global _DB
    tables_in_db = []
    host = user = password = ""

    print("Let's make sure the database is set up correctly!")
    host = input("Enter the host, default is localhost, press enter to accept default: ")
    user = input("Enter the current user, default is root, press enter to accept default: ")
    password = input("Enter the password for the current user: ")

    host = "localhost" if host == "" else host
    user = "root" if user == "" else user

    try:
        _DB = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database="Betterboxd",
        )

    except mysql.connector.errors.Error as e:
        print(f"Ran into an error: {e}.")
        print(
            "Make sure you set the database up according to the README, and make sure you entered the correct host, username, and password for the database"
        )
        print("Exiting.")
        sys.exit(1)

    # simple sanity check if all tables are there
    with _DB.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        for x in cursor:
            tables_in_db.append(x[0])

    if tables_in_db != _TABLES:
        for table in _TABLES:
            if table not in tables_in_db:
                print(
                    f"Error: table {table} not found in the database. Are you sure you configured it correctly?"
                )
                print("Exiting")
                sys.exit(1)


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
            else:
                return list(options[choice].values())[0]
        except Exception:
            print("Unrecognized input, please try again")


def set_current_user(username: str) -> None:
    """Sets global current user, acts as a token for the session

    Args:
        username - a str representing the username of the currently logged-in user
    """
    global _CURRENT_USER

    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT * 
               FROM Account 
               WHERE account_name = %(username)s;""",
            {"username": username.lower()},
        )
        db_username, fav, watch_count, password = cursor.fetchone()
        _CURRENT_USER = User(db_username, password, fav)


def get_current_user() -> User:
    """Gets the user currently logged in"""
    return _CURRENT_USER


def delete_current_user() -> None:
    """Deletes the current user from the database and un-sets current user.
    Will break many parts of the homepage, use carefully
    """
    _USERS.remove(_CURRENT_USER)


def add_to_users(username: str, password: str) -> None:
    """Add a user to the database

    Args:
        username - a str representing the queried username
        password - a str representing the entered password
    """

    with _DB.cursor() as cursor:
        cursor.execute(
            """INSERT INTO Account(account_name, favorite_movie, watch_count, passphrase)
            VALUES (%(username)s, 25, 0, %(password)s);""",
            {
                "username": username.lower(),
                "password": password.lower(),
            },
        )
        _DB.commit()


def user_exists(username: str) -> bool:
    """Query if user is already in database

    Args:
        username - a string representing the queried username

    Returns:
        a bool representing if the user exists in the database
    """
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT COUNT(*) 
               FROM Account 
               WHERE account_name = %(username)s;""",
            {"username": username.lower()},
        )
        result = cursor.fetchone()[0]
        return result == 1


def password_correct(username: str, password: str) -> bool:
    """Query if password is correct for the given username.
    Note: this does not check if username exists, use accordingly

    Args:
        username - a string representing the queried username
        password - a string representing the entered password

    Returns:
        a bool representing if the password is correct
    """
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT passphrase 
               FROM Account 
               WHERE account_name = %(username)s;""",
            {"username": username.lower()},
        )
        result = cursor.fetchone()[0]
        return result == password


def search_for_movie_by_title_exact(title: str) -> int:
    """Query if a given movie title is in the database (exact match)

    Args:
        title - a string representing the title of a movie

    Returns:
        an int indicating the movie ID if a matching title was found, else None
    """
    for m in _MOVIES:
        if m.get_title().lower() == title.lower():
            return m.get_id()
    return None


def search_for_movie_by_id(id: int) -> Movie:
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


def search_by_title_inexact(term: str) -> List[Movie]:
    """Returns search results that include the term in the move title (inexact match)
    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the title, may be None
    """
    return [m for m in _MOVIES if term.lower() in m.get_title().lower()]


def search_by_genre(term: str) -> List[Movie]:
    """Returns search results that include the term in the genre field

    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the genre field, may be None
    """
    return [m for m in _MOVIES if any(g.lower() == term.lower() for g in m.get_genres())]


def search_by_crew(term: str) -> List[Movie]:
    """Returns search results that include the term in the crew field

    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the crew field, may be None
    """
    return [m for m in _MOVIES if any(term.lower() in c.lower() for c in m.get_crew().keys())]


def search_by_score(term: str) -> List[Movie]:
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
