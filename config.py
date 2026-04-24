import os

EXECUTION_MODE = "MTD"

PATHS = {
    "raw_mbu_data": "data/input/mbu_report.txt",
    "reference_csv": "data/input/reference_data.csv",
    "ytd_dataset": "data/processed/ytd_data.csv",
    "excel_report": "data/output/West_Market_Summary.xlsx",
}

SEGMENTS = {
    "WGS": "WGS",
    "MED": "Medicaid",
    "GBD": "GBD",
    "COM": "Commercial",
    "NEW": "New States",
}

SEGMENT_CODES = ["WGS", "MED", "GBD", "COM", "NEW"]

REQUIRED_COLUMNS = ["SegmentCode", "ProcessingType"]

EMAIL = {
    "sender": "mxml@telegmail.com",
    "recipients": ["mxml@telegmail.com", "manager@domain.com"],
    "subject": "Daily Healthcare Claims Auto-Adjudication Report",
}

LOG_FILE = "logs/pipeline.log"

def ensure_dirs():
    """Create required directories if they don't exist."""
    for path in [PATHS["ytd_dataset"], PATHS["excel_report"]]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
