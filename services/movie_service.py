from utils.api_manager import APIManager
from database import SessionLocal
from models.models import Movie
from datetime import date

class MovieService:
    """CRUD ve İş Mantığı Servisi"""

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def add_movie_by_title(self, db, title: str):
        api_manager = APIManager()
        details = api_manager.search_movie_details(title)

        if details and not db.query(Movie).filter(Movie.tmdb_id == details['tmdb_id']).first():
            new_movie = Movie(
                name=title,
                release_year=details['release_year'],
                tmdb_id=details['tmdb_id'],
                external_rating=details['external_rating'],
                last_updated=date.today()
            )
            db.add(new_movie)
            db.commit()
            db.refresh(new_movie)
            return new_movie
        return None

