import hashlib
import utilities.utils as utils
from utilities.movie import Movie
from utilities.collection import Collection
from typing import List


def home_page(override: bool) -> None:
    """Betterboxd home page, where a user can choose what to do on the app
    Handles user input, redirects to child functions

    Args:
        override - a dev argument to override the login panic, remove for release
    """
    options = [
        {"Log a movie": log_movie},
        {"Add a movie to the database": add_movie},
        {"Search the catalog": search},
        {"View and edit profile": view_and_edit},
        {"View my lists": lists},
        {"Log out": quit},
    ]

    if utils.get_current_user() and override is not True:
        print("Error-- user made it to homepage without logging in. Exiting")
        quit(1)

    while 1:
        utils.clear_terminal()
        print("|-- Betterboxd Home Page --|")
        print("What would you like to do?")
        utils.take_cli_input_with_options(options)()


def log_movie() -> None:
    """Log a movie on your profile
    Handles user input, updates the database to add a movie, updates the database to change star values
    """

    def _log(movie_id: int) -> None:
        """Handles logging the movie once we know it's in the database

        Args:
            movie_id - an int representing the ID of a movie in the database
        """
        rating = 0.0

        # get the rating
        while 1:
            try:
                rating = float(input("Enter a star rating 1-5, including partial values"))
                if rating < 0.0:
                    print("Sorry, we know it's bad, but you can't give a negative rating")
                elif rating > 5.0:
                    print("Sorry, even though you love this movie, you can only give up to 5 stars")
                else:
                    break
            except Exception:
                print("Unrecognized input, please try again")

        # get the text review - TODO: how do we handle someone reviewing more than 250 characters? retype it? cut if off?
        review = input("Enter your review of the movie (max 250 characters): ")
        utils.add_log(movie_id, rating, review)

    utils.clear_terminal()
    print("|-- Log Movie --|")
    title = input("Enter movie name: ")

    # if we find the movie
    if id := utils.search_for_movie_by_title(title):
        _log(id)
        return

    # if we need to add the movie
    print(f"We couldn't find the movie {title} in our database, would you like to add it?")
    if input("Type 1 for yes, anything else to return to homepage: ") == "1":
        new_movie = add_movie(title)
        if new_movie is None:
            return
        _log(new_movie.get_id())


def add_movie(name: str = None) -> Movie | None:
    """Add a movie to the database

    Args:
        name - a string containing the name of the movie
    Returns:
        a Movie object representing the new movie, or None if the user quits out early
    """

    title = ""
    id = -1
    genres = []
    runtime = 0
    crew = {}
    score = []

    while id is not None:
        title = input("Enter movie name: ") if name is None else name
        if id := utils.search_for_movie_by_title(title):
            print(
                "That movie already exists in the database. If there is a duplicate name, try adding the year afterwards in parenthesis"
            )
            if (
                input(
                    "Would you like to continue adding a movie? Type 1 for yes, anything else to return to homepage: "
                )
                == "1"
            ):
                return None

    # get list of genres
    raw_genre = input(
        "Enter the genre(s) of this movie. For multiple genres, seperate them with a comma: "
    )
    raw_genre = raw_genre.replace(" ", "")
    genres = raw_genre.split(",")

    # get runtime
    while 1:
        try:
            runtime = int(input("Enter the runtime of the movie as an integer number of minutes: "))
            if runtime < 0:
                print("Runtime must be at least 1 minute long, try again")
        except Exception:
            print("Unrecognized input, try again")

    # Get the crew
    print("Enter the crew:")
    while 1:
        name = input("Enter the name of a crew member: ")
        raw_roles = input(
            f"Enter the jobs {name} did on this movie. For multiple roles, seperate them with a comma: "
        )
        raw_roles = raw_roles.replace(" ", "")
        crew[name] = raw_roles.split(",")
        print(f"Would you like to add another crew member?")
        if input("Type 1 for yes, anything else to finish adding crew members: ") != "1":
            break

    # Get the score
    print("Enter the score song by song:")
    while 1:
        song = input("Enter the name of a song: ")
        score.append(song)
        print(f"Would you like to add another song?")
        if input("Type 1 for yes, anything else to finish adding crew members: ") != "1":
            break

    # add the movie
    new_movie = Movie(title, genres, runtime, crew, score)
    utils.add_movie_to_database(new_movie)
    return new_movie


def search() -> None:
    pass


