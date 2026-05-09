# CLAUDE.md

## Project Name

Healthcare Claims Reporting Pipeline

---

# Project Vision

This repository simulates and automates real-world healthcare claims reporting workflows inspired by enterprise production support operations in IBM Consulting for a US healthcare client.

The project focuses on transforming manual reporting operations into a scalable, modular, automation-first pipeline using Python and lightweight data engineering practices.

This is NOT a tutorial/demo repository.

The goal is to build:

- a realistic enterprise-style automation system
- a portfolio-quality engineering project
- a reporting/data operations platform
- an AI-assisted engineering showcase

---

# Real-World Workflow Context

The original workflow includes:

1. Monitoring mainframe batch jobs
2. Exporting report datasets
3. Cleaning and transforming files
4. Calculating MTD/YTD metrics
5. Updating Excel reports
6. Generating CSV outputs
7. Preparing reporting summaries
8. Uploading deliverables to SharePoint
9. Supporting daily/monthly operational reporting

This project abstracts and modernizes those workflows.

---

# Core Objectives

## Primary Goals

- Automate repetitive reporting tasks
- Reduce manual intervention
- Simulate enterprise production workflows
- Build modular reporting pipelines
- Create recruiter-friendly portfolio evidence
- Demonstrate automation + analytics capabilities
- Learn practical software engineering through execution

---

# Engineering Philosophy

This repository should prioritize:

- clarity over cleverness
- maintainability over shortcuts
- modularity over monolithic scripts
- execution over perfection
- practical enterprise patterns over academic complexity

Code should feel:

- realistic
- production-inspired
- easy to extend
- beginner-friendly
- operationally useful

---

# Preferred Stack

## Backend

- Python 3.11+
- FastAPI
- Pandas
- SQLAlchemy

## Database

- SQLite (local development)
- PostgreSQL (future scalability)

## Frontend / UI

- Streamlit
- Lightweight dashboards

## DevOps / Infra

- Docker
- Docker Compose
- GitHub Actions
- Environment variables
- Logging + monitoring

---

# Recommended Architecture

## High-Level Flow

```text
Raw Data
   ↓
Ingestion Layer
   ↓
Transformation Layer
   ↓
Validation Layer
   ↓
Metrics Engine
   ↓
Report Generation
   ↓
Dashboard/API Layer
   ↓
Exports / Notifications
```
