import tkinter as tk
from tkinter import messagebox, ttk
# PIL and requests were used for posters, not needed now
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO

# Your project modules
from database import SessionLocal, init_db
from services.movie_service import MovieService
from utils.api_manager import APIManager
from models.models import Movie

# --------------------------
# 5 movies to add automatically
# --------------------------
AUTO_MOVIES = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "Fight Club",
    "Inception"
]

# --------------------------
# Movie adding functions
# --------------------------
def add_movie_by_title(title):
    init_db()
    db = SessionLocal()

    movie_service = MovieService()
    api_manager = APIManager(api_key="6523d141f924d3a8ad4726be5021b873")

    details = api_manager.search_movie_details(title)

    if not details:
        result_text.set("API error or movie not found.")
        db.close()
        return

    overview_text = details.get('overview', 'No description available.')
    short_overview = overview_text[:150] + "..." if len(overview_text) > 150 else overview_text

    existing = db.query(Movie).filter_by(tmdb_id=details['tmdb_id']).first()

    if existing:
        result_text.set(
            f"✅ Already exists: **{existing.name}** (Rating: {existing.external_rating})\n"
            f"Overview: {short_overview}"
        )
    else:
        new_movie = movie_service.add_movie_by_title(db, title)
        if new_movie:
            result_text.set(
                f"🎉 Added: **{new_movie.name}** (Rating: {new_movie.external_rating})\n"
                f"Overview: {short_overview}"
            )

    db.close()


def search_movie():
    title = entry_title.get()

    if not title.strip():
        messagebox.showwarning("Error", "Movie name cannot be empty!")
        return

    add_movie_by_title(title)


def add_auto_movies():
    """Automatically adds 5 movies."""
    added_count = 0

    for title in AUTO_MOVIES:
        init_db()
        db = SessionLocal()

        movie_service = MovieService()
        api_manager = APIManager(api_key="6523d141f924d3a8ad4726be5021b873")

        details = api_manager.search_movie_details(title)
        if not details:
            db.close()
            continue

        existing = db.query(Movie).filter_by(tmdb_id=details['tmdb_id']).first()

        if not existing:
            movie_service.add_movie_by_title(db, title)
            added_count += 1

        db.close()

    messagebox.showinfo("Completed", f"{added_count} movies were added automatically!")
    list_movies()


def list_movies():
    """Lists top 5 movies."""
    init_db()
    db = SessionLocal()

    movies = db.query(Movie).order_by(Movie.external_rating.desc()).limit(5).all()

    movie_list.delete(*movie_list.get_children())

    for m in movies:
        movie_list.insert("", tk.END, values=(m.name, m.external_rating))

    db.close()


# --------------------------
# GUI Design
# --------------------------
root = tk.Tk()
root.title("Movie Rating System")
root.geometry("700x550")

tk.Label(root, text="Movie Title:", font=("Arial", 12, "bold")).pack(pady=5)

entry_title = tk.Entry(root, font=("Arial", 13), width=30)
entry_title.pack(pady=5)

btn_search = tk.Button(root, text="Search & Add Movie", command=search_movie, font=("Arial", 12), bg="#4CAF50", fg="white")
btn_search.pack(pady=10)

btn_auto = tk.Button(root, text="Add 5 Automatic Movies", command=add_auto_movies, font=("Arial", 12), bg="#008CBA", fg="white")
btn_auto.pack(pady=10)

result_text = tk.StringVar()
description_label = tk.Label(root, textvariable=result_text, font=("Arial", 11), fg="#333", justify=tk.LEFT, wraplength=600)
description_label.pack(pady=15, padx=20)

tk.Label(root, text="Saved Movies (Top 5)", font=("Arial", 12, "bold")).pack(pady=10)

columns = ("Movie", "Rating")
movie_list = ttk.Treeview(root, columns=columns, show='headings', height=5)
movie_list.heading("Movie", text="Movie Title")
movie_list.heading("Rating", text="TMDB Rating")
movie_list.column("Movie", width=500, anchor=tk.W)
movie_list.column("Rating", width=100, anchor=tk.CENTER)
movie_list.pack(pady=10, fill=tk.X, padx=20)

btn_list = tk.Button(root, text="Refresh List (Top 5)", command=list_movies, font=("Arial", 12), bg="#f44336", fg="white")
btn_list.pack(pady=10)

root.mainloop()
