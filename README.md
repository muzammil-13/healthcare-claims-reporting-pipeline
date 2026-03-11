# Healthcare Auto Adjudication Report Automation Toolkit

A lightweight automation toolkit for processing healthcare auto-adjudication reports generated from legacy systems and delivering clean, validated reports directly to SharePoint.

This project focuses on removing repetitive manual work from reporting workflows such as downloading reports from Outlook, cleaning them in Excel, validating fields, and uploading them to SharePoint.

The toolkit converts that process into a reliable Python pipeline.

---

## Problem

Many healthcare operations still depend on legacy systems such as mainframe batch jobs. These jobs typically generate TXT or CSV reports that are sent through email.

A common manual workflow looks like this:

Mainframe JCL job → report sent via Outlook → analyst downloads file → data cleaned in Excel → report uploaded to SharePoint → summary emailed.

This process is repetitive, error-prone, and time consuming.

---

## Solution

This toolkit automates the entire pipeline.

Reports are automatically processed using Python, cleaned and validated, then uploaded to SharePoint. A daily summary email and a simple dashboard provide visibility into report status.

The goal is simple:
turn a manual reporting workflow into a reliable automated system.

---

## Workflow Overview

Input
TXT or CSV reports generated from legacy systems (typically mainframe JCL batch jobs and delivered through Outlook).

Processing
Python data pipeline cleans and validates the data.

Output
Cleaned reports automatically uploaded to SharePoint.

Extras
Daily email summary and a lightweight dashboard to monitor report status.

---

## Architecture

```
Legacy System (Mainframe JCL)
        │
        ▼
Report Delivered via Outlook
        │
        ▼
Python Processing Pipeline
   - Data Cleaning
   - Field Validation
   - Transformation
        │
        ▼
SharePoint Upload
        │
        ├── Daily Summary Email
        └── Dashboard Monitoring
```

---

## Tech Stack
```
Python
Pandas – data cleaning and transformation
FastAPI – lightweight API layer for triggers and dashboard
Docker – containerized deployment
GitHub Actions – automated CI/CD pipeline

Optional integrations may include:

Microsoft Graph API for email and SharePoint automation.
```
---

## Project Structure

```
healthcare-report-automation/
│
├── app/
│   ├── ingestion/
│   │   ├── email_fetcher.py
│   │   └── file_parser.py
│   │
│   ├── processing/
│   │   ├── cleaner.py
│   │   ├── validator.py
│   │   └── transformer.py
│   │
│   ├── output/
│   │   ├── sharepoint_uploader.py
│   │   └── email_summary.py
│   │
│   ├── api/
│   │   └── main.py
│   │
│   └── dashboard/
│       └── metrics.py
│
├── tests/
├── docker/
│   └── Dockerfile
│
├── .github/workflows/
│   └── ci.yml
│
└── README.md
```

---

## Features

Automated ingestion of TXT or CSV reports
Data cleaning and normalization using Pandas
Validation checks for missing or inconsistent fields
Automated upload to SharePoint
Daily summary email with report status
Lightweight dashboard for monitoring processing results
Containerized deployment using Docker
CI/CD automation with GitHub Actions

---

## Example Data Processing Flow

1. Report file arrives via Outlook.
2. Pipeline fetches the file automatically.
3. Pandas cleans the dataset.
4. Validation rules check for missing values or incorrect formats.
5. Processed file is saved as a standardized CSV.
6. File is uploaded to SharePoint.
7. Daily summary email is generated.

---

## Local Development

Clone the repository

```
git clone https://github.com/yourusername/healthcare-report-automation.git
cd healthcare-report-automation
```

Create a virtual environment

```
python -m venv venv
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Run the API

```
uvicorn app.api.main:app --reload
```

---

## Running with Docker

Build the container

```
docker build -t healthcare-automation .
```

Run the container

```
docker run -p 8000:8000 healthcare-automation
```

---

## CI/CD

GitHub Actions handles:

Linting
Testing
Docker build
Deployment pipeline

---

## Future Improvements

Automated Outlook integration via Microsoft Graph API
Advanced anomaly detection in reports
Historical reporting analytics dashboard
Scheduled orchestration using Airflow or Prefect
Alerting system for failed jobs

---

## Use Case

Designed for healthcare reporting workflows involving:

Auto adjudication reports
Claims processing reports
Operational daily batch reports
Legacy system reporting pipelines

---

## License

MIT License
