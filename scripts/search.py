import pandas as pd
from typing import Callable



def apply_filter(df: pd.DataFrame, condition: Callable[[pd.DataFrame], pd.Series]) -> pd.DataFrame:
    """
    A user-defined function to filter a DataFrame.
    It takes the parameters df (the movie dataset)
    and the condition (as a callable -  a fucntion that takes the df as the parameter and returns a boolean)
    Then everything returns a dataframe with the filters applied to it already
    """
    return df[condition(df)]



def search_sci_fi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the top Sci-Fi actions amovies starring Brusce Willis sorted from the highest rating to the lowest rating
    """
    def condition(df):
        # Performing the filtering condition logic
        return (
            df["genres"].str.contains("Science Fiction", case=False, na=False)
            & df["genres"].str.contains("Action", case=False, na=False)
            & df["cast"].str.contains("Bruce Willis", case=False, na=False)
        )

    filtered = apply_filter(df, condition)
    return filtered.sort_values(by="vote_average", ascending=False)

def search_uma_by_tarantino(df: pd.DataFrame) -> pd.DataFrame:
    """
    Search for Movies starring Uma Thurman and directed by Quentin Tarantino
    sorted by runtime(shortest to the longest runtime)
    """

    def condition(df):
        return (
            df["cast"].str.contains("Uma Thurman", case=False, na=False)
            & df["director"].str.contains("Quentin Tarantino", case=False, na=False)
        )

    filtered = apply_filter(df, condition)
    return filtered.sort_values(by="runtime", ascending=True)