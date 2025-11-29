import requests

class APIManager:
    """TMDB API ile iletişim kurar."""

    def __init__(self, api_key: str = "6523d141f924d3a8ad4726be5021b873"):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    def search_movie_details(self, title: str):
        """Verilen film başlığına göre TMDB'den detayları çeker."""
        url = f"{self.base_url}/search/movie?api_key={self.api_key}&query={title}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['results']:
                movie = data['results'][0]
                return {
                    "tmdb_id": movie["id"],
                    "release_year": movie.get("release_date", "")[:4],
                    "external_rating": movie.get("vote_average", 0)
                }

            return None  # try bloğu içinde
        except requests.HTTPError as e:
            print(f"API hatası: {e}")
            return None  # except bloğu içinde
        except requests.RequestException as e:
            print(f"İstek hatası: {e}")
            return None






