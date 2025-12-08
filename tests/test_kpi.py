import pytest
import pandas as pd
from scripts.kpi import (
    rank_movies,
    highest_revenue,
    highest_budget,
    highest_profit,
    lowest_profit,
    highest_roi,
    lowest_roi,
    most_voted,
    highest_rated,
    lowest_rated,
    most_popular,
    franchise_vs_standalone,
    most_successful_franchises,
    most_successful_directors
)

# Fixtures

@pytest.fixture
def movie_df():
    """
    Datasets fixture to create reusable datasets for the test suite .
    """
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "title": ["A", "B", "C", "D", "E"],
        "revenue_musd": [300, 100, 500, 50, 200],
        "budget_musd": [100, 20, 200, 5, 50],
        "vote_average": [7.5, 8.0, 6.0, 5.0, 9.0],
        "vote_count": [200, 5000, 50, 100, 1200],
        "popularity": [10, 80, 5, 2, 60],
        "belongs_to_collection": ["Franchise X", None, "Franchise X", None, "Franchise Y"],
        "director": ["Dir1", "Dir1", "Dir2", None, "Dir2"],
    })


# rank_movies
def test_rank_movies_valid(movie_df):
    result = rank_movies(movie_df, metric="revenue_musd", ascending=False, top_n=2)
    assert list(result["title"]) == ["C", "A"]  # 500, 300


def test_rank_movies_invalid_column(movie_df):
    with pytest.raises(ValueError):
        rank_movies(movie_df, metric="invalid_column")


# Simple KPI Sorters
def test_highest_revenue(movie_df):
    result = highest_revenue(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "C"  # highest revenue = 500


def test_highest_budget(movie_df):
    result = highest_budget(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "C"  # highest budget = 200


def test_highest_profit(movie_df):
    # Profit: [200, 80, 300, 45, 150] → highest = movie C (300)
    result = highest_profit(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "C"


def test_lowest_profit(movie_df):
    # Same profits: lowest = D (45)
    result = lowest_profit(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "D"

# ROI KPI tests
def test_highest_roi(movie_df):
    # Remove D (budget < 10) — ROI:
    # A: 3.0, B: 5.0, C: 2.5, E: 4.0 → B wins
    result = highest_roi(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "B"


def test_lowest_roi(movie_df):
    # Lowest ROI among valid budgets → C (2.5)
    result = lowest_roi(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "C"


# Rating / popularity
def test_most_voted(movie_df):
    result = most_voted(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "B"  # 5000 votes


def test_highest_rated(movie_df):
    # Filter vote_count >= 10 → all except C (vote_count=50 *is included*)
    result = highest_rated(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "E"  # rating = 9.0


def test_lowest_rated(movie_df):
    result = lowest_rated(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "D"  # rating = 5.0


def test_most_popular(movie_df):
    result = most_popular(movie_df, top_n=1)
    assert result.iloc[0]["title"] == "B"  # popularity = 80

# Franchise vs Standalone
def test_franchise_vs_standalone(movie_df):
    result = franchise_vs_standalone(movie_df)

    # Should have exactly two rows: Franchise, Standalone
    assert list(result.index) == ["Standalone", "Franchise"]

    # Franchise mean revenue should be average of A, C, E
    franchise_mean_rev = (300 + 500 + 200) / 3
    assert result.loc["Franchise", "mean_revenue"] == pytest.approx(franchise_mean_rev)


# Franchise Rankings
def test_most_successful_franchises(movie_df):
    result = most_successful_franchises(movie_df)
    assert list(result.index) == ["Franchise X", "Franchise Y"]


# Director Rankings
def test_most_successful_directors(movie_df):
    result = most_successful_directors(movie_df)
    assert result.index[0] == "Dir2"
