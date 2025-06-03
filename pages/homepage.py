import hashlib
import utilities.utils as utils
from utilities.movie import Movie
from utilities.collection import Collection
import sys


def home_page() -> None:
    """Betterboxd home page, where a user can choose what to do on the app
    Handles user input, redirects to child functions
    """
    options = [
        {"Log a movie": log_movie},
        {"Add a movie to the database": add_movie},
        {"Search the catalog": search},
        {"View and edit profile": view_and_edit},
        {"View my lists": lists},
        {"Log out": quit},
    ]

    if not utils.get_current_user():
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
                rating = float(input("Enter a star rating 0.0-5, including partial values: "))
                if rating < 0.0:
                    print("Sorry, we know it's bad, but you can't give a negative rating")
                elif rating > 5.0:
                    print("Sorry, even though you love this movie, you can only give up to 5 stars")
                else:
                    break
            except Exception:
                print("Unrecognized input, please try again")

        utils.add_log(movie_id, rating)
        print(f"you've successfully logged {utils.search_for_movie_by_id(movie_id).get_title()}")
        input("Press enter to return to homepage: ")

    utils.clear_terminal()
    print("|-- Log Movie --|")
    title = input("Enter movie name: ")

    # if we find the movie
    if id := utils.search_for_movie_by_title_exact(title):
        _log(id)
        return

    # if we need to add the movie
    print(f"We couldn't find the movie {title} in our database, would you like to add it?")
    if input("Type 1 for yes, anything else to return to homepage: ") == "1":
        new_movie = add_movie(title)
        if new_movie is None:
            return
        _log(new_movie.get_id())


def add_movie(name: str = None) -> Movie:
    """Add a movie to the database

    Args:
        name - a string containing the name of the movie
    Returns:
        a Movie object representing the new movie, or None if the user quits out early
    """

    title = ""
    id = -1
    runtime = 0
    crew = {}
    score = []

    while id is not None:
        title = input("Enter movie name: ") if name is None else name
        if id := utils.search_for_movie_by_title_exact(title):
            print(
                "That movie already exists in the database. If there is a duplicate name, try adding the year afterwards in parenthesis"
            )
            if (
                input(
                    "Would you like to continue adding a movie? Type 1 for yes, enter to return to homepage: "
                )
                != "1"
            ):
                return None
        else:
            break

    # get runtime
    while 1:
        try:
            runtime = int(input("Enter the runtime of the movie as an integer number of minutes: "))
            if runtime < 0:
                print("Runtime must be at least 1 minute long, try again")
            else:
                break
        except Exception:
            print("Unrecognized input, try again")

    hours = runtime // 60
    minutes = runtime % 60
    runtime = ((hours * 100) + minutes) * 100

    # Get the crew
    print("|-- Crew Entry --|")
    while 1:
        tmp = []
        name = input("Enter the name of a crew member: ")
        role = input(f"Enter the job {name} did on this movie: ")
        tmp.append(role)
        crew[name] = tmp
        print(f"Would you like to add another crew member?")
        if input("Type 1 for yes, enter to finish adding crew members: ") != "1":
            break

    # Get the score
    print("Enter the score song by song:")
    while 1:
        song = input("Enter the name of a song: ")
        score.append(song)
        print(f"Would you like to add another song?")
        if input("Type 1 for yes, enter to finish adding songs: ") != "1":
            break

    # add the movie
    new_movie = Movie(-1, title, runtime, 0, 0, -1, crew, score)
    new_movie = utils.add_movie_to_database(new_movie)
    print(f"You've successfully added {title} to the database!")
    new_movie.display_movie()
    input("Press enter to return to home screen")
    return new_movie


def search() -> None:
    """Allows the user to set a filter and search within that category"""

    def _sort_title() -> None:
        """Searches by title"""
        utils.clear_terminal()
        print("|-- Seach Movie by Title --|")
        term = input("Enter your search term: ")
        movies = utils.search_by_title_inexact(term)
        if movies:
            for m in movies:
                m.display_movie()
                print()
        else:
            print(f'Sorry, could not find any movies with "{term}" in the title')
        input("Type anything to return to search menu: ")

    def _sort_genre() -> None:
        """Searches by genre"""
        utils.clear_terminal()
        print("|-- Seach Movie by Genre --|")
        term = input("Enter your search term: ")
        movies = utils.search_by_genre(term)
        if movies:
            for m in movies:
                m.display_movie()
                print()
        else:
            print(f'Sorry, could not find any movies where the genre matched the term "{term}"')
        input("Type anything to return to search menu: ")

    def _sort_crew() -> None:
        """Searches by crew members"""
        utils.clear_terminal()
        print("|-- Seach Movie by Crew --|")
        term = input("Enter your search term: ")
        movies = utils.search_by_crew(term)
        if movies:
            for m in movies:
                m.display_movie()
                print()
        else:
            print(f'Sorry, could not find any movies where the crew included the "{term}"')
        input("Type anything to return to search menu: ")

    def _sort_score() -> None:
        """Searches by songs"""
        utils.clear_terminal()
        print("|-- Seach Movie by Score --|")
        term = input("Enter your search term: ")
        movies = utils.search_by_score(term)
        if movies:
            for m in movies:
                m.display_movie()
                print()
        else:
            print(
                f'Sorry, could not find any movies where the score included songs with "{term}" in the title'
            )
        input("Type anything to return to search menu: ")

    def _go_back() -> None:
        """Raises GoBackException so the function knows to return to the homepage menu"""
        raise utils.GoBackException

    options = [
        {"Search by title": _sort_title},
        {"Search by genre": _sort_genre},
        {"Search by crew": _sort_crew},
        {"Search by score": _sort_score},
        {"Go back": _go_back},
    ]

    while 1:
        utils.clear_terminal()
        print("|-- Search the Database --|")
        print("What would you like to search by?")
        try:
            utils.take_cli_input_with_options(options)()
        except utils.GoBackException:
            return


