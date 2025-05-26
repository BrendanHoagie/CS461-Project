import os


# this is an example, will be replaced when we add SQL
USERS = {
    "brendan": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",  # pass: hello
    "randy": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",  # pass: test
    "dante": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",  # pass: 123
}


def add_to_users(username: str, password: str) -> None:
    """Add to the username database"""
    USERS[username] = password


def user_exists(username: str) -> bool:
    """Query if user is already in database"""
    return username in USERS


def password_correct(username: str, password: str) -> bool:
    """Query if password is correct for the given username"""
    return password == USERS[username]


# this is an example to be changed when we add SQL
MOVIES = [
    [
        "Hatari!",
        ["Adventure, Comedy"],
        157,
        {
            "John Wayne": ["Actor", "Producer"],
            "Howard Hanks": ["Director", "Producer"],
            "Henry Mancini": ["Composer"],
        },
        ["Theme from 'Hatari!'", "Baby Elephant Walk", "Just for Tonight"],
        [1.5, 4.5, 3.0],
        3,
        {1: ["I did not like it"], 2: ["I'm a big fan!", "I still really love it, man"], 3: []},
    ],
]


def clear_terminal() -> None:
    """Clear the terminal on Windows & Linux"""
    os.system("cls" if os.name == "nt" else "clear")
