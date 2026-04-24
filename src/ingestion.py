import pandas as pd
import os

def load_csv(file_path):
    """Load CSV file and return DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def load_text_delimited(file_path, delimiter="|"):
    """Load pipe-delimited or custom delimiter text file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path, sep=delimiter)
