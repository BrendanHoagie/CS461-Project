from movie import Movie
from utils import clear_terminal
from utils import MOVIES


def home_page(user: str) -> None:
    """Betterboxd home page, where a user can choose what to do on the app
    Handles user input, redirects to child functions
    """
    options = [
        {"Log A Movie": log_movie},
        {"Search the catalog": search},
        {"Edit profile": edit},
        {"View my lists": lists},
        {"Log out": quit},
    ]

    clear_terminal()
    print("|-- Betterboxd Home Page --|")
    print("What would you like to do?")
    while 1:
        for i, e in enumerate(options):
            print(f"{i + 1}. {list(e.keys())[0]}")
        try:
            choice = int(input(f"Enter a number 1-{i + 1}: ")) - 1
            if choice < 0:
                raise ValueError
            list(options[choice].values())[0]()
        except Exception:
            print("Unrecognized input, please try again")


def log_movie():
    """Log a movie on your profile
    Handles user input, updates the database to add a movie, updates the database to change star values
    """
    # TODO: finish after user


def search():
    pass


def edit():
    pass


def lists():
    pass
