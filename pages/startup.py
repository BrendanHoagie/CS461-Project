import utilities.utils as utils
import hashlib


def start_up():
    """Startup function for Betterboxd
    Acts as the entry point into the app, according to the flowchart,
    takes user input and handles unrecognized errors
    """
    options = [
        {"Sign Up": sign_up},
        {"Log In": log_in},
    ]

    utils.set_up_database()
    utils.clear_terminal()
    print("What would you like to do?")
    user = utils.take_cli_input_with_options(options)().lower()
    utils.set_current_user(user)


def sign_up() -> str:
    """Sign up function for Betterboxd
    Safely adds a new person to the database, handling user input

    Returns:
        a string representing the currently logged in user
    """
    username = password = ""

    utils.clear_terminal()
    print("|-- Sign Up for Betterboxd --|")

    # get username
    while 1:
        username = input(
            f"Enter your username (max {utils.MAX_USERNAME_LENGTH} characters): "
        ).lower()
        if len(username) <= utils.MAX_USERNAME_LENGTH:

            if not utils.user_exists(username):
                break
            print("Sorry, a user with that name already exists, please choose another one")
        else:
            print("Sorry, that username is too long, please try again")

    # get password
    while 1:
        password = input(f"Enter your password (max {utils.MAX_PASSWORD_LENGTH} characters): ")
        if len(password) <= utils.MAX_PASSWORD_LENGTH:
            break
        print("Sorry, that password is too long, please try again")

    # hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

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

    utils.clear_terminal()
    print("|-- Log In To Betterboxd --|")

    # get the username
    while 1:
        username = input("Enter your username: ")
        if len(username) <= utils.MAX_USERNAME_LENGTH and utils.user_exists(username):
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
