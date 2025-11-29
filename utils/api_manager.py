import requests

class APIManager:
    TMDB_API_KEY = "DEMO_KEY"  
    BASE_URL = "https://api.themoviedb.org/3"

    def search_movie_details(self, title: str):
        endpoint = f"{self.BASE_URL}/search/movie"
        params = {"api_key": self.TMDB_API_KEY, "query": title}

        try:
            resp = requests.get(endpoint, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            if data.get("results"):
                movie = data["results"][0]
                return {
                    "tmdb_id": movie["id"],
                    "external_rating": round(movie.get("vote_average", 0.0), 1),
                    "release_year": int(movie.get("release_date", "0000")[:4])
                }

            return None

        except Exception as e:
            print("API hatası:", e)
            return None
