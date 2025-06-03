from pages.homepage import home_page
from pages.startup import start_up
from utilities.utils import disconnect_database

if __name__ == "__main__":
    print("|-- Welcome to Betterboxd! --|")
    try:
        start_up()
        home_page()
    except KeyboardInterrupt:
        disconnect_database()
