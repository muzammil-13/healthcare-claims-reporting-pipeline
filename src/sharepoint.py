"""
sharepoint.py — Simulated SharePoint upload module.

In production, this module would use the Microsoft Graph API to upload files
to a SharePoint document library and return a shareable link.

Graph API equivalent (production):
    POST https://graph.microsoft.com/v1.0/sites/{site-id}/drives/{drive-id}/items/{folder-id}:/{filename}:/content
    Headers: Authorization: Bearer {access_token}
    Body: <file bytes>

For portfolio simulation, this module:
1. Copies the file into a local `sharepoint_sim/` folder (mimics the document library)
2. Constructs a realistic SharePoint-style URL
3. Returns that URL for use in the email body

To activate real SharePoint integration, replace the body of `upload_file`
with a Graph API call using the `requests` library and an OAuth2 token.
"""

import os
import shutil
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Simulated SharePoint base URL — replace with your real tenant in production
SHAREPOINT_BASE_URL = "https://elevancehealth.sharepoint.com/sites/ClaimsOps/Shared%20Documents"
LOCAL_SIM_DIR = "sharepoint_sim"  # local folder that mimics the document library


def upload_file(file_path: str, report_date: str = None) -> str:
    """
    Simulate uploading a file to SharePoint.

    In production: replace this with a Microsoft Graph API call.
    For simulation: copies the file to sharepoint_sim/ and returns a fake URL.

    Args:
        file_path: Local path to the file to upload.
        report_date: Date string used to organize files (e.g., '20260509').
                     Defaults to today's date.

    Returns:
        A SharePoint-style URL string pointing to the uploaded file.
    """
    if report_date is None:
        report_date = datetime.today().strftime("%Y%m%d")

    file_path = Path(file_path)

    if not file_path.exists():
        logger.warning(f"  [SharePoint] File not found, skipping upload: {file_path}")
        return None

    # Organize into date-based subfolder (mirrors real SP folder structure)
    sim_subfolder = Path(LOCAL_SIM_DIR) / report_date
    sim_subfolder.mkdir(parents=True, exist_ok=True)

    destination = sim_subfolder / file_path.name
    shutil.copy(file_path, destination)

    # Construct a realistic SharePoint URL
    sp_url = f"{SHAREPOINT_BASE_URL}/{report_date}/{file_path.name}"

    logger.info(f"  [SharePoint] Simulated upload: {file_path.name}")
    logger.info(f"  [SharePoint] Accessible at: {sp_url}")
    logger.info(f"  [SharePoint] Local sim path: {destination}")

    return sp_url


def upload_multiple(file_paths: list, report_date: str = None) -> dict:
    """
    Upload multiple files and return a dict of filename -> SharePoint URL.

    Args:
        file_paths: List of local file paths to upload.
        report_date: Date string for folder organization.

    Returns:
        Dict mapping filename to its SharePoint URL.
    """
    links = {}
    for fp in file_paths:
        url = upload_file(fp, report_date)
        if url:
            links[Path(fp).name] = url
    return links
