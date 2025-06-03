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
DEFAULT_MOVIE_ID = 25  # fake/default movie, check if ID matches when displaying profile and display "no favorite set yet or something"
MAX_PASSWORD_LENGTH = 32
MAX_USERNAME_LENGTH = 32
MAX_JOB_LENGTH = 32
MAX_CREW_NAME_LENGTH = 128
MAX_SONG_NAME_LENGTH = 128
MAX_MOVIE_TITLE_LENGTH = 128
MAX_COLLECTION_NAME_LENGTH = 32
MAX_PASSPHRASE_LENGTH = 64


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
    # host = input("Enter the host, default is localhost, press enter to accept default: ")
    # user = input("Enter the current user, default is root, press enter to accept default: ")
    # password = input("Enter the password for the current user: ")

    # my login info for testing, remove before push
    host = "localhost"
    user = "root"
    password = "*Brendan10!"

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


def disconnect_database() -> None:
    """Safely disconnects from database and clears globals"""
    global _DB
    global _CURRENT_USER

    _DB.close()
    _DB = None
    _CURRENT_USER = None


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
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT movie_ID 
               FROM Movie 
               WHERE movie_title = %(title)s;""",
            {"title": title.lower()},
        )
        result = cursor.fetchall()
    if result == []:
        return []
    print(result[0][0])
    return result[0][0]


def search_for_movie_by_id(id: int) -> Movie:
    """Return a movie given its id

    Args:
        id - an int representing the id of a movie in the database

    Returns:
        a Movie object if the movie was found, else None
    """
    result = None
    songs = []
    crew_ids = []
    crew = {}
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT * 
               FROM Movie 
               WHERE movie_ID = %(id)s;""",
            {"id": id},
        )
        result = cursor.fetchone()
        if result is None:
            return None

    # there was a result
    movie_id, runtime, rating, num_ratings, title, score_id = result
    mov = Movie(movie_id, title, runtime, rating, num_ratings)

    # search for score
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT song 
               FROM Score_Songs
               WHERE score_ID = %(score_id)s;""",
            {"score_id": score_id},
        )
        result = cursor.fetchall()
    for tup in result:
        songs.append(tup[0])
    mov.set_score(score_id, songs)

    # search for crew ids
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT crew_ID
               FROM Crew_Movie
               WHERE movie_ID = %(id)s;""",
            {"id": id},
        )
        result = cursor.fetchall()
    for tup in result:
        crew_ids.append(tup[0])

    # append composers to crew ids
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT crew_ID
            FROM Score
            WHERE score_ID = %(score_id)s;""",
            {"score_id": score_id},
        )
        result = cursor.fetchall()
        for id in result:
            crew_ids.append(id[0])

    # search for crew names
    tmp_crew = {}
    for crew_id in crew_ids:
        with _DB.cursor() as cursor:
            cursor.execute(
                """SELECT crew_name
                FROM Crew
                WHERE crew_ID = %(crew_id)s;""",
                {"crew_id": crew_id},
            )
            result = cursor.fetchall()[0][0]
            tmp_crew[result] = crew_id

    # get crew jobs
    for crew_name, crew_id in tmp_crew.items():
        with _DB.cursor() as cursor:
            cursor.execute(
                """SELECT job
                FROM Crew_Job
                WHERE crew_ID = %(crew_id)s;""",
                {"crew_id": crew_id},
            )
            result = cursor.fetchall()[0]
            tmp = []
            for job in result:
                tmp.append(job)
            crew[crew_name] = tmp

    mov.set_crew(crew)
    return mov


def search_by_title_inexact(term: str) -> List[Movie]:
    """Returns search results that include the term in the move title (inexact match)
    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the title, may be None
    """
    results = []
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT movie_ID 
               FROM Movie 
               WHERE movie_title LIKE %(term)s;""",
            {"term": f"%{term.lower()}%"},
        )
        results = cursor.fetchall()
    if results == []:
        return []

    # flatten into list of IDs
    tmp = []
    for tup in results:
        tmp.append(tup[0])
    results = tmp

    # turn list of IDs into list of movies
    tmp = []
    for id in results:
        tmp.append(search_for_movie_by_id(id))

    return tmp


