CREATE DATABASE Betterboxd;

USE Betterboxd;

CREATE TABLE Crew (
    crew_ID	INT AUTO_INCREMENT,
    crew_name    VARCHAR(128),
    PRIMARY KEY (crew_ID)
);

CREATE TABLE Crew_Job (
    job     VARCHAR(32),
    crew_ID INT,
    FOREIGN KEY (crew_ID) REFERENCES Crew (crew_ID)
);

CREATE TABLE Score (
    score_ID INT,
    crew_ID  INT,
    PRIMARY KEY (score_ID, crew_ID),
    FOREIGN KEY (crew_ID) REFERENCES Crew (crew_ID)
);

CREATE TABLE Score_Songs (
    song         VARCHAR(128),
    score_ID     INT,
    track_number VARCHAR(2),
    FOREIGN KEY (score_ID) REFERENCES Score (score_ID)
);

CREATE TABLE Movie (
    movie_ID       INT AUTO_INCREMENT,
    run_time       TIME,
    average_rating FLOAT,
    num_ratings    INT,
    movie_title    VARCHAR(128),
    score_ID       INT,
    PRIMARY KEY (movie_ID),
    FOREIGN KEY (score_ID) REFERENCES Score (score_ID)
);

CREATE TABLE Collections (
    collection_ID    INT AUTO_INCREMENT,
    collection_name  VARCHAR(32),
    PRIMARY KEY (collection_ID)
);

CREATE TABLE Entry (
    collection_ID INT,
    movie_ID      INT,
    ranking       INT,
    PRIMARY KEY (collection_ID, movie_ID),
    FOREIGN KEY (collection_ID) REFERENCES Collections (collection_ID),
    FOREIGN KEY (movie_ID) REFERENCES Movie (movie_ID)
);

CREATE TABLE Account (
    account_name   VARCHAR(32),
    favorite_movie INT,
    watch_count    INT,
    passphrase     VARCHAR(64),
    PRIMARY KEY (account_name),
    FOREIGN KEY (favorite_movie) REFERENCES Movie (movie_ID)
);

CREATE TABLE Crew_Movie (
    crew_ID  INT,
    movie_ID INT,
    PRIMARY KEY (crew_ID, movie_ID),
    FOREIGN KEY (crew_ID) REFERENCES Crew (crew_ID),
    FOREIGN KEY (movie_ID) REFERENCES Movie (movie_ID)
);

CREATE TABLE Account_Collections (
    account_name VARCHAR(32),
    collection_ID    INT,
    PRIMARY KEY (account_name, collection_ID),
    FOREIGN KEY (account_name)  REFERENCES Account (account_name),
    FOREIGN KEY (collection_ID) REFERENCES Collections (collection_ID)
);