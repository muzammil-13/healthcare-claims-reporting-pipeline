# Pipeline Completion Roadmap
**healthcare-claims-reporting-pipeline**
**Internship ends: ~42 days from 09 May 2026**

---

## Current State (Honest Assessment)

| Area | Status |
|---|---|
| Project structure & config | ✅ Done |
| Logging module | ✅ Done |
| Data parsing & merging | ✅ Done |
| Metrics computation | ✅ Done |
| Excel report generation | ✅ Done |
| Sample data (runnable) | ❌ Missing |
| Email output | ❌ Placeholder (`pass`) |
| End-to-end test | ❌ Not verified |
| Measurable impact stat | ❌ Vague |

**Current read:** Clean architecture. Doesn't run out of the box.  
**Target read:** Built and runs. Solves a real ops problem. Numbers to prove it.

---

## Phase 1 — Make It Run (Week 1–2, by ~23 May)

**Goal:** Anyone who clones this repo can run it in under 5 minutes.

### Task 1.1 — Add sample data
- Create `/data/sample_mbu.csv` with pipe-delimited format matching expected schema
- Create `/data/sample_reference.csv` with `SegmentCode` mapping
- Create `/data/ytd_dataset.csv` as empty seed file
- Columns needed: `SegmentCode`, `ProcessingType`, and whatever merge keys exist

```
SegmentCode|ProcessingType|ClaimDate|ClaimAmount
WGS|AUTO|2026-04-01|1500.00
WGS|MANUAL|2026-04-01|2300.00
MED|AUTO|2026-04-01|900.00
```

### Task 1.2 — Replace the `pass` in `generate_and_send_email`
- Write HTML report to `/logs/report_YYYYMMDD.html` instead of Outlook (Outlook is environment-locked)
- Template should show: segment name, total claims, AA rate as a formatted table
- Keep Outlook logic commented out with a note: *"Active in production environment with win32com"*

### Task 1.3 — Verify end-to-end run
- `python main.py` should complete without errors
- Output: Excel file in `/data/`, HTML report in `/logs/`
- Log output should show section starts, ends, and metrics

**Checkpoint:** Paste the terminal output here once it runs clean.

---

## Phase 2 — Make It Credible (Week 3–4, by ~06 Jun)

**Goal:** The README tells a real story with real numbers.

### Task 2.1 — Add the impact stat
Replace this in README:
> "Reduced manual reporting effort"

With this:
> "The daily reporting workflow (MBU extraction → Excel update → stakeholder email) previously required ~45 minutes of manual effort. This pipeline completes the same workflow in under 2 minutes."

Use your actual estimate. Even 30 mins → 3 mins is a strong number.

### Task 2.2 — Add a `run_demo.sh` or `quickstart` section
```bash
# Install dependencies
pip install -r requirements.txt

# Run with sample data
python main.py
```
Update `config.ini` to point to sample data paths by default so it just works.

### Task 2.3 — Add one real chart or output screenshot to README
- Screenshot of the generated Excel report
- Or the HTML email output rendered in browser
- This is the visual proof that it runs

---

## Phase 3 — Make It Yours (Week 5–6, by ~20 Jun)

**Goal:** You can talk about every decision in this codebase. No black boxes.

### Task 3.1 — Write a `DECISIONS.md`
Document 3–5 architectural decisions you made and why:
- Why `configparser` over hardcoded paths
- Why `pandas.merge` on `SegmentCode` (what happens if it's missing?)
- Why logging is a separate module
- Why email output falls back to HTML file

This is the document you reference in interviews. It proves you understood it, not just ran it.

### Task 3.2 — Handle one real edge case in code
Pick one and fix it:
- What if `SegmentCode` in MBU doesn't match any reference entry? (currently silent `NaN`)
- What if the YTD file is corrupt or has schema mismatch?
- What if `total_claims` is 0 for a segment? (AA rate division already guarded — good. Log it visibly.)

Adding one real edge case handler shows engineering judgment, not just feature shipping.

### Task 3.3 — Update your contribution note
Change this in README (or add a section):
> **My contribution:** Domain knowledge, system architecture, AI-assisted coding, decision making, local testing.

To something like:
> **Built by:** Muzammil Ibrahim, IBM CIC Bangalore Intern (2025–26). Designed the system architecture based on real healthcare claims ops workflow. Used AI coding tools for implementation velocity. Owned debugging, edge case handling, config design, and end-to-end validation.

Don't hide the AI usage — frame it correctly.

---

## Timeline Summary

| Week | Dates | Goal |
|---|---|---|
| Week 1–2 | 09–23 May | Sample data + email output + clean run |
| Week 3–4 | 24 May–06 Jun | Impact numbers + quickstart + screenshot |
| Week 5–6 | 07–20 Jun | DECISIONS.md + edge case + contribution framing |
| Buffer | 21 Jun onward | Polish, internship wrap-up, resume update |

---

## Resume Bullet (Target)

> Built a Python ETL pipeline automating healthcare claims AA rate reporting across 5 business segments (WGS, Medicaid, GBD, Commercial, New States). Reduced daily reporting time from ~45 mins to under 2 mins. Stack: Python, Pandas, OpenPyXL, ConfigParser.

That bullet is 42 days away. Each phase gets you closer to being able to say it with evidence.

---

## One Rule

**Don't add features. Close open loops.**  
The email function being a `pass` is more damaging to this project's credibility than any missing feature. Finish what's started before expanding scope.
