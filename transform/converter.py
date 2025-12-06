import pandas as pd
from typing import Dict
# from .api import fetch_movies



# A function to convert the extracted movies(In JSON format) to Dataframes
def json_to_dataframe(data: Dict[int, dict]) -> pd.DataFrame:
    return pd.DataFrame.from_dict(data)



## testing the script
# if __name__ == " __main__":
#     movie_ids =  [
#         0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428,
#         168259, 99861, 284054, 12445, 181808, 330457, 
#         351286, 109445, 321612, 260513
#     ]
#     movies =fetch_movies(movie_ids)
#     df = json_to_dataframe(movies)
#     print(df)
