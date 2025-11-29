from database import SessionLocal, init_db
from services.movie_service import MovieService
from utils.api_manager import APIManager
import webbrowser

def main():
    print("--- Movie Rating & Archiving System ---")

    init_db()
    db = SessionLocal()
    movie_service = MovieService()
    api_manager = APIManager(api_key="6523d141f924d3a8ad4726be5021b873")

    title = "Dune"
    details = api_manager.search_movie_details(title)

    from models.models import Movie
    existing_movie = db.query(Movie).filter_by(tmdb_id=details['tmdb_id']).first() if details else None

    if existing_movie:
        print(f"Film zaten mevcut: {existing_movie.name}")
    elif details:
        new_movie = movie_service.add_movie_by_title(db, title)
        if new_movie:
            print(f"Eklendi: {new_movie.name} (API puanı: {new_movie.external_rating})")
        else:
            print("Film eklenemedi veya API hatası.")
    else:
        print("Film bulunamadı veya API hatası.")

    # IMDb Top 250 sayfasını aç
    imdb_url = "https://www.imdb.com/chart/top/"
    print(f"IMDb sayfası açılıyor: {imdb_url}")
    webbrowser.open(imdb_url)

    db.close()

if __name__ == "__main__":
    main()





