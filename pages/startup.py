import utilities.utils as utils
import hashlib


def start_up() -> str:
    """Startup function for Betterboxd
    Acts as the entry point into the app, according to the flowchart,
    takes user input and handles unrecognized errors

    Returns:
        a string representing the currently logged in user
    """
    options = [{"Sign Up": sign_up}, {"Log In": log_in}]

    utils.clear_terminal()
    print("|-- Welcome to Betterboxd --|")
    print("What would you like to do?")
    while 1:
        for i, e in enumerate(options):
            print(f"{i + 1}. {list(e.keys())[0]}")
        try:
            choice = int(input(f"Enter a number 1-{i + 1}: ")) - 1
            if choice < 0:
                raise ValueError
            return list(options[choice].values())[0]()
        except Exception:
            print("Unrecognized input, please try again")


def sign_up() -> str:
    """Sign up function for Betterboxd
    Safely adds a new person to the database, handling user input

    Returns:
        a string representing the currently logged in user
    """
    username = password = ""
    username_max_length = 32
    password_max_length = 64  # are these values right?

    utils.clear_terminal()
    print("|-- Sign Up for Betterboxd --|")

    # get username
    while 1:
        username = input("Enter your username (max 32 characters): ").lower()
        if len(username) <= username_max_length:
            # replace me with SQL query
            if not utils.user_exists(username):
                break
            print("Sorry, a user with that name already exists, please choose another one")
        else:
            print("Sorry, that username is too long, please try again")

    # get password
    while 1:
        password = input("Enter your password (max 32 characters): ")
        if len(password) <= password_max_length:
            break
        print("Sorry, that password is too long, please try again")

    # hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # replace me with SQL add to database
    utils.add_to_users(username, hashed_password)
    return username


def log_in() -> str:
    """Log in function for Betterboxd
    Safely checks if a user is in the database

    Returns:
        a string representing the currently logged in user
    """
    username = password = ""
    failed_attempts = 0
    max_failed_attempts = 3

    # TODO: May want to restructure this to do just 1 SQL lookup instead of 2

    utils.clear_terminal()
    print("|-- Log In To Betterboxd --|")

    # get the username
    while 1:
        username = input("Enter your username: ")

        # replace me with an SQL lookup
        if utils.user_exists(username):
            break

        print("User not found, try again")
        failed_attempts += 1

        # if they fail too many times let them go back
        if failed_attempts == max_failed_attempts:
            print(
                f"Username lookup failed {failed_attempts} times, would you like to create an account instead?"
            )
            if input("Type 1 for yes, anything else to keep trying: ") == "1":
                return sign_up()
            failed_attempts = 0
    failed_attempts = 0

    # get the password
    while 1:
        password = input("Enter your password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # replace me with an SQL lookup
        if utils.password_correct(username, hashed_password):
            break

        print("Incorrect password, try again")
        failed_attempts += 1

        # if they fail too many times let them go back
        if failed_attempts == max_failed_attempts:
            print(
                f"Username lookup failed {failed_attempts} times, would you like to create an account instead?"
            )
            if input("Type 1 for yes, anything else to keep trying: ") == "1":
                return sign_up()
            failed_attempts = 0

    # treat them as logged in
    return username
