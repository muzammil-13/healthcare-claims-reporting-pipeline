# Testing Guide

This project uses **[pytest](https://docs.pytest.org/)** as its testing framework to ensure data validation, metric calculations, and edge case handling work reliably.

## Prerequisites

Ensure you have installed the project dependencies, which includes `pytest`.
If you haven't already, run:

```bash
pip install -r requirements.txt
```

## Running the Tests

You can run the test suite from your terminal in the root directory of the project.

### 1. Run all tests
To execute all tests across the entire project automatically, simply run:
```bash
pytest
```
*Pytest will automatically discover any files starting with `test_` and execute them.*

### 2. Run tests with verbose output
If you want to see exactly which individual test functions are passing or failing, add the `-v` (verbose) flag:
```bash
pytest -v
```

### 3. Run a specific test file
If you are actively working on a specific module (e.g., validation) and only want to run tests for that module:
```bash
pytest tests/test_validation.py
```

## Test Structure

Our unit tests are organized to test individual components of the ETL pipeline:

- **`test_metrics.py`**: 
  - Verifies that `calculate_metrics()` correctly aggregates Auto and Manual claims.
  - Ensures proper handling of edge cases, such as division-by-zero when calculating the Auto-Adjudication (AA) rate for a segment with 0 claims.
  - Checks that unrecognized Segment Codes are safely ignored.
  
- **`test_validation.py`**:
  - Ensures `validate_columns()` catches missing schema dependencies.
  - Verifies that `check_duplicates()` successfully identifies and removes duplicate rows based on identical `SegmentCode` and `ClaimDate`.

- **`test_sharepoint.py`**:
  - Tests the simulated SharePoint upload mechanism using `pytest` fixtures (`monkeypatch` and `tmp_path`) to redirect I/O operations and avoid leaving residual files.
  - Verifies that requests to upload missing files are handled gracefully and logged appropriately without crashing the pipeline.
