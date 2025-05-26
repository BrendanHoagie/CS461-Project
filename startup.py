import hashlib

USERS = {"account1": "password123"}
CURRENT_USER = None


def start_up() -> str:
    """Startup function for Betterboxd
    Acts as the entry point into the app, according to the flowchart,
    takes user input and handles unrecognized errors

    Returns:
        a string representing the currently logged in user
    """
    choices = {"Sign Up": sign_up, "Log In": log_in}

    print("What would you like to do?")
    while 1:
        i = 1
        for k in choices:
            print(f"{i}. {k}")
            i += 1
        try:
            return choices.get(int(input(f"Enter a number 1-{i - 1}: ")))()

        # first three are for debugging, in release can be just general exception w/o debug print
        except KeyError as ke:
            print(f"DEBUG KEY ERROR: {ke}")
            print("Unrecognized input, please try again")

        except ValueError as ve:
            print(f"DEBUG VALUE ERROR: {ve}")
            print("Unrecognized input, please try again")

        except TypeError as te:
            print(f"DEBUG TYPE ERROR: {te}")
            print("Unrecognized input, please try again")

        except Exception as e:
            print(f"DEBUG EXCEPTION: {e}")
            print("Unrecognized input, please try again")


def sign_up() -> str:
    """Sign up function for Betterboxd
    Safely adds a new person to the database, handling user input

    Returns:
        a string representing the currently logged in user
    """
    username, password = ""
    username_max_length = 32
    password_max_length = 64  # are these values right?

    # get username
    while 1:
        username = input("Enter your username (max 32 characters): ")
        if len(username) > username_max_length:
            # replace me with SQL query
            if not username in USERS.keys:
                break
        print("Sorry, that username is too long, please try again")

    # get password
    while 1:
        password = input("Enter your password (max 32 characters): ")
        if len(password) > password_max_length:
            break
        print("Sorry, that password is too long, please try again")

    # hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # enter to db
    USERS[username] = hashed_password
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

    ### May want to restructure this to do just 1 SQL lookup instead of 2

    # get the username
    while 1:
        username = input("Enter your username: ")
        # replace me with an SQL lookup
        if username in USERS.keys:
            break

        print("User not found, try again")
        failed_attempts += 1

        # if they fail too many times let them go back
        if failed_attempts == max_failed_attempts:
            print(
                f"Username lookup failed {failed_attempts} times, would you like to create an account instead?"
            )
            username = input("Type 1 for yes, anything else to keep trying: ")
            if username == "1":
                sign_up()
            failed_attempts = 0
    failed_attempts = 0

    # get the password
    while 1:
        password = input("Enter your password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # replace me with an SQL lookup
        if hashed_password == USERS[username]:
            break

        print("incorrect password, try again")
        failed_attempts += 1

        # if they fail too many times let them go back
        if failed_attempts == max_failed_attempts:
            print(
                f"Username lookup failed {failed_attempts} times, would you like to create an account instead?"
            )
            password = input("Type 1 for yes, anything else to keep trying: ")
            if password == "1":
                sign_up()
            failed_attempts = 0

    # treat them as logged in
    return username
