Movie Rating & Archiving System
Description:
This project is a modular movie rating and archiving application that collects film data (via the TMDB API or web scraping), normalizes it, stores it in a database, and manages it through a user interface. The project includes tests, linter configuration, sample data, and CI steps for a complete and professional submission.

Quick Overview:

Project Type:
Scraping / API + MySQL Database + Object-Oriented Programming
(fully meets all minimum project requirements)

Main Components:

models/ – SQLAlchemy ORM models

services/ – MovieService, RatingService, User services

utils/ – API manager, data dictionary, normalizer helpers

playwright_scraper.py – Dynamic scraping (IMDb Top 250)

database.py – MySQL engine and session management

gui.py – Optional graphical interface

main.py – Main entry point connecting all layers

sample/top10imdb_movies.txt – Sample dataset

drivers/ – ChromeDriver & setup executables for automation

Extra Features (Bonus Points):

Uses MySQL + SQLAlchemy ORM instead of basic SQLite

Fully modular architecture (Models → Services → Utils → Scrapers → GUI)

Requirements:

Common Requirements (Windows / macOS / Linux / VM):

Python 3.10+

MySQL Server 8.0+

Google Chrome (latest version)

Git

Python Dependencies:
All Python libraries are listed in requirements.txt. You can install them after creating a virtual environment.

Clone the Project:
git clone https://github.com/elif-ozgr/Movie-Archiving-and-Rating-System.git

cd yourproject

Create a Virtual Environment:

Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

Upgrade pip:
python -m pip install --upgrade pip

Install Required Packages:
python -m pip install SQLAlchemy
python -m pip install pymysql
python -m pip install requests
python -m pip install python-dotenv
python -m pip install cryptography
python -m pip install pytest
python -m pip install pylint

Generate requirements.txt (Optional):
python -m pip freeze > requirements.txt
or
python -m pip install -r requirements.txt

Environment Variables (.env file in project root):
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/Movie_Rating_and_Archiving_System
TMDB_API_KEY=6523d141f924d3a8ad4726be5021b873
TMDB_BASE_URL=https://api.themoviedb.org/3

Test Installation:
python -m pip list

Configure MySQL Database:

-- 1) Create the database
CREATE DATABASE Movie_Rating_and_Archiving_System;

-- 2) Select the database
USE Movie_Rating_and_Archiving_System;

-- 3) Users Table
CREATE TABLE Users (
user_id INT AUTO_INCREMENT PRIMARY KEY,
user_name VARCHAR(50) NOT NULL,
user_surname VARCHAR(50) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
join_date DATE NOT NULL,
password_hash VARCHAR(255) NOT NULL
);

