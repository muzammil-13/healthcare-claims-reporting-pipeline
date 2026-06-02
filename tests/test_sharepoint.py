import pytest
from pathlib import Path
from src.sharepoint import upload_file

def test_upload_file_simulated(monkeypatch, tmp_path):
    # 1. Monkeypatch the simulation directory to use pytest's temporary directory
    monkeypatch.setattr("src.sharepoint.LOCAL_SIM_DIR", str(tmp_path / "sharepoint_sim"))
    
    # 2. Create a dummy file to "upload"
    dummy_file = tmp_path / "test_report.xlsx"
    dummy_file.write_text("dummy data")
    
    # 3. Run the upload function
    report_date = "20260509"
    url = upload_file(str(dummy_file), report_date=report_date)
    
    # 4. Assert the URL is formatted correctly
    assert "https://elevancehealth.sharepoint.com" in url
    assert f"{report_date}/test_report.xlsx" in url
    
    # 5. Assert the file was actually "uploaded" (copied) to our mock directory
    copied_file = tmp_path / "sharepoint_sim" / report_date / "test_report.xlsx"
    assert copied_file.exists()
    assert copied_file.read_text() == "dummy data"

def test_upload_file_not_found(caplog):
    # Test that a missing file is handled gracefully
    url = upload_file("non_existent_file.xlsx")
    
    assert url is None
    assert "File not found" in caplog.text
