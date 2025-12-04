import pandas as pd
import ast
from typing import Optional, List, Self

# A class for handing the data cleaning and processing
class MovieDataCleaner():
    # Make a copy of the data to keep the original one.
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    def drop_irrelevant(self, columns: List[str]) -> pd.DataFrame:
        """
        Drops irrelevant columns from the working copy of the dataframe.
        Returns the new dataframe with the dropped columns.
        """
        existing_cols = [col for col in columns if col in self.df.columns]
        self.df = self.df.drop(columns=existing_cols)

        return self
    
    def extract_single_json_column(self, column:str, key: str) -> pd.DataFrame:
        """
            Replace the column with the extracted value of a key from a single dictionary column.
        """
        def extract_value(cell):
            if pd.isna(cell):
                return None
            try:
                decoded = ast.literal_eval(cell) if isinstance(cell, str) else cell

                if isinstance(decoded, dict):
                    return decoded.get(key)

            except Exception:
                return None
            
            return None
        
        self.df[column] = self.df[column].apply(extract_value)
        
        return self
    
    def pipe_names(self, columns: List[str]) -> pd.DataFrame:
        """
        Extracts the 'name' field from a list of dictionaries
        and joins them with '|' into a string.
        """
        for column in columns:
            if column in self.df.columns:
                def transform(x):
                    if isinstance(x, list):
                        if all(isinstance(item, dict) for item in x):
                            return "|".join(item.get("name", "") for item in x)
                        if all(isinstance(item, str) for item in x):
                            return "|".join(x)
                    return None
                
                self.df[column] = self.df[column].apply(transform)
        return self
    
    def convert_dtypes(
        self,
        numeric_cols: list = None,
        date_cols: list = None
    ) -> pd.DataFrame:
        
        """
        Converts the columns with numeric values to Numeric and ones with Date to DateTime,
        The `errors="coerce"` makes sure that invalid fields are replaced with safe NaNs
        """
        if numeric_cols:
            for col in numeric_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
        
        if date_cols:
            for col in date_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
        
        return self
    
    def replace_zero_with_nan(self, columns: List[str]) -> pd.DataFrame:
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].replace(0, pd.NA)
        return self
    
    def convert_to_millions(self, columns: List[str]) -> pd.DataFrame:
        for col in columns:
            if col in self.df.columns:
                self.df[col] = (self.df[col] / 1_000_000).round(2)
                self.df.rename(columns = {col: f"{col}_musd"}, inplace=True)
        return self
    
    def fix_vote_count(self) -> pd.DataFrame:
        if "vote_count" in self.df.columns:
            self.df["vote_count"] = self.df["vote_count"].replace(0, pd.NA)
        return self
    
    def clean_text_placeholders(self, columns: List[str]) -> pd.DataFrame:
        placeholders = ["", " ", "No Data", "N/A", "None", "null"]

        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].replace(placeholders, pd.NA)
        return self
    
    def remove_invalid_and_duplicated(self) -> pd.DataFrame:
        '''
        Function for removing inlvais and duplicates in title and id columns
        '''
        
        # Drop rows with missing ids or invalid titles
        if "id" in self.df.columns:
            self.df = self.df[self.df["id"].notna()]
        if "title" in self.df.columns:
            self.df = self.df[self.df["title"].notna()]
            
        # Remove ids with duplicates
        
        if "id" in self.df.columns:
            self.df = self.df.drop_duplicates(subset=["id"], keep="first")

        
        return self
    
    def keep_min_non_null(self, min_non_null: int = 10) -> pd.DataFrame:
        """
        Keeps only rows that have at least `min_non_null` non-NaN values.
        Drops rows that do not meet the threshold.
        """
        # Count non-null values per row
        non_null_counts = self.df.notna().sum(axis=1)

        # Filter rows
        self.df = self.df[non_null_counts >= min_non_null]

        return self
    
    def filter_and_drop(self) -> pd.DataFrame:
        if "status" in self.df.columns:
            self.df = self.df[self.df["status"] == "Released"]
            self.df = self.df.drop(columns = ['status'])
        return self
    
    def select_final_columns(self, columns: list) -> pd.DataFrame:
        """
        Selects only the specified final set of columns.
        Skips columns that are missing to avoid KeyErrors.
        """
        existing_cols = [col for col in columns if col in self.df.columns]
        self.df = self.df[existing_cols]
        return self
    
    def reset_index(self) -> pd.DataFrame:
        self.df = self.df.reset_index(drop=True)
        return self

            
    
    
