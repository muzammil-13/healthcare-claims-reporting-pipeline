# **Healthcare Claims Auto-Adjudication Reporting Pipeline**

---

## 🚀 Overview

Built an automated reporting pipeline to process healthcare claims data and generate daily/month-to-date (MTD) performance reports across multiple business segments including WGS, Medicaid, GBD, Commercial, and New States.

The system ingests raw operational data, computes key metrics (Auto Adjudication Rate, total claims, manual processing, etc.), updates reporting workbooks, and delivers formatted HTML reports via email.

---

## ⚙️ Key Features

* Automated ETL pipeline (Text, CSV, Excel data sources)
* Multi-segment reporting (WGS, Medicaid, GBD, Commercial)
* Metric computation:

  * Total Claims
  * Auto Adjudication (AA)
  * Manual Claims
  * First Pass / Second Pass
  * AA Rate (%)
* Excel report generation (West Market summary)
* HTML email report generation
* Outlook-based automated email delivery
* Config-driven file paths and environment setup
* Logging and error handling for production stability

---

## 🧠 System Architecture

```
Raw MBU Files + CSV + Excel
            ↓
     Data Parsing Layer
            ↓
     Data Merge Layer
            ↓
   Metrics Computation Engine
            ↓
   ┌───────────────┬───────────────┐
   ↓                               ↓
Excel Report Update        HTML Email Generator
   ↓                               ↓
        Outlook Email Sender
```

---

## 🔄 Workflow

1. Load configuration and determine execution mode (MTD)
2. Parse MBU text report files
3. Merge with reference CSV data
4. Append data to Year-To-Date dataset
5. Compute metrics for:

   * WGS
   * Medicaid
   * GBD
   * Commercial
   * New States
6. Update Excel reporting workbook
7. Generate HTML email with formatted tables
8. Send report via Outlook with attachments

---

## 🛠 Tech Stack

* Python
* Pandas
* OpenPyXL
* ConfigParser
* Win32com (Outlook Automation)
* Excel-based reporting

---

## ⚠️ Challenges & Improvements

### Challenges

* Monolithic script (>1500 lines)
* Hardcoded paths and email lists
* Lack of logging and error handling
* Repeated logic across segments

### Improvements Implemented

* Added structured logging
* Introduced error handling for file operations and email sending
* Externalized configuration using `.ini` files
* Refactored repeated logic into reusable functions
* Improved code readability and modularity

---

## 📈 Impact

* Reduced manual reporting effort
* Improved reporting accuracy and consistency
* Enabled reliable daily operational insights
* Increased maintainability of legacy reporting system

---

## 🔐 Note

All data used in this repository is anonymized or sample data. No real client or sensitive data is included.
