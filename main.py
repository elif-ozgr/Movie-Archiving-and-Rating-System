from database import SessionLocal, init_db
from services.movie_service import MovieService

def main():
    print("--- Movie Rating & Archiving System (Multi-file Version) ---")

    init_db()  # Tabloları oluştur

    db = SessionLocal()
    movie_service = MovieService()

    # Örnek film ekleme
    new_movie = movie_service.add_movie_by_title(db, "Dune")
    if new_movie:
        print(f"Eklendi: {new_movie.name} (API puanı: {new_movie.external_rating})")
    else:
        print("Film zaten mevcut veya API hatası.")

    db.close()

if __name__ == "__main__":
    main()
