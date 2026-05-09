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
from src.ingestion import load_csv, load_text_delimited
from src.metrics import calculate_metrics
from src.processing import merge_data

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Claims AA Rate Dashboard",
    page_icon="🏥",
    layout="wide",
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_latest_excel(output_dir="data/output") -> pd.DataFrame:
    """Find the most recently written Excel report and load it."""
    patterns = [
        os.path.join(output_dir, "West_Market_Summary*.xlsx"),
        os.path.join(output_dir, "west_market_summary*.xlsx"),
    ]
    files = sorted(
        {file_path for pattern in patterns for file_path in glob.glob(pattern)},
        reverse=True,
    )
    if not files:
        return None, None
    latest = files[0]
    try:
        df = pd.read_excel(latest, sheet_name="West Market Summary")
        return df, latest
    except Exception as exc:
        st.warning(f"Generated report could not be loaded, using sample data instead: {exc}")
        return None, None


def load_ytd(output_dir="data/output") -> pd.DataFrame:
    """Load the most recent YTD Excel snapshot."""
    pattern = os.path.join(output_dir, "YTD_*.xlsx")
    files = sorted(glob.glob(pattern), reverse=True)
    if not files:
        return None
    try:
        return pd.read_excel(files[0])
    except Exception:
        return None


def metrics_to_dataframe(metrics: dict) -> pd.DataFrame:
    """Convert calculated metrics into the same shape as the Excel report."""
    rows = []
    for segment_code, data in metrics.items():
        rows.append(
            {
                "Segment Code": segment_code,
                "Segment Name": data["segment_name"],
                "Total Claims": data["total_claims"],
                "Auto Claims": data["auto_claims"],
                "Manual Claims": data["manual_claims"],
                "AA Rate (%)": data["aa_rate"],
            }
        )
    return pd.DataFrame(rows)


def load_sample_dashboard_data(
    mbu_path="data/input/sample_mbu.csv",
    reference_path="data/input/sample_reference.csv",
) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """Build dashboard data from committed sample files for fresh cloud deploys."""
    mbu_df = load_text_delimited(mbu_path)
    reference_df = load_csv(reference_path)
    merged_df = merge_data(mbu_df, reference_df)
    metrics = calculate_metrics(merged_df)
    return metrics_to_dataframe(metrics), merged_df, "sample input files"


# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏥 Healthcare Claims — AA Rate Dashboard")
st.caption(f"Last refreshed: {datetime.now().strftime('%B %d, %Y  %I:%M %p')}")

st.markdown("---")

# ── Load data ─────────────────────────────────────────────────────────────────
df, source_file = load_latest_excel()
ytd_df = load_ytd()

if df is None:
    try:
        df, ytd_df, source_file = load_sample_dashboard_data()
        st.info("Showing sample dashboard data because no generated report exists yet.")
    except Exception as exc:
        st.error(f"Dashboard data could not be loaded: {exc}")
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
        delta=f"{rate - 94:.1f}% vs target",
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
