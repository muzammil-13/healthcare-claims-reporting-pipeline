# Architectural Decisions

This document outlines the key technical and architectural decisions made during the development of the Healthcare Claims Reporting Pipeline.

## 1. Configuration Management (`configparser` vs Hardcoding)
**Decision:** Used Python's built-in `configparser` and a `config.ini` file to manage paths, email credentials, and segment codes, exposed through a `config.py` module.
**Why:** Hardcoding paths and parameters inside operational scripts makes them brittle and environment-locked. By extracting these into an `.ini` file, the pipeline becomes environment-agnostic. A stakeholder or DevOps engineer can redirect input/output directories or update SMTP credentials without ever touching the source code.

## 2. Email Delivery Mechanism (SMTP vs Outlook/win32com)
**Decision:** Implemented email delivery using the standard `smtplib` library with HTML payloads, rather than relying on Windows COM automation (`win32com.client`).
**Why:** While enterprise environments often use Outlook, binding the pipeline to `win32com` locks the execution to Windows machines with an active, logged-in Outlook desktop session. SMTP is cross-platform, headless, and standard for automated service accounts (e.g., CI/CD pipelines, Airflow). We kept the `win32com` logic commented out to demonstrate awareness of corporate Windows environments.

## 3. Data Merging Strategy (`pandas.merge`)
**Decision:** Used relational merging on `SegmentCode` to enrich raw Market Business Unit (MBU) extracts with Reference Data.
**Why:** Real-world claims data is highly normalized; raw mainframe extracts rarely contain human-readable segment names or regional mappings. Enforcing a relational join ensures that if a new segment is added to the claims extract, it must be mapped in the reference table. *Note: We enforce the existence of `SegmentCode` in the ingestion phase via `src/validation.py` to prevent silent `NaN` failures during the merge.*

## 4. Centralized Logging vs Print Statements
**Decision:** Replaced standard `print()` statements with Python's built-in `logging` module, configured with both `StreamHandler` (console) and `FileHandler` (disk).
**Why:** For a production ETL pipeline, ephemeral console output is insufficient. When automated jobs fail at 2:00 AM, operations teams need a persistent audit trail. The current configuration automatically timestamps every step and logs it to `logs/pipeline.log`, making debugging and compliance reporting straightforward.

## 5. Metrics Calculation (Aggregated Volumes vs Row Counts)
**Decision:** Calculated the Auto-Adjudication (AA) rate by summing `TOT_CLMS` and `TOT_AA` columns rather than counting DataFrame rows.
**Why:** This represents a crucial domain-driven design choice. In healthcare operations, daily extracts often represent aggregated batches of claims rather than single claim rows. Calculating metrics based on row counts would result in fundamentally inaccurate reporting. Utilizing `.sum()` accurately reflects operational volume.

## 6. Preserving Upstream Data Typos (e.g., "COMMERICAL")
**Decision:** Retained legacy typos (such as "COMMERICAL" instead of "COMMERCIAL" in source extracts) exactly as they appear in the production mainframe outputs.
**Why:** A core tenet of ETL pipelines is traceability. Silently "fixing" typos in Python code creates a discrepancy between the source extract and the pipeline's logic. If the upstream system generates a typo, the pipeline should pass it through transparently or map it explicitly via reference data. This ensures that any audit of the pipeline matches the source system byte-for-byte.