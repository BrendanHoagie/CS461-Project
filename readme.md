# CS 461 - BHM Project
Our project is called Betterboxd, it's a movie app inspired by the website Letterboxd. \
Created by: \
Brendan Hoag <beh73@drexel.edu> \
Dante C. Barbosa-Toney <dcb333@drexel.edu> \
Randy Modglin <rjm433@drexel.edu>

# What's included
## Python
- `main.py`: the entry point of the application
- `pages/`: a folder containing the code for the equivalent of webpages if our app was a website
- `utilities/`: a folder containing the python objects the front end works with
    - `utils.py` is a large utility file that primarily interfaces between the python application and the mysql database. If you were looking for SQL calls to grade, it would be here.
## SQL_files
- This is a folder that contains all of our `.sql` files that you will need to run in order to set up the database
- The sql files are numbered from 0 to 7, this is the order they should be run in

# Setup
## Setting Up MySQL
- Download mySQL 8.0.42 from the [website](https://dev.mysql.com/downloads/installer/), and go through the installation process
- It will ask you to set a username and password when you run it, please note these down, as they will be needed later. If you are not running this locally, please also note down the host. Keep this running for the duration of the time working with the app.
## Creating the Betterboxd Database
- Please ensure you do not already have an existing database in mysql called Betterboxd. If you do, please `DROP DATABASE Betterboxd;` to start with a clean slate
- You will be sourcing each of the 11 files found in `sql_files/`. You will do this by running `source absolute/path/to/file.sql` in the mysql terminal. It is important that it is an absolute path, and it is important to not have quotes around the filepath
- Do this starting at `0_tables.sql` through `10_account_collections.sql`, and you will have successfully set up the database!
## Setting Up Python
- Ensure you have `python 3` installed on your computer and its package manager `pip`
- To install the mysql python connector package, in the root of the project run `python -m pip install mysql-connector-python`. This will install the library specific to mysql that allows python to interface with it
- Finally, in the root of the project, run `python3 main.py`. This will bring you to the start of the application, where you will be asked to enter you mysql information from earlier. Once this has been entered and validated, only then will you be prompted to sign up or log into the app, and from there you will be on the homescreen.

