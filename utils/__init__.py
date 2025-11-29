import requests
from typing import Optional

class APIManager:
    TMDB_API_KEY = "DEMO_KEY"  # Gerçek projede kendi API key
    BASE_URL = "https://api.themoviedb.org/3"

    def search_movie_details(self, title: str) -> Optional[dict]:
        endpoint = f"{self.BASE_URL}/search/movie"
        params = {"api_key": self.TMDB_API_KEY, "query": title}

        try:
            response = requests.get(endpoint, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get('results'):
                first_result = data['results'][0]
                return {
                    "tmdb_id": first_result['id'],
                    "external_rating": round(first_result.get('vote_average', 0.0), 1),
                    "director": "API'dan director için ekstra çağrı gerekir",
                    "description": first_result.get('overview'),
                    "release_year": int(first_result.get('release_date', '0000')[:4])
                }
            return None
        except requests.exceptions.RequestException as e:
            print(f"API hatası: {e}")
            return None

