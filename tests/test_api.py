import pytest
from unittest.mock import patch, MagicMock
from extract.api import fetch_movies

@patch("extract.api.session.get")
def test_fetch_movies_success(mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"title": "Fake Movie", "credits": {}}

    mock_get.return_value = fake_response

    movie_ids = [12, 456, 743]
    movies = fetch_movies(movie_ids)

    for mid in movie_ids:
        assert movies[mid]["title"] == "Fake Movie"


@patch("extract.api.session.get")
def test_fetch_movies_failure(mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 404

    mock_get.return_value = fake_response

    movies = fetch_movies([999])
    assert movies[999] is None
