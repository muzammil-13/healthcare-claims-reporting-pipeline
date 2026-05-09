"""
streamlit_app.py — Live AA Rate Dashboard

Reads the latest pipeline output and shows:
1. Segment-level AA rate bar chart (interactive)
2. Summary metrics table
3. YTD trend if YTD data is available

Run with:
    streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Claims AA Rate Dashboard",
    page_icon="🏥",
    layout="wide",
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_latest_excel(output_dir="data/output") -> pd.DataFrame:
    """Find the most recently written Excel report and load it."""
    pattern = os.path.join(output_dir, "West_Market_Summary*.xlsx")
    files = sorted(glob.glob(pattern), reverse=True)
    if not files:
        return None, None
    latest = files[0]
    df = pd.read_excel(latest, sheet_name="West Market Summary")
    return df, latest


def load_ytd(output_dir="data/output") -> pd.DataFrame:
    """Load the most recent YTD Excel snapshot."""
    pattern = os.path.join(output_dir, "YTD_*.xlsx")
    files = sorted(glob.glob(pattern), reverse=True)
    if not files:
        return None
    return pd.read_excel(files[0])


# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏥 Healthcare Claims — AA Rate Dashboard")
st.caption(f"Last refreshed: {datetime.now().strftime('%B %d, %Y  %I:%M %p')}")

st.markdown("---")

# ── Load data ─────────────────────────────────────────────────────────────────
df, source_file = load_latest_excel()

if df is None:
    st.warning(
        "No report data found. Run `python main.py` first to generate output files."
    )
    st.stop()

st.caption(f"Source: `{source_file}`")

# ── KPI row ───────────────────────────────────────────────────────────────────
st.subheader("Segment Overview")

cols = st.columns(len(df))
for col, (_, row) in zip(cols, df.iterrows()):
    rate = row["AA Rate (%)"]
    delta_color = "normal" if rate >= 85 else "inverse"
    col.metric(
        label=row["Segment Name"],
        value=f"{rate:.1f}%",
        delta=f"{rate - 85:.1f}% vs target",
        delta_color=delta_color,
    )

st.markdown("---")

# ── Main chart ────────────────────────────────────────────────────────────────
st.subheader("Auto-Adjudication Rate by Segment")

# Rebuild metrics dict from Excel df so we can reuse charts.py
metrics_from_excel = {}
for _, row in df.iterrows():
    metrics_from_excel[row["Segment Code"]] = {
        "segment_name": row["Segment Name"],
        "total_claims":  row["Total Claims"],
        "auto_claims":   row["Auto Claims"],
        "manual_claims": row["Manual Claims"],
        "aa_rate":       row["AA Rate (%)"],
    }

from src.charts import generate_aa_rate_chart_figure

fig = generate_aa_rate_chart_figure(
    metrics_from_excel,
    report_date=datetime.now().strftime("%B %d, %Y"),
)
if fig:
    st.pyplot(fig)
else:
    st.error("Chart could not be generated.")

st.markdown("---")

# ── Data table ────────────────────────────────────────────────────────────────
st.subheader("Detailed Metrics Table")

display_df = df.copy()
display_df["AA Rate (%)"] = display_df["AA Rate (%)"].apply(lambda x: f"{x:.2f}%")
display_df["Total Claims"] = display_df["Total Claims"].apply(lambda x: f"{int(x):,}")
display_df["Auto Claims"]  = display_df["Auto Claims"].apply(lambda x: f"{int(x):,}")
display_df["Manual Claims"]= display_df["Manual Claims"].apply(lambda x: f"{int(x):,}")

st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ── YTD section ───────────────────────────────────────────────────────────────
st.subheader("YTD Dataset Preview")

ytd_df = load_ytd()
if ytd_df is not None:
    st.write(f"{len(ytd_df)} total records in YTD dataset")
    st.dataframe(ytd_df.head(20), use_container_width=True, hide_index=True)
else:
    st.info("No YTD file found yet.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Healthcare Claims Reporting Pipeline — Built by Muzammil Ibrahim, IBM CIC Bangalore Intern (2025–26)."
)