def view_and_edit() -> None:
    """Displays info about the user profile, allows you to change it"""

    def _display_profile() -> None:
        """Displays a user's profile"""

        utils.clear_terminal()
        user = utils.get_current_user()
        print(f"|__ {user.get_username()}'s Profile --|")
        print(f"Favorite Movie: ", end="")
        if user.get_fav_movie_id() is None:
            print("Has not been chosen yet")
        else:
            print(f"{utils.search_for_movie_by_id(user.get_fav_movie_id()).get_title()}")
        print()
        print(f"Has created {len(user.get_collections())} lists")
        input("Type anthing to return to the account page: ")
        return

    def _set_favorite() -> None:
        """Search for a movie & set it as favorite, add it to database if it doesn't yet exist"""

        utils.clear_terminal()
        user = utils.get_current_user()
        title = input("Enter the name of a movie: ")
        if id := utils.search_for_movie_by_title(title):
            user.set_fav_movie_id(id)
            return

        print(f"We couldn't find the movie {title} in our database, would you like to add it?")
        if input("Type 1 for yes, anything else to return to the account page: ") == "1":
            user.set_fav_movie_id(add_movie().get_id())

    def _change_password() -> None:
        """Updates a user's password"""

        user = utils.get_current_user()
        password = ""
        utils.clear_terminal()
        while 1:
            password = input("Enter your password (max 32 characters): ")
            if len(password) <= utils.MAX_PASSWORD_LENGTH:
                break
            print("Sorry, that password is too long, please try again")

        # hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # update password (replace w/ sql)
        user.set_password(hashed_password)

    def _delete_account() -> None:
        """Deletes the account and logs the user out

        Side Effects:
            exits the application
        """

        utils.clear_terminal()
        user = utils.get_current_user()
        password = ""
        num_attempts = 0
        while 1:
            password = input(
                "Enter your password to confirm that you'd like to delete your account and log out: "
            )
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user.check_password(hashed_password):
                utils.delete_current_user()
                quit()

            print("Sorry, that password does not match, please try again")
            num_attempts += 1
            if num_attempts == 3:
                print(
                    f"You've entered the wrong password {num_attempts} times, would you like to keep trying?"
                )
                if input("Type 1 for yes, anything else to return to the account page: ") == "1":
                    return
                num_attempts = 0

    def _go_back() -> None:
        """Raises GoBackException so the function knows to return to the homepage menu"""
        raise utils.GoBackException

    options = [
        {"Display profile information": _display_profile},
        {"Choose a favorite movie": _set_favorite},
        {"Change password": _change_password},
        {"Delete account": _delete_account},
        {"Go back": _go_back},
    ]

    while 1:
        utils.clear_terminal()
        print("|-- Account Page --|")
        print("What would you like to do?")
        try:
            utils.take_cli_input_with_options(options)()
        except utils.GoBackException:
            return


def lists() -> None:
    """Displays user created list, allows for creation of lists"""

    def _create_helper(id: int, title: str, new_list_size: int) -> int:
        """Helper for _create_list, handles getting the ranking

        Args:
            id - the id of a movie in the database
            title - a string containing the name of the movie
            new_list_size - the size of new list

        Returns:
            an integer representing the chosen index
        """
        while 1:
            try:
                index = int(
                    input(f"Enter your ranking of {title}, an integer 1-{new_list_size + 1}")
                )
                if index < 1:
                    raise Exception
                return index - 1
            except Exception:
                print("Unrecognized input, please try again")

    def _create_list() -> None:
        """Creates a new list and saves it to the user's profile"""

        new_list = []
        new_list_size = 0

        utils.clear_terminal()
        print("|-- Create a New List --|")
        list_name = input("Enter the name of the list: ")
        while 1:
            title = input("Enter the name of a movie to add to the list: ")

            # movie is in the database
            if id := utils.search_for_movie_by_title(title):
                index = _create_helper(id, title, new_list_size)
                new_list.insert(index, id)
                new_list_size += 1

            # needs to be added
            else:
                print(
                    f"We couldn't find the movie {title} in our database, would you like to add it?"
                )
                if (
                    input(
                        f"Type 1 for yes, anything else to skip and continue adding to {list_name}: "
                    )
                    == "1"
                ):
                    new_movie = add_movie(title)
                    if new_movie is None:
                        continue
                    index = _create_helper(new_movie.get_id(), title, new_list_size)
                    new_list.insert(index, new_movie.get_id())
                    new_list_size += 1

            print(f"Would you like to add another movie to the list?")
            if input(f"Type 1 for yes, anything else to return to list viewer page: ") != "1":
                break

        new_collection = Collection(list_name, new_list)
        utils.get_current_user().add_new_collection(new_collection)

    def _view_all_lists() -> None:
        pass

    def _go_back() -> None:
        """Raises GoBackException so the function knows to return to the homepage menu"""
        raise utils.GoBackException

    options = [
        {"Create a new list": _create_list},
        {"Select an existing list to view": _view_all_lists},
        {"Go back": _go_back},
    ]

    while 1:
        utils.clear_terminal()
        print("|-- List Viewer --|")
        try:
            utils.take_cli_input_with_options(options)()
        except utils.GoBackException:
            return
