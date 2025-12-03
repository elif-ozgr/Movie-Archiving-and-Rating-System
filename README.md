# Movie-Archiving-and-Rating-System
SQL working
🚀 Movie Archiving and Rating System (IMDb + TMDB + MySQL)
This project is a comprehensive system that combines powerful modern tools (Playwright, MySQL, TMDB API) to dynamically scrape movie data, store it permanently, and manage it through a user-friendly desktop application (Tkinter).
Key Features
1. 🌐 Advanced Web Scraping (Playwright)
Modern Approach: Playwright is used instead of Selenium for faster and more reliable dynamic web interaction.

Target: IMDb's official Top 250 list (/chart/top/).
Data Extraction: Scrapes the names of the top 10 movies and saves them to a .txt file.
Browser Control: Can be run either visibly (headless=False) or in the background (headless=True).

2. 💾 Persistent Data Storage (MySQL)
Database: All movie data is stored in a local MySQL server.
SQLAlchemy ORM: A robust and reliable ORM layer is built using the mysql+pymysql connection string in the database.py file.
Automatic Setup: Tables are automatically created (init_db) when the application starts.

3. 🎬 API Integration (The Movie Database - TMDB)
Detailed Information: When a movie title is entered, the TMDB API is used to fetch details, the external rating, and the plot summary (overview).
Duplicate Check: Prevents the same movie from being added twice (based on the tmdb_id).

4. 🖥 Tkinter Desktop Application (GUI)
User-Friendly: Provides a fast and functional interface using tkinter.
Adding Modules: Features both search/add by title and the ability to batch-add 5 popular movies.
Feedback: Displays the rating and a short summary of the most recently added film instantly.
Listing: Displays the top 5 movies in the database, sorted by their rating, within a TreeView table.

⚙️ Requirements and Setup
Requirements
Python 3.x
Libraries: playwright, sqlalchemy, pymysql, requests, tkinter (Built-in)
Database: A running MySQL server instance.
