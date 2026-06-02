import pytest
import pandas as pd
from src.metrics import calculate_metrics

def test_calculate_metrics_aggregations():
    # Arrange: Create dummy DataFrame with multiple records per segment
    df = pd.DataFrame({
        "SegmentCode": ["WGS", "MED", "WGS", "UNKNOWN"],
        "TOT_CLMS": [100, 50, 200, 10],
        "TOT_AA": [80, 20, 190, 5]
    })
    
    # Act
    metrics = calculate_metrics(df)
    
    # Assert
    assert "WGS" in metrics
    assert "MED" in metrics
    assert "UNKNOWN" not in metrics  # Should be skipped as it's not in SEGMENT_CODES
    
    wgs = metrics["WGS"]
    assert wgs["total_claims"] == 300
    assert wgs["auto_claims"] == 270
    assert wgs["manual_claims"] == 30
    assert wgs["aa_rate"] == 90.0
    
def test_calculate_metrics_zero_claims():
    # Arrange: Test division by zero handling
    df = pd.DataFrame({
        "SegmentCode": ["COM"],
        "TOT_CLMS": [0],
        "TOT_AA": [0]
    })
    
    # Act
    metrics = calculate_metrics(df)
    
    # Assert
    assert metrics["COM"]["aa_rate"] == 0
