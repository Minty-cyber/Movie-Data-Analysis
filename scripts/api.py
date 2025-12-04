import requests
import os
from dotenv import load_dotenv
import logging
from typing import List, Optional, Dict
# from converter import json_to_dataframe

load_dotenv()

# instantiate api_key loading
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Logging configuration showing metadata like time. Currently logging in the command line.
_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=_log_level,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def extract_credit_info(movie: dict) -> dict:
    """Extract cast list, cast size, director, and crew size from TMDB credits.
    """

    credits = movie.get("credits", {})

    cast_list = [member.get("name") for member in credits.get("cast", []) if "name" in member]
    cast_size = len(cast_list)

    crew_list = credits.get("crew", [])
    crew_size = len(crew_list)

    director = None
    for member in crew_list:
        if member.get("job") == "Director":
            director = member.get("name")
            break

    return {
        "cast": cast_list,
        "cast_size": cast_size,
        "director": director,
        "crew_size": crew_size,
    }
    


def fetch_movies(movie_ids: List[int]) -> Dict[int, Optional[dict]]:
    """Fetch movie details for a list of Movie IDs.

    Returns a dictionary mapping movie_id -> movie data (or None if fetch failed).
    """
    movies = {}

    for movie_id in movie_ids:
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": API_KEY,
            "append_to_response": "credits"
        }
        logger.debug("Requesting movie %s with params %s", movie_id, params)
        try:
            resp = requests.get(url, params=params, timeout=10)
        except requests.RequestException as re:
            movies[movie_id] = None
            continue

        if resp.status_code == 200:
            try:
                data = resp.json()
                credit_info = extract_credit_info(data)
                data.update(credit_info)
                movies[movie_id] = data
                ## First start fetching movie titles to make sure the requests are going through
                # title = (
                #     movies[movie_id].get("title") if isinstance(movies[movie_id], dict) else None
                # )
            except ValueError:
                # Return a None value when there is an error(Graceful error handling)
                movies[movie_id] = None
        else:
            logger.error("Failed to fetch movie %s: status %s", movie_id, resp.status_code) 
            movies[movie_id] = None

    logger.info("Completed fetch, %d items processed", len(movie_ids))
    return movies


movie_ids = [
    0,
    299534,
    19995,
    140607,
    299536,
    597,
    135397,
    420818,
    24428,
    168259,
    99861,
    284054,
    12445,
    181808,
    330457,
    351286,
    109445,
    321612,
    260513,
]





# Test the script
if __name__ == "__main__":
    movies = fetch_movies(movie_ids)
    # dataframe = json_to_dataframe(movies)
    print(movies)
