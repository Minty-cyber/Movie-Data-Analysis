import pandas as pd
from pandas.testing import assert_frame_equal
from transform.converter import json_to_dataframe

def test_json_to_dataframe_transposed():
    data = {
        123: {"title": "Inception", "budget": 160, "revenue": 800},
        456: {"title": "Avatar", "budget": 237, "revenue": 2788},
    }

    # Expected: DataFrame with movie IDs as rows
    expected = pd.DataFrame([
        {"title": "Inception", "budget": 160, "revenue": 800},
        {"title": "Avatar",    "budget": 237, "revenue": 2788},
    ], index=[123, 456])

    result = json_to_dataframe(data)
    assert_frame_equal(result, expected, check_dtype=False)
