import pandas as pd

def validate_columns(df, required_cols=None):
    """Check if DataFrame has required columns."""
    if required_cols is None:
        required_cols = ["SegmentCode"]
    
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True

def check_nulls(df, critical_cols=None):
    """Warn about null values in critical columns."""
    if critical_cols is None:
        critical_cols = ["SegmentCode"]
    
    available_cols = [col for col in critical_cols if col in df.columns]
    if available_cols:
        nulls = df[available_cols].isnull().sum()
        if nulls.sum() > 0:
            print(f"Warning: Found nulls in columns:\n{nulls[nulls > 0]}")
    return df

def check_duplicates(df, subset=None):
    """Remove duplicate rows."""
    if subset is None:
        subset = ["SegmentCode"] if "SegmentCode" in df.columns else None
    
    before = len(df)
    if subset:
        df = df.drop_duplicates(subset=subset)
    after = len(df)
    
    if before > after:
        print(f"Removed {before - after} duplicate rows")
    
    return df

def validate(df):
    """Run all validation checks."""
    validate_columns(df)
    check_nulls(df)
    df = check_duplicates(df)
    return df
