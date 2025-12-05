from database import SessionLocal, init_db
from services.movie_service import MovieService
from utils.api_manager import APIManager
import webbrowser

def main():
    print("--- Movie Rating & Archiving System ---")

    # 1. Initialize database and open session
    init_db()
    db = SessionLocal()
    
    # 2. Create service and API manager
    movie_service = MovieService()
    # Make sure API key is correct and up-to-date
    api_manager = APIManager(api_key="6523d141f924d3a8ad4726be5021b873") 

    # 3. Search and process movie
    title = "Dune"
    details = api_manager.search_movie_details(title)

    from models.models import Movie
    existing_movie = db.query(Movie).filter_by(tmdb_id=details['tmdb_id']).first() if details else None

    if existing_movie:
        print(f"Movie already exists: {existing_movie.name}")
    elif details:
        new_movie = movie_service.add_movie_by_title(db, title)
        if new_movie:
            print(f"Added: {new_movie.name} (API rating: {new_movie.external_rating})")
        else:
            print("Movie could not be added or API error.")
    else:
        print("Movie not found or API error.")

    # 4. Open IMDb Top 250 page
    imdb_url = "https://www.imdb.com/chart/top/"
    print(f"Opening IMDb page: {imdb_url}")
    webbrowser.open(imdb_url)

    # 5. Close session
    db.close()

# Standard Python entry point
if __name__ == "__main__":
    main()
