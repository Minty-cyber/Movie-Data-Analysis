import requests
import os
from dotenv import load_dotenv
import logging
from typing import List, Optional, Dict
from settings.config import settings
from settings.utils import get_retry_session, run_threaded


API_KEY = settings.TMDB_API_KEY
BASE_URL = settings.TMDB_API_URL

session = get_retry_session()

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
  
def fetch_single_movie(movie_id: int) -> Optional[dict]:
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "append_to_response": "credits",
    }

    try:
        resp = session.get(url, params=params, timeout=10)
    except Exception:
        return None

    if resp.status_code != 200:
        return None

    try:
        data = resp.json()
        data.update(extract_credit_info(data))
        return data
    except Exception:
        return None



def fetch_movies(movie_ids: List[int]) -> Dict[int, Optional[dict]]:
    """Fetch movie details for a list of Movie IDs.

    Returns a dictionary mapping movie_id -> movie data (or None if fetch failed).
    """
    logger.info("Fetching %d movies...", len(movie_ids))

    movies = run_threaded(
        worker_fn=fetch_single_movie,
        items=movie_ids,
        max_workers=10,
    )

    logger.info("Completed fetch for %d movies", len(movie_ids))
    return movies

movie_ids = [
    0, 299534, 19995, 140607, 299536, 597,
    135397, 420818, 24428, 168259, 99861,
    284054, 12445, 181808, 330457, 351286,
    109445, 321612, 260513,
]


# Test the script
if __name__ == "__main__":
    movies = fetch_movies(movie_ids)
    # dataframe = json_to_dataframe(movies)
    print(movies)
