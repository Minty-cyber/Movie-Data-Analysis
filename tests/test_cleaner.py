import pandas as pd
import pytest
from transform.cleaner import MovieDataCleaner

def test_drop_irrelevant():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    cleaner = MovieDataCleaner(df).drop_irrelevant(["b", "z"])

    assert "b" not in cleaner.df.columns
    assert "a" in cleaner.df.columns
    assert "c" in cleaner.df.columns


def test_extract_single_json_column():
    df = pd.DataFrame({
        "info": ['{"name": "John", "age": 30}', '{"name": "Jane"}']
    })

    cleaner = MovieDataCleaner(df).extract_single_json_column("info", "name")

    assert cleaner.df["info"].tolist() == ["John", "Jane"]


def test_pipe_names():
    df = pd.DataFrame({
        "genres": [
            [{"name": "Action"}, {"name": "Drama"}],
            [{"name": "Comedy"}]
        ],
        "cast": [
            ["John", "Mary"],
            ["Bruce"]
        ]
    })

    cleaner = MovieDataCleaner(df).pipe_names(["genres", "cast"])

    assert cleaner.df["genres"].tolist() == ["Action|Drama", "Comedy"]
    assert cleaner.df["cast"].tolist() == ["John|Mary", "Bruce"]


def test_convert_dtypes():
    df = pd.DataFrame({
        "budget": ["1000", "2000", "x"],
        "release_date": ["2020-01-01", "bad date", None],
    })

    cleaner = MovieDataCleaner(df).convert_dtypes(
        numeric_cols=["budget"],
        date_cols=["release_date"]
    )

    assert pd.isna(cleaner.df["budget"].iloc[2])
    assert pd.isna(cleaner.df["release_date"].iloc[1])


def test_replace_zero_with_nan():
    df = pd.DataFrame({"a": [0, 2], "b": [3, 0]})
    cleaner = MovieDataCleaner(df).replace_zero_with_nan(["a", "b"])

    assert pd.isna(cleaner.df["a"].iloc[0])
    assert pd.isna(cleaner.df["b"].iloc[1])


def test_convert_to_millions():
    df = pd.DataFrame({"budget": [2_000_000], "revenue": [10_500_000]})

    cleaner = MovieDataCleaner(df).convert_to_millions(["budget", "revenue"])

    assert cleaner.df.columns.tolist() == ["budget_musd", "revenue_musd"]
    assert cleaner.df["budget_musd"].iloc[0] == 2.0
    assert cleaner.df["revenue_musd"].iloc[0] == 10.5


def test_fix_vote_count():
    df = pd.DataFrame({"vote_count": [0, 5]})
    cleaner = MovieDataCleaner(df).fix_vote_count()

    assert pd.isna(cleaner.df["vote_count"].iloc[0])
    assert cleaner.df["vote_count"].iloc[1] == 5


def test_clean_text_placeholders():
    df = pd.DataFrame({"title": ["No Data", "Good Movie", ""]})

    cleaner = MovieDataCleaner(df).clean_text_placeholders(["title"])

    assert pd.isna(cleaner.df["title"].iloc[0])
    assert pd.isna(cleaner.df["title"].iloc[2])


def test_remove_invalid_and_duplicated():
    df = pd.DataFrame({
        "id": [1, 2, 2, None],
        "title": ["A", "B", "B", None]
    })

    cleaner = MovieDataCleaner(df).remove_invalid_and_duplicated()

    assert len(cleaner.df) == 2
    assert set(cleaner.df["id"]) == {1, 2}


def test_keep_min_non_null():
    df = pd.DataFrame({
        "a": [1, 5, 3],
        "b": [2, None, None],
        "c": [3, 4, None]
    })

    cleaner = MovieDataCleaner(df).keep_min_non_null(min_non_null=2)

    # only rows 0 and 1 have >= 2 non-null entries
    assert len(cleaner.df) == 2


def test_filter_and_drop():
    df = pd.DataFrame({
        "status": ["Released", "Rumored"],
        "name": ["Movie A", "Movie B"]
    })

    cleaner = MovieDataCleaner(df).filter_and_drop()

    assert len(cleaner.df) == 1
    assert "status" not in cleaner.df.columns


def test_select_final_columns():
    df = pd.DataFrame({
        "a": [1],
        "b": [2],
        "c": [3]
    })

    cleaner = MovieDataCleaner(df).select_final_columns(["a", "c", "x"])

    assert cleaner.df.columns.tolist() == ["a", "c"]


def test_reset_index():
    df = pd.DataFrame({"a": [1, 2, 3]}).drop([1])
    cleaner = MovieDataCleaner(df).reset_index()

    assert cleaner.df.index.tolist() == [0, 1]
