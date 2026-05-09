# Security & Compliance Notes

This document explains the security and compliance decisions made in this pipeline.
It is intended for reviewers, interviewers, and future maintainers.

---

## Credential Management

### Rule: Passwords never live in code or config files

All sensitive credentials are loaded via environment variables, not from `config.ini`.

| Credential       | Environment Variable | Purpose                         |
|------------------|----------------------|---------------------------------|
| SMTP password    | `SMTP_PASSWORD`      | Email sender authentication     |
| SMTP username    | `SMTP_USERNAME`      | Sender email address            |
| SMTP server      | `SMTP_SERVER`        | Mail relay host                 |
| Recipients list  | `SMTP_RECIPIENTS`    | Comma-separated email addresses |

`config.ini` is used only for non-sensitive settings (file paths, subject line).
It is excluded from version control via `.gitignore`.

### How to set credentials locally

**Windows PowerShell:**
```powershell
$env:SMTP_PASSWORD = "your-app-password"
$env:SMTP_USERNAME = "sender@example.com"
$env:SMTP_RECIPIENTS = "recipient1@example.com,recipient2@example.com"
```

**bash / zsh (Mac/Linux):**
```bash
export SMTP_PASSWORD="your-app-password"
export SMTP_USERNAME="sender@example.com"
export SMTP_RECIPIENTS="recipient1@example.com,recipient2@example.com"
```

### How to set credentials in CI/CD (GitHub Actions)

Go to: `Settings → Secrets and variables → Actions → New repository secret`

Add each variable listed above as a repository secret. Reference them in your
workflow YAML as `${{ secrets.SMTP_PASSWORD }}`.

### Why the pipeline warns if credentials fall back to config.ini

`config.py` emits a `warnings.warn()` if `SMTP_PASSWORD` is read from
`config.ini` rather than an environment variable. This surfaces the risk
visibly during development so it is never silently deployed to production.

---

## PHI / PII Handling

This project simulates a healthcare claims reporting workflow. In production,
the data processed by this pipeline would be subject to **HIPAA** (Health
Insurance Portability and Accountability Act).

### Design decisions made with PHI in mind

**1. No PHI in logs**
The logging layer records only record counts, segment codes, file paths,
and pipeline events. It never logs DataFrame contents, individual claim
records, or member identifiers. This is enforced by convention — all
`logger.*` calls reference aggregated values only.

**2. No PHI in Git**
Sample data uses synthetic, non-identifiable values. Real input files
(`data/input/`, `data/processed/`, `data/output/`) are excluded from
version control via `.gitignore`.

**3. No PHI in email bodies**
The email report contains only segment-level aggregated metrics
(total claims, AA rate). No individual claim or member data is included.

**4. SharePoint simulation keeps files local**
The `sharepoint_sim/` folder is gitignored. In production, files would
be uploaded to an access-controlled SharePoint library — not emailed
as attachments — reducing PHI exposure in inboxes.

---

## Audit Logging

Every pipeline run emits a structured log entry capturing:
- Run timestamp
- Report date
- Records processed
- Segments included
- Email recipients

Log files are written to `logs/pipeline.log`. In production, these logs
should be retained and access-controlled as part of the audit trail
required for healthcare data operations.

---

## Known Limitations (Non-Production Gaps)

These are intentional simplifications acceptable for a portfolio simulation.
Each would require a production-grade solution before handling real PHI.

| Gap | Production Solution |
|-----|---------------------|
| SMTP credentials in env vars | Azure Key Vault / AWS Secrets Manager |
| Local SharePoint simulation | Microsoft Graph API with OAuth2 |
| No data encryption at rest | Encrypt CSVs and Excel files at rest |
| No access control on output files | Role-based access via SharePoint permissions |
| No data retention policy | Automated purge of files older than retention window |
| SQLite for local dev | PostgreSQL with encrypted connections in production |

---

## Responsible AI / Automation Note

This pipeline was built with AI coding assistance (Claude, Anthropic).
All architectural decisions, domain logic, edge case handling, and
security design were reviewed and owned by the developer.
AI was used as an implementation accelerator, not a replacement for
engineering judgment.

---

*Last updated: May 2026 — Muzammil Ibrahim, IBM CIC Bangalore Intern*
