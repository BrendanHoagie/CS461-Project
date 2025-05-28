from pages.homepage import home_page
from pages.startup import start_up

if __name__ == "__main__":
    print("|-- Welcome to Betterboxd! --|")
    # home_page(override=True)  # debug to avoid logging in for testing

    # once testing is over uncomment these and remove home_page call above
    start_up()
    home_page()
