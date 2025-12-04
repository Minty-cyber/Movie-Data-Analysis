from typing import Optional
import pandas as pd


def rank_movies(
    df: pd.DataFrame,
    metric: str,
    ascending: bool = False,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    User-Defined ranking function for KPI operations.
    Sorts the DataFrame by `metric` and returns the top_n rows.
    """
    if metric not in df.columns:
        raise ValueError(f"Column '{metric}' does not exist in the DataFrame.")

    return df.sort_values(metric, ascending=ascending).head(top_n)

def highest_revenue(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return rank_movies(df, metric="revenue_musd", ascending=False, top_n=top_n)


def highest_budget(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return rank_movies(df, metric="budget_musd", ascending=False, top_n=top_n)


def highest_profit(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    temp = df.copy()
    temp["profit"] = temp["revenue_musd"] - temp["budget_musd"]
    return rank_movies(temp, metric="profit", ascending=False, top_n=top_n)

def lowest_profit(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    temp = df.copy()
    temp["profit"] = temp["revenue_musd"] - temp["budget_musd"]
    return rank_movies(temp, metric="profit", ascending=True, top_n=top_n)

def highest_roi(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    temp = df[df["budget_musd"] >= 10].copy()
    temp["roi"] = temp["revenue_musd"] / temp["budget_musd"]
    return rank_movies(temp, metric="roi", ascending=False, top_n=top_n)

def lowest_roi(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    temp = df[df["budget_musd"] >= 10].copy()
    temp["roi"] = temp["revenue_musd"] / temp["budget_musd"]
    return rank_movies(temp, metric="roi", ascending=True, top_n=top_n)

def most_voted(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return rank_movies(df, metric="vote_count", ascending=False, top_n=top_n)

def highest_rated(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    temp = df[df["vote_count"] >= 10]
    return rank_movies(temp, metric="vote_average", ascending=False, top_n=top_n)

def lowest_rated(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    temp = df[df["vote_count"] >= 10]
    return rank_movies(temp, metric="vote_average", ascending=True, top_n=top_n)

def most_popular(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return rank_movies(df, metric="popularity", ascending=False, top_n=top_n)


def franchise_vs_standalone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compares franchise movies vs standalone movies using:
    - Mean Revenue
    - Median ROI
    - Mean Budget
    - Mean Popularity
    - Mean Rating
    """
    temp = df.copy()
    temp["is_franchise"] = temp["belongs_to_collection"].notna()

    temp["roi"] = temp["revenue_musd"] / temp["budget_musd"]

    results = temp.groupby("is_franchise").agg(
        mean_revenue=("revenue_musd", "mean"),
        median_roi=("roi", "median"),
        mean_budget=("budget_musd", "mean"),
        mean_popularity=("popularity", "mean"),
        mean_rating=("vote_average", "mean")
    )

    results.index = ["Standalone", "Franchise"]
    return results

def most_successful_franchises(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank franchises based on:
    - total number of movies
    - total & mean budget
    - total & mean revenue
    - mean rating
    """
    temp = df.dropna(subset=["belongs_to_collection"]).copy()

    ranking = temp.groupby("belongs_to_collection").agg(
        movie_count=("id", "count"),
        total_budget=("budget_musd", "sum"),
        mean_budget=("budget_musd", "mean"),
        total_revenue=("revenue_musd", "sum"),
        mean_revenue=("revenue_musd", "mean"),
        mean_rating=("vote_average", "mean")
    )

    return ranking.sort_values(by="total_revenue", ascending=False)

def most_successful_directors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ranks directors based on:
    - Number of movies directed
    - Total revenue generated
    - Mean rating
    """
    temp = df.dropna(subset=["director"]).copy()

    ranking = temp.groupby("director").agg(
        movie_count=("id", "count"),
        total_revenue=("revenue_musd", "sum"),
        mean_rating=("vote_average", "mean")
    )

    return ranking.sort_values(by="total_revenue", ascending=False)
