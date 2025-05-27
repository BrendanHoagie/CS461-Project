import utilities.utils as utils
from utilities.movie import Movie


def home_page(override: bool) -> None:
    """Betterboxd home page, where a user can choose what to do on the app
    Handles user input, redirects to child functions

    Args:
        override - a dev argument to override the login panic, remove for release
    """
    options = [
        {"Log A Movie": log_movie},
        {"Search the catalog": search},
        {"View and edit profile": edit},
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
        for i, e in enumerate(options):
            print(f"{i + 1}. {list(e.keys())[0]}")
        try:
            choice = int(input(f"Enter a number 1-{i + 1}: ")) - 1
            if choice < 0:
                raise ValueError
            list(options[choice].values())[0]()
        except Exception:
            print("Unrecognized input, please try again")


def log_movie() -> None:
    """Log a movie on your profile
    Handles user input, updates the database to add a movie, updates the database to change star values
    """
    genres = []
    runtime = 0
    crew = {}
    score = []

    def log(movie_id: int) -> None:
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
        log(id)
        return

    # if we need to add the movie
    print(f"We couldn't find the movie {title} in our database, would you like to add it?")
    if input("Type 1 for yes, anything else to return to homepage: ") != "1":
        return

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

    # add the movie, then log it
    new_movie = Movie(title, genres, runtime, crew, score)
    utils.add_movie_to_database(new_movie)
    log(new_movie.get_id())


def search():
    pass


def edit():
    pass


def lists():
    pass