def search_by_crew_inexact(term: str) -> List[Movie]:
    """Returns search results that include the term in the crew field

    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in the crew field, may be None
    """
    results = []
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT movie_ID
               FROM Crew_Movie
               WHERE crew_ID = (
	            SELECT crew_ID
	            FROM Crew
	            WHERE crew_name like %(term)s;
                );""",
            {"term": f"%{term.lower()}%"},
        )
        results = cursor.fetchall()
    if results == []:
        return []

    # flatten into list of IDs
    tmp = []
    for tup in results:
        tmp.append(tup[0])
    results = tmp

    # turn list of IDs into list of movies
    tmp = []
    for id in results:
        tmp.append(search_for_movie_by_id(id))

    return tmp


def search_by_score_inexact(term: str) -> List[Movie]:
    """Returns search results that include the term in any song titles of the score field

    Args:
        term - a string we are filtering by

    Returns:
        a list of Movie objects that have the search term in a song in the score field, may be None
    """
    results = []
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT movie_ID
               FROM Movie
               WHERE movie_ID = (
	                SELECT score_ID
	                FROM Score_Songs
	                WHERE song like %(term)s;
            );""",
            {"term": f"%{term.lower()}%"},
        )
        results = cursor.fetchall()
    if results == []:
        return []

    # flatten into list of IDs
    tmp = []
    for tup in results:
        tmp.append(tup[0])
    results = tmp

    # turn list of IDs into list of movies
    tmp = []
    for id in results:
        tmp.append(search_for_movie_by_id(id))

    return tmp


