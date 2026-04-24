import pandas as pd
import os
from config import PATHS

def merge_data(mbu_df, reference_df, on_column="SegmentCode"):
    """Merge MBU data with reference data."""
    return pd.merge(mbu_df, reference_df, on=on_column, how="left")

def append_to_ytd(merged_df, ytd_path=None):
    """Append new data to year-to-date dataset."""
    if ytd_path is None:
        ytd_path = PATHS["ytd_dataset"]
    
    if os.path.exists(ytd_path):
        ytd_df = pd.read_csv(ytd_path)
        ytd_df = pd.concat([ytd_df, merged_df], ignore_index=True)
    else:
        ytd_df = merged_df
    
    return ytd_df

def save_csv(df, file_path):
    """Save DataFrame to CSV."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"Saved {len(df)} records to {file_path}")
