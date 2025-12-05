import requests
from typing import Optional

class APIManager:
    """Communicates with the TMDB API and retrieves movie details."""

    # Insert your own API key here
    TMDB_API_KEY = "6523d141f924d3a8ad4726be5021b873"  # Example: replace with your own key
    BASE_URL = "https://api.themoviedb.org/3"

    def search_movie_details(self, title: str) -> Optional[dict]:
        """Fetches movie data from TMDB based on the given title."""
        endpoint = f"{self.BASE_URL}/search/movie"
        params = {"api_key": self.TMDB_API_KEY, "query": title}

        try:
            response = requests.get(endpoint, params=params, timeout=5)
            response.raise_for_status()  # Catch HTTP errors
            data = response.json()

            if data.get('results'):
                first_result = data['results'][0]
                return {
                    "tmdb_id": first_result['id'],
                    "name": first_result.get('title'),
                    "external_rating": round(first_result.get('vote_average', 0.0), 1),
                    "release_year": int(first_result.get('release_date', '0000')[:4]) 
                        if first_result.get('release_date') else None,
                    "description": first_result.get('overview'),
                    "director": "Requires an additional API call to fetch director info"
                }
            else:
                print(f"Movie not found: {title}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return None
