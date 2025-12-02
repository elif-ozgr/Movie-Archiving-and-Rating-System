import tkinter as tk
from tkinter import messagebox, ttk
# PIL ve requests kütüphaneleri poster için gerekliydi, artık değil.
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO

# Senin proje modüllerin
from database import SessionLocal, init_db
from services.movie_service import MovieService
from utils.api_manager import APIManager
from models.models import Movie

# --------------------------
# Otomatik eklenecek 5 film
# --------------------------
AUTO_MOVIES = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "Fight Club",
    "Inception"
]

# --------------------------
# Film ekleme fonksiyonları
# --------------------------
def add_movie_by_title(title):
    init_db()
    db = SessionLocal()

    movie_service = MovieService()
    api_manager = APIManager(api_key="6523d141f924d3a8ad4726be5021b873")

    details = api_manager.search_movie_details(title)

    if not details:
        result_text.set("API hatası veya film bulunamadı.")
        db.close()
        return

    # API'den gelen açıklama metnini alalım (overview)
    overview_text = details.get('overview', 'Açıklama mevcut değil.')
    # Açıklamayı GUI'da daha okunaklı göstermek için kısaltalım
    short_overview = overview_text[:150] + "..." if len(overview_text) > 150 else overview_text

    existing = db.query(Movie).filter_by(tmdb_id=details['tmdb_id']).first()

    if existing:
        result_text.set(
            f"✅ Zaten kayıtlı: **{existing.name}** (Puan: {existing.external_rating})\n"
            f"Özet: {short_overview}"
        )
    else:
        new_movie = movie_service.add_movie_by_title(db, title)
        if new_movie:
            result_text.set(
                f"🎉 Eklendi: **{new_movie.name}** (Puan: {new_movie.external_rating})\n"
                f"Özet: {short_overview}"
            )

    db.close()


def search_movie():
    title = entry_title.get()

    if not title.strip():
        messagebox.showwarning("Hata", "Film adı boş bırakılamaz!")
        return

    add_movie_by_title(title)


def add_auto_movies():
    """5 filmi otomatik ekler."""
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

    messagebox.showinfo("Tamamlandı", f"{added_count} film otomatik olarak eklendi!")
    list_movies()


def list_movies():
    """İlk 5 filmi listeler."""
    init_db()
    db = SessionLocal()

    # Puanı yüksekten düşüğe doğru sıralayalım
    movies = db.query(Movie).order_by(Movie.external_rating.desc()).limit(5).all()

    movie_list.delete(*movie_list.get_children())

    for m in movies:
        movie_list.insert("", tk.END, values=(m.name, m.external_rating))

    db.close()


# --------------------------
# GUI Tasarımı
# --------------------------
root = tk.Tk()
root.title("Movie Rating System")
root.geometry("700x550") # Pencere boyutunu küçülttük

tk.Label(root, text="Film Adı:", font=("Arial", 12, "bold")).pack(pady=5)

entry_title = tk.Entry(root, font=("Arial", 13), width=30)
entry_title.pack(pady=5)

btn_search = tk.Button(root, text="Filmi Ara & Ekle", command=search_movie, font=("Arial", 12), bg="#4CAF50", fg="white")
btn_search.pack(pady=10)

btn_auto = tk.Button(root, text="5 Otomatik Film Ekle", command=add_auto_movies, font=("Arial", 12), bg="#008CBA", fg="white")
btn_auto.pack(pady=10)

# Açıklama metni için alan
result_text = tk.StringVar()
description_label = tk.Label(root, textvariable=result_text, font=("Arial", 11), fg="#333", justify=tk.LEFT, wraplength=600)
description_label.pack(pady=15, padx=20)


# Film listesi
tk.Label(root, text="Kayıtlı Filmler (En İyi 5)", font=("Arial", 12, "bold")).pack(pady=10)

columns = ("Film", "Puan")
movie_list = ttk.Treeview(root, columns=columns, show='headings', height=5)
movie_list.heading("Film", text="Film Adı")
movie_list.heading("Puan", text="TMDB Puanı")
movie_list.column("Film", width=500, anchor=tk.W)
movie_list.column("Puan", width=100, anchor=tk.CENTER)
movie_list.pack(pady=10, fill=tk.X, padx=20)

btn_list = tk.Button(root, text="Listeyi Güncelle (İlk 5)", command=list_movies, font=("Arial", 12), bg="#f44336", fg="white")
btn_list.pack(pady=10)

root.mainloop()