def add_log(movie_id: int, rating: float) -> None:
    """Adds a log to a movie in the database
    Does not do any error checking

    Args:
        movie_id - an int representing the id of the movie we want
        rating - a float representing the rating given
    """
    current_rating = num_ratings = 0

    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT average_rating, num_ratings
            FROM movie
            WHERE movie_ID = %(movie_id)s""",
            {"movie_id": movie_id},
        )
        current_rating, num_ratings = cursor.fetchall()[0]

    total_score = current_rating * num_ratings
    new_total_score = total_score + rating
    num_ratings += 1
    new_average_rating = round(new_total_score / num_ratings, 2)

    with _DB.cursor() as cursor:
        cursor.execute(
            """UPDATE Movie
            SET average_rating = %(new_average_rating)s, num_ratings = %(num_ratings)s 
            WHERE movie_ID = %(movie_id)s""",
            {
                "new_average_rating": new_average_rating,
                "num_ratings": num_ratings,
                "movie_id": movie_id,
            },
        )
        _DB.commit()


def add_movie_to_database(mov: Movie) -> Movie:
    """Adds a movie to the database & returns the properly formatted movie

    Args:
        mov - a movie object to be added to database

    Returns:
        a Movie object containing the same data, but properly formatted
    """
    run_time = mov.get_runtime()
    avg_rating = mov.get_avg_rating()
    num_ratings = mov.get_num_rating()
    movie_title = mov.get_title()
    movie_id = -1

    # add the movie
    with _DB.cursor() as cursor:
        cursor.execute(
            """INSERT INTO Movie(run_time, average_rating, num_ratings, movie_title)
            VALUES (%(run_time)s, %(avg_rating)s, %(num_ratings)s, %(movie_title)s);""",
            {
                "run_time": run_time,
                "avg_rating": avg_rating,
                "num_ratings": num_ratings,
                "movie_title": movie_title.lower(),
            },
        )

    # get the id - no error checking since we just added it
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT movie_ID 
               FROM Movie 
               WHERE movie_title = %(movie_title)s AND run_time = %(run_time)s;""",
            {
                "movie_title": movie_title.lower(),
                "run_time": run_time,
            },
        )
        movie_id = cursor.fetchall()[0][0]

    # check for composer
    composer_name = ""
    for crew_name, roles in mov.get_crew().items():
        print(f"{crew_name}: {roles}")
        if roles[0].lower() == "composer":
            composer_name = crew_name
            break
    if composer_name == "":
        mov.add_crew_member("Unknown Composer", ["Composer"])

    # find the existing crew members
    tmp_crew = mov.get_crew()
    results = []
    for crew_name, roles in tmp_crew.items():
        with _DB.cursor() as cursor:
            cursor.execute(
                """SELECT *
                FROM Crew
                WHERE crew_name = %(crew_name)s;""",
                {"crew_name": crew_name.lower()},
            )
            results.append(cursor.fetchall())

    # prune existing crew from tmp_crew
    for result in results:
        try:
            cur_crew_id, name = result[0]
            tmp_crew.pop(name)

            # insert new movie for existing crew
            with _DB.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO Crew_Movie(crew_ID, movie_ID)
                    VALUES (%(cur_crew_id)s, %(movie_id)s);""",
                    {
                        "cur_crew_id": cur_crew_id,
                        "movie_id": movie_id,
                    },
                )
                _DB.commit()
        except:
            continue

    # add remaining crew members
    for crew_name, roles in tmp_crew.items():
        with _DB.cursor() as cursor:
            cursor.execute(
                """INSERT INTO Crew(crew_name)
                VALUES (%(crew_name)s);""",
                {"crew_name": crew_name.lower()},
            )
            _DB.commit()

    # get new crew IDs, put them after the job in tmp_crew
    for crew_name, roles in tmp_crew.items():
        with _DB.cursor() as cursor:
            cursor.execute(
                """SELECT crew_ID
                FROM Crew
                WHERE crew_name = %(crew_name)s;""",
                {"crew_name": crew_name.lower()},
            )
            roles.append(cursor.fetchall()[0])

    # set new crew jobs
    for crew_name, roles in tmp_crew.items():
        job = roles[0]
        id_solo = roles[1][0]
        with _DB.cursor() as cursor:
            cursor.execute(
                """INSERT INTO Crew_Job(job, crew_ID)
                VALUES (%(job)s, %(id_solo)s)""",
                {
                    "job": job,
                    "id_solo": id_solo,
                },
            )
            _DB.commit()

    # set new crew movie cross tables
    for crew_name, roles in tmp_crew.items():
        with _DB.cursor() as cursor:
            cursor.execute(
                """INSERT INTO Crew_Movie(crew_ID, movie_ID)
                VALUES (%(crew_ID)s, %(movie_id)s);""",
                {
                    "crew_ID": roles[1][0],
                    "movie_id": movie_id,
                },
            )
            _DB.commit()

    # get composer id
    composer_id = -1
    composers = []
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT crew_ID
                FROM Crew_Job
                WHERE job = 'composer';""",
        )
        for tup in cursor.fetchall():
            composers.append(tup[0])

    this_movie_ids = []
    with _DB.cursor() as cursor:
        cursor.execute(
            """SELECT crew_ID
                FROM Crew_Movie
                WHERE movie_ID = %(movie_id)s;""",
            {"movie_id": movie_id},
        )
        for tup in cursor.fetchall():
            this_movie_ids.append(tup[0])

    for composer in composers:
        if composer in this_movie_ids:
            composer_id = composer

    # put composer id into Score table
    with _DB.cursor() as cursor:
        cursor.execute(
            """INSERT INTO Score(score_ID, crew_ID)
            VALUES (%(score_ID)s, %(composer_id)s);""",
            {
                "score_ID": movie_id,
                "composer_id": composer_id,
            },
        )
        _DB.commit()

    # link songs to Score if it exists
    if mov.get_score() != None:
        print(f"There are {len(mov.get_score())}")
        i = 1
        for song in mov.get_score():
            print(f"Adding song: {song}")
            with _DB.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO Score_Songs(song, score_ID, track_number)
                    VALUES (%(song)s, %(score_id)s, %(track_number)s);""",
                    {
                        "song": song,
                        "score_id": movie_id,
                        "track_number": i,
                    },
                )
                _DB.commit()
                i += 1

    # update to add score_id via movie_id
    with _DB.cursor() as cursor:
        cursor.execute(
            """UPDATE Movie
            SET score_ID = %(score_id)s
            WHERE movie_ID = %(movie_id)s""",
            {
                "score_id": movie_id,
                "movie_id": movie_id,
            },
        )
        _DB.commit()

    return search_for_movie_by_id(movie_id)

    # testing cleanup
    # with _DB.cursor() as cursor:
    #     cursor.execute(
    #         """DELETE FROM Score_Songs
    #         WHERE score_ID = %(score_id)s;""",
    #         {"score_id": movie_id},
    #     )
    #     _DB.commit()

    # with _DB.cursor() as cursor:
    #     cursor.execute(
    #         """DELETE FROM Score
    #         WHERE crew_ID = %(composer_id)s;""",
    #         {"composer_id": composer_id},
    #     )
    #     _DB.commit()

    # for crew_name, roles in tmp_crew.items():
    #     with _DB.cursor() as cursor:
    #         cursor.execute(
    #             """DELETE FROM Crew_Job
    #             WHERE crew_ID = %(crew_id)s;""",
    #             {"crew_id": roles[1][0]},
    #         )
    #         _DB.commit()

    # for crew_name, roles in tmp_crew.items():
    #     with _DB.cursor() as cursor:
    #         cursor.execute(
    #             """DELETE FROM Crew_Movie
    #             WHERE crew_ID = %(crew_id)s;""",
    #             {"crew_id": roles[1][0]},
    #         )
    #         _DB.commit()

    # for crew_name, roles in tmp_crew.items():
    #     with _DB.cursor() as cursor:
    #         cursor.execute(
    #             """DELETE FROM Crew
    #             WHERE crew_name = %(crew_name)s;""",
    #             {"crew_name": crew_name.lower()},
    #         )
    #         _DB.commit()
