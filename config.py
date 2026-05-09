import os
import configparser

# Initialize ConfigParser and read the INI file
config = configparser.ConfigParser()

# Safely locate and read config.ini in the current directory
ini_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(ini_path)

# Extract configurations into structures expected by main.py
PATHS = dict(config["Paths"])

# Extract logging configuration
LOG_FILE = config.get("Logging", "log_file", fallback="logs/pipeline.log")

# Format EMAIL config to match what src/report.py expects
EMAIL = dict(config["SMTP"])
if "recipients" in EMAIL:
    # If recipients are defined in config.ini, split them into a list
    EMAIL["recipients"] = [r.strip() for r in EMAIL["recipients"].split(",")]
else:
    # Default to sending the email to the authenticated user
    EMAIL["recipients"] = [EMAIL.get("username", "")]

# Define business segment mapping codes expected by src/metrics.py
SEGMENT_CODES = {
    "MCR": "Medicare",
    "MCD": "Medicaid",
    "COM": "Commercial",
    "WGS": "WGS Market",
    "GBD": "GBD Market"
}

def ensure_dirs():
    """Ensure that the directories for all configured paths exist."""
    for file_path in PATHS.values():
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
            
    if config.has_section("Logging") and "log_file" in config["Logging"]:
        log_dir = os.path.dirname(config["Logging"]["log_file"])
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
