import pandas as pd
from typing import Dict

# A function to convert the extracted movies(In JSON format) to Dataframes
def json_to_dataframe(data: Dict[int, dict]) -> pd.DataFrame:
    return pd.DataFrame(data).T