INSERT INTO Users (user_id, user_name, user_surname, email, join_date, password_hash) VALUES
(1, 'Ahmet', 'Yıldırım', 'ahmet.yildirim@outlook.com
', '2023-05-01', '124456'),
(2, 'Azra', 'Karamir', 'azra.karamr@gmail.com
', '2023-06-10', 'abcdef'),
(3, 'Mehmet', 'Aydemir', 'mehmet.aydemir@gmail.com
', '2020-07-15', 'pass123'),
(4, 'Esra', 'Aydın', 'esra.aydin@outlook.com
', '2023-11-20', 'q7erty'),
(5, 'Burak', 'Korkmaz', 'burak.korkmaz@gmail.com
', '2020-09-18', '984654'),
(6, 'Zeynep', 'Merak', 'zeynep.merak@outlook.com
', '2023-10-06', 'zxdvb'),
(7, 'Ece', 'Acar', 'ece.acar@gmail.com
', '2003-11-12', 'password'),
(8, 'Kerem', 'Kaya', 'kerem.kaya@gmail.com
', '2023-12-01', 'aaa111'),
(9, 'Derya', 'Kuleli', 'derya.kuleli@outlook.com
', '2023-01-09', 'bcb222'),
(10, 'Erhan', 'Ak', 'erhan.ak@outlook.com
', '2004-02-14', 'c7c333');

-- 4) Genres Table
CREATE TABLE Genres (
genre_id INT AUTO_INCREMENT PRIMARY KEY,
genre_name VARCHAR(50) NOT NULL
);

INSERT INTO Genres (genre_id, genre_name) VALUES
(1, 'Comedy'), (2, 'Drama'), (3, 'Action'), (4, 'Science Fiction'),
(5, 'Adventure'), (6, 'Animation'), (7, 'Horror'), (8, 'Romantic'),
(9, 'Thriller'), (10, 'Mystery'), (11, 'Fantasy'), (12, 'Documentary'),
(13, 'Musical'), (14, 'Crime'), (15, 'Historical');

-- 5) Movies Table
CREATE TABLE Movies (
movie_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
director VARCHAR(100),
duration_minutes INT,
release_year INT,
description TEXT,
language VARCHAR(50),
genre_id INT,
FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);

INSERT INTO Movies (movie_id, name, director, duration_minutes, release_year, description, language, genre_id) VALUES
(1, 'Inception', 'Christopher Nolan', 148, 2010, 'A mind-bending science fiction thriller about dreams within dreams.', 'English', 4),
(2, 'Interstellar', 'Christopher Nolan', 169, 2014, 'A team travels through a wormhole to save humanity.', 'English', 4),
(3, 'The Shawshank Redemption', 142, 1994, 'Two imprisoned men bond over years, finding solace and eventual redemption.', 'English', 2),
(4, 'The Godfather', 'Francis Ford Coppola', 175, 1972, 'The aging patriarch transfers control to his reluctant son.', 'English', 14),
(5, 'Parasite', 'Bong Joon-ho', 132, 2019, 'A poor family infiltrates a wealthy household.', 'Korean', 9),
(6, 'Spirited Away', 'Hayao Miyazaki', 125, 2001, 'A girl enters a magical world of spirits.', 'Japanese', 6),
(7, 'The Dark Knight', 'Christopher Nolan', 152, 2008, 'Batman faces the Joker.', 'English', 3),
(8, 'Pulp Fiction', 'Quentin Tarantino', 154, 1994, 'Intersecting tales of crime in LA.', 'English', 14),
(9, 'La La Land', 'Damien Chazelle', 128, 2016, 'A jazz musician and actress pursue dreams.', 'English', 13),
(10, 'Avatar', 'James Cameron', 162, 2009, 'A marine joins the Na’vi tribe.', 'English', 11);

-- 6) Actors Table
CREATE TABLE Actors (
actor_id INT AUTO_INCREMENT PRIMARY KEY,
actor_name VARCHAR(100) NOT NULL,
nationality VARCHAR(50),
age INT
);

INSERT INTO Actors (actor_name, nationality, age) VALUES
('Leonardo DiCaprio', 'American', 48),
('Scarlett Johansson', 'American', 38),
('Tom Hanks', 'American', 67),
('Natalie Portman', 'Israeli-American', 42),
('Robert De Niro', 'American', 80),
('Emma Watson', 'British', 33),
('Will Smith', 'American', 55),
('Jennifer Lawrence', 'American', 33),
('Morgan Freeman', 'American', 86),
('Brad Pitt', 'American', 60),
('Gal Gadot', 'Israeli', 37),
('Chris Hemsworth', 'Australian', 40),
('Angelina Jolie', 'American', 50),
('Denzel Washington', 'American', 68),
('Anne Hathaway', 'American', 41);

-- 7) Ratings Table
CREATE TABLE Ratings (
rating_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
movie_id INT NOT NULL,
score INT CHECK(score BETWEEN 1 AND 10),
comment TEXT,
spoiler BOOLEAN DEFAULT FALSE,
FOREIGN KEY (user_id) REFERENCES Users(user_id),
FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

INSERT INTO Ratings (user_id, movie_id, score, comment, spoiler) VALUES
(1, 1, 9, 'Amazing movie!', FALSE),
(2, 1, 8, 'Great performances.', FALSE),
(3, 2, 7, 'Good but slow.', TRUE),
(4, 3, 10, 'Masterpiece!', FALSE),
(5, 4, 6, 'Ok, a bit slow.', FALSE);

-- 8) Archive Table
CREATE TABLE Archive (
archive_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
movie_id INT NOT NULL,
date_added DATE NOT NULL,
watching_status ENUM('not started','watching','finished') DEFAULT 'not started',
FOREIGN KEY (user_id) REFERENCES Users(user_id),
FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

INSERT INTO Archive (user_id, movie_id, date_added, watching_status) VALUES
(1, 1, '2025-01-10', 'not started'),
(1, 2, '2025-01-12', 'watching'),
(1, 3, '2025-01-15', 'finished');

-- 9) Management Table
CREATE TABLE Management (
management_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
admins BOOLEAN DEFAULT FALSE,
read_users BOOLEAN DEFAULT TRUE,
change_users BOOLEAN DEFAULT FALSE,
FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Management (user_id, admins, read_users, change_users) VALUES
(1, TRUE, TRUE, TRUE),
(2, FALSE, TRUE, FALSE),
(3, TRUE, TRUE, TRUE);

-- 10) Reports Table
CREATE TABLE Reports (
report_id INT AUTO_INCREMENT PRIMARY KEY,
high_score_movie_id INT,
most_watched_movie_id INT,
most_scored_movie_id INT,
most_archived_movie_id INT,
most_commented_movie_id INT,
FOREIGN KEY (high_score_movie_id) REFERENCES Movies(movie_id),
FOREIGN KEY (most_watched_movie_id) REFERENCES Movies(movie_id),
FOREIGN KEY (most_scored_movie_id) REFERENCES Movies(movie_id),
FOREIGN KEY (most_archived_movie_id) REFERENCES Movies(movie_id),
FOREIGN KEY (most_commented_movie_id) REFERENCES Movies(movie_id)
);

Known Issues / Limitations:

TMDB API rate limits may cause temporary failures on many requests.

User input validation for ratings/comments is basic; edge cases may not be fully handled.

Test database usage does not affect real database; users should be aware.

Minor environment differences may require adjusting paths or environment variables.

Credits / Acknowledgements:

-TMDB API (https://www.themoviedb.org/)

-IMDb (https://www.imdb.com/)

-Python, SQLAlchemy
