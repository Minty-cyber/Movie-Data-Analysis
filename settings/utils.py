import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Dict, Any


def get_retry_session(
    retries: int = 5,
    backoff_factor: float = 1,
    status_forcelist: List[int] = None,
    allowed_methods: List[str] = None
):
    """
    A retry-session logic with backoff and jitter
    """
    session = requests.Session()

    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist or [429, 500, 502, 503, 504],
        allowed_methods=allowed_methods or ["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

def run_threaded(
    worker_fn: Callable[[Any], Any],
    items: List[Any],
    max_workers: int = 10
) -> Dict[Any, Any]:
    """
    Runs the worker in parallel to increase speed
    Returns a dictionary mapping input -> result.
    """
    results: Dict[Any, Any] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker_fn, item): item for item in items}

        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()

    return results
