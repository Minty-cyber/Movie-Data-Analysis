import pytest
import pandas as pd
from scripts.search import (
    apply_filter,
    search_sci_fi,
    search_uma_by_tarantino,
)


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def movie_df():
    """
    Dataset fixture for datasets in the whole test suite here
    """
    return pd.DataFrame({
        "title": [
            "Looper", "Fifth Element", "Pulp Fiction",
            "Kill Bill", "Random Movie"
        ],
        "genres": [
            "Science Fiction|Action",  # Sci-Fi + Action
            "Science Fiction|Comedy",  # Sci-Fi only
            "Crime|Drama",
            "Action|Thriller",
            "Horror"
        ],
        "cast": [
            "Bruce Willis|Emily Blunt",
            "Bruce Willis",
            "John Travolta|Uma Thurman",
            "Uma Thurman",
            "Nobody"
        ],
        "director": [
            "Rian Johnson",
            "Luc Besson",
            "Quentin Tarantino",
            "Quentin Tarantino",
            "Someone"
        ],
        "vote_average": [7.4, 7.6, 8.9, 8.1, 3.2],
        "runtime": [119, 126, 154, 111, 100]
    })


# apply_filter


def test_apply_filter_basic(movie_df):
    """Check that apply_filter correctly applies a boolean mask."""
    condition = lambda df: df["genres"].str.contains("Science Fiction")
    result = apply_filter(movie_df, condition)

    assert len(result) == 2
    assert set(result["title"]) == {"Looper", "Fifth Element"}


def test_apply_filter_empty_result(movie_df):
    condition = lambda df: df["cast"].str.contains("Nonexistent Actor")
    result = apply_filter(movie_df, condition)

    assert result.empty

# search_sci_fi

def test_search_sci_fi_returns_correct_movie(movie_df):
    """
    Sci-Fi + Action + Bruce Willis:
    Only Looper matches all three criteria.
    """
    result = search_sci_fi(movie_df)

    assert len(result) == 1
    assert result.iloc[0]["title"] == "Looper"


def test_search_sci_fi_sorting(movie_df):
    """
    Test that sorting happens by vote_average desc.
    Create two valid matches with different scores.
    """
    df = movie_df.copy()
    df.loc[1, "genres"] = "Science Fiction|Action"  # make Fifth Element valid

    result = search_sci_fi(df)

    assert len(result) == 2
    # Fifth Element = 7.6, Looper = 7.4 → Fifth Element first
    assert list(result["title"]) == ["Fifth Element", "Looper"]


def test_search_sci_fi_handles_nan(movie_df):
    df = movie_df.copy()
    df.loc[0, "genres"] = None

    result = search_sci_fi(df)

    # Looper was affected by NaN, so only other matches should remain (none)
    assert result.empty

# search_uma_by_tarantino
def test_search_uma_by_tarantino(movie_df):
    """
    Uma Thurman + Tarantino:
    Matches:
      - Pulp Fiction
      - Kill Bill
    Sorted by runtime ascending → Kill Bill first (111 < 154)
    """
    result = search_uma_by_tarantino(movie_df)

    assert len(result) == 2
    assert result.iloc[0]["title"] == "Kill Bill"
    assert result.iloc[1]["title"] == "Pulp Fiction"


def test_search_uma_by_tarantino_no_match(movie_df):
    df = movie_df.copy()
    df["cast"] = "Nobody"

    result = search_uma_by_tarantino(df)
    assert result.empty


def test_search_uma_by_tarantino_case_insensitive(movie_df):
    df = movie_df.copy()
    df.loc[2, "cast"] = "uma thurman"  # lowercase

    result = search_uma_by_tarantino(df)

    assert "Pulp Fiction" in set(result["title"])
