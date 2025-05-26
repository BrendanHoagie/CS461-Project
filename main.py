import startup
import homepage


if __name__ == "__main__":
    print("|-- Welcome to Betterboxd! --|")
    # pass username from startup to homepage
    homepage.home_page(startup.start_up())
