import requests
from typing import Optional, Dict, Any


class APIManager:
    """TMDB API ile iletişim kurar."""

    # Senin TMDB API KEY'in (hard-coded versiyon)
    TMDB_API_KEY = "6523d141f924d3a8ad4726be5021b873"
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key: Optional[str] = None):
        """
        İstenirse dışarıdan API key alınır.
        Alınmazsa class içindeki default key kullanılır.
        """
        self.api_key = api_key or self.TMDB_API_KEY

    def search_movie_details(self, title: str) -> Optional[Dict[str, Any]]:
        """Verilen film adıyla TMDB'den detayları çeker."""
        endpoint = f"{self.BASE_URL}/search/movie"
        params = {"api_key": self.api_key, "query": title}

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = data.get("results")
            if not results:
                return None

            movie = results[0]

            tmdb_id = movie.get("id")
            overview = movie.get("overview", "")
            release_year = (
                movie.get("release_date", "")[:4]
                if movie.get("release_date")
                else None
            )
            external_rating = float(movie.get("vote_average", 0))

            # ➕ Daha kapsamlı bilgiler için ekstra API isteği
            genres = []
            if tmdb_id:
                details_url = f"{self.BASE_URL}/movie/{tmdb_id}"
                det_resp = requests.get(details_url, params={"api_key": self.api_key}, timeout=10)
                det_resp.raise_for_status()
                det_data = det_resp.json()

                # Daha detaylı overview
                overview = det_data.get("overview", overview)

                # Türler
                genres = [g["name"] for g in det_data.get("genres", [])]

            return {
                "tmdb_id": tmdb_id,
                "release_year": release_year,
                "external_rating": external_rating,
                "overview": overview,
                "genres": genres,
            }

        except Exception as e:
            print(f"[APIManager] Error: {e}")
            return None