def view_and_edit() -> None:
    """Displays info about the user profile, allows you to change it"""

    def _display_profile() -> None:
        """Displays a user's profile"""

        utils.clear_terminal()
        print("Displaying")
        user = utils.get_current_user()
        print(f"|-- {user.get_username()}'s Profile --|")
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
        if id := utils.search_for_movie_by_title_exact(title):
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

    def _go_back() -> None:
        """Raises GoBackException so the function knows to return to the homepage menu"""
        raise utils.GoBackException

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
            if id := utils.search_for_movie_by_title_exact(title):
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

    def _view_rankings() -> None:
        """Sub-function of _view_lists, displays the rankings of a single collection"""
        choice = -1

        utils.clear_terminal()
        print("|-- Pick a List to View --|")
        collections = utils.get_current_user().get_collections()
        for i, c in enumerate(collections):
            print(f"{i + 1}. {c.get_name()}")
        print()

        while 1:
            try:
                choice = int(input(f"Enter a number 1-{i}: "))
                if choice < 1 or choice > i:
                    raise Exception
            except Exception:
                print("Unrecognized input, please try again")

        collections[choice].display_collection()
        input("Type anything to return to the list page: ")

    def _edit_list() -> None:
        """Sub-function for _view_lists, chooses a specific list and allows a user to edit it"""

        choice = -1
        new_index = -1

        utils.clear_terminal()
        print("|-- Pick a List to Edit --|")
        collections = utils.get_current_user().get_collections()
        for i, c in enumerate(collections):
            print(f"{i + 1}. {c.get_name()}")
        print()

        while 1:
            try:
                choice = int(input(f"Enter a number 1-{i}: "))
                if choice < 1 or choice > i:
                    raise Exception
            except Exception:
                print("Unrecognized input, please try again")

        collection = collections[choice - 1]

        # name
        print(f"Would you like to change {collection.get_name()}'s name?")
        if input("Type 1 for yes, anything else to continue: ") == "1":
            collection.set_name(input("Enter the new name of the list: "))

        # rankings
        print(f"Would you like to change {collection.get_name()}'s rankings?")
        if input("Type 1 for yes, anything else to continue: ") != "1":
            return

        while 1:
            # display all movies & rankings
            for i, c in enumerate(collection.get_lst()):
                print(f"{i}. {utils.search_for_movie_by_id(c)}")

            # get input
            while 1:
                try:
                    choice = int(input(f"Enter a number 1-{i} to change: "))
                    if choice < 1 or choice > i:
                        raise Exception
                    choice -= 1
                    break
                except Exception:
                    print("Unrecognized input, please try again")

            # get new ranking
            while 1:
                try:
                    new_index = int(input(f"Enter the new ranking (a number 1-{i}): "))
                    if new_index < 1 or new_index > i:
                        raise Exception
                    new_index -= 1
                    break
                except Exception:
                    print("Unrecognized input, please try again")

            # update list and leave/keep going
            collection.change_index(choice, new_index)
            print(f"Would you like to continue updating rankings?")
            if input("Type 1 for yes, anything else to finish: ") != "1":
                break

    def _delete_list() -> None:
        """Sub-function for _view_lists, deletes a list from a user's collections"""
        choice = -1

        utils.clear_terminal()
        print("|-- Pick a List to Delete --|")
        collections = utils.get_current_user().get_collections()
        for i, c in enumerate(collections):
            print(f"{i + 1}. {c.get_name()}")
        print()

        while 1:
            try:
                choice = int(input(f"Enter a number 1-{i}: "))
                if choice < 1 or choice > i:
                    raise Exception
                choice -= 1
                break
            except Exception:
                print("Unrecognized input, please try again")

        collection = collections[choice]
        print(f"Are you sure you want to delete {collection.get_name()}?")
        if input("Type 1 to confirm deletion, anything else to go back to the list menu: ") == "1":
            utils.get_current_user().delete_collection(collection)

    def _view_lists() -> None:
        """Manager for sub functions, displays all lists, lets the user take a closer look or edit a specific one"""

        options = [
            {"View the rankings in a specific list": _view_rankings},
            {"Edit a list": _edit_list},
            {"Delete a list": _delete_list},
            {"Go back": _go_back},
        ]

        utils.clear_terminal()
        print("|-- Lists --|")
        collections = utils.get_current_user().get_collections()
        for i, c in enumerate(collections):
            print(f"{i + 1}. {c.get_name()}")
        print()

        while 1:
            try:
                utils.take_cli_input_with_options(options)()
            except utils.GoBackException:
                return

    options = [
        {"Create a new list": _create_list},
        {"View all lists": _view_lists},
        {"Go back": _go_back},
    ]

    while 1:
        utils.clear_terminal()
        print("|-- List Viewer --|")
        try:
            utils.take_cli_input_with_options(options)()
        except utils.GoBackException:
            return
