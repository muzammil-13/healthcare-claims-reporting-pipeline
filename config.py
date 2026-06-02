"""
config.py — Configuration loader for the Healthcare Claims Reporting Pipeline.

Credential loading order (most secure first):
    1. Environment variables  ← always preferred in production
    2. config.ini fallback    ← for local dev only, never commit with real values

Environment variables recognised:
    SMTP_SERVER    — SMTP host (e.g. smtp.gmail.com)
    SMTP_PORT      — SMTP port (e.g. 465)
    SMTP_USERNAME  — sender email address
    SMTP_PASSWORD  — sender password or app password  ← most sensitive
    SMTP_RECIPIENTS — comma-separated recipient list
    SMTP_SUBJECT   — email subject prefix

To set env vars locally (Windows PowerShell):
    $env:SMTP_PASSWORD = "your-app-password"

To set env vars locally (bash/zsh):
    export SMTP_PASSWORD="your-app-password"

For CI/CD (GitHub Actions), add these as repository secrets:
    Settings → Secrets and variables → Actions → New repository secret
"""

import os
import configparser
from dotenv import load_dotenv

# ── Load .env file (if it exists) to inject local secrets securely ────────────
load_dotenv()

# ── Load config.ini (used for non-sensitive path/app settings) ────────────────
config = configparser.ConfigParser()
ini_path = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(ini_path)

# ── Paths ─────────────────────────────────────────────────────────────────────
DEFAULT_PATHS = {
    "raw_mbu_data": "data/input/sample_mbu.csv",
    "reference_csv": "data/input/sample_reference.csv",
    "ytd_dataset": "data/processed/ytd_data.csv",
    "excel_report": "data/output/West_Market_Summary.xlsx",
    "processed_path": "data/processed/",
}

PATHS = DEFAULT_PATHS.copy()
if config.has_section("Paths"):
    PATHS.update(dict(config["Paths"]))

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_FILE = config.get("Logging", "log_file", fallback="logs/pipeline.log")

# ── SMTP / Email ──────────────────────────────────────────────────────────────
# Environment variables take priority over config.ini for all credential fields.
# This ensures passwords are never stored in version-controlled files.

_smtp_server    = os.getenv("SMTP_SERVER")    or config.get("SMTP", "server",    fallback="smtp.gmail.com")
_smtp_port      = os.getenv("SMTP_PORT")      or config.get("SMTP", "port",      fallback="465")
_smtp_username  = os.getenv("SMTP_USERNAME")  or config.get("SMTP", "username",  fallback="")
_smtp_password  = os.getenv("SMTP_PASSWORD")  or config.get("SMTP", "password",  fallback="")
_smtp_recipients= os.getenv("SMTP_RECIPIENTS")or config.get("SMTP", "recipients",fallback="")
_smtp_subject   = os.getenv("SMTP_SUBJECT")   or config.get("SMTP", "subject",   fallback="Daily Healthcare Claims Report")

# Warn loudly if password is coming from config.ini instead of env var
if not os.getenv("SMTP_PASSWORD") and _smtp_password:
    import warnings
    warnings.warn(
        "SMTP_PASSWORD is being read from config.ini. "
        "Set the SMTP_PASSWORD environment variable instead for production use.",
        stacklevel=2,
    )

EMAIL = {
    "server":     _smtp_server,
    "port":       int(_smtp_port),
    "username":   _smtp_username,
    "password":   _smtp_password,
    "recipients": [r.strip() for r in _smtp_recipients.split(",") if r.strip()],
    "subject":    _smtp_subject,
    "sender":     _smtp_username,
}

# ── Segment code mappings ─────────────────────────────────────────────────────
# Keys must match SegmentCode values in sample_mbu.csv exactly.
SEGMENT_CODES = {
    "WGS": "Whole Group Solutions",
    "MED": "Medicaid",
    "GBD": "Government Business Division",
    "COM": "Commercial",
    "NEW": "New States"
}

# ── Directory setup ───────────────────────────────────────────────────────────
def ensure_dirs():
    """Create all required directories if they don't exist."""
    required_dirs = [
        "data/input",
        "data/output",
        "data/processed",
        "logs",
        "sharepoint_sim",
    ]
    for d in required_dirs:
        os.makedirs(d, exist_ok=True)

    # Also create dirs for any configured file paths
    for file_path in PATHS.values():
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
