import pytest
import pandas as pd
from src.validation import validate_columns, check_duplicates, validate

def test_validate_columns_success():
    # Arrange & Act
    df = pd.DataFrame({"SegmentCode": ["COM"], "TOT_CLMS": [10], "TOT_AA": [5]})
    
    # Assert
    assert validate_columns(df) is True

def test_validate_columns_missing():
    # Arrange
    df = pd.DataFrame({"SegmentCode": ["COM"], "TOT_CLMS": [10]})
    
    # Act & Assert
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_columns(df)

def test_check_duplicates_with_date():
    # Arrange: 3 records total, 2 are duplicates based on SegmentCode and ClaimDate
    df = pd.DataFrame({
        "SegmentCode": ["WGS", "WGS", "MED"],
        "ClaimDate": ["2026-05-01", "2026-05-01", "2026-05-01"],
        "TOT_CLMS": [100, 100, 50]
    })
    
    # Act
    result = check_duplicates(df)
    
    # Assert
    assert len(result) == 2

def test_validate_pipeline():
    # Arrange: Valid DataFrame with one duplicate
    df = pd.DataFrame({
        "SegmentCode": ["COM", "COM"],
        "ClaimDate": ["2026-05-08", "2026-05-08"],
        "TOT_CLMS": [10, 10],
        "TOT_AA": [5, 5]
    })
    
    # Act
    result = validate(df)
    
    # Assert
    assert len(result) == 1
