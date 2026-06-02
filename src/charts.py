"""
charts.py — Chart generation for AA rate reporting.

Generates:
1. A base64-encoded PNG bar chart for embedding inline in HTML emails.
   (No file attachment needed — the image travels with the email body.)
2. A reusable chart function that Streamlit can also call with live data.

Why base64 inline?
   Email clients block external image URLs for security.
   Attaching the image as a CID reference is complex.
   Base64 inline works across Gmail, Outlook, and most clients.
"""

import io
import base64
import logging
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — safe for servers and scripts
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

logger = logging.getLogger(__name__)

# Color palette — maps segment names to colors for consistency across email + dashboard
SEGMENT_COLORS = {
    "WGS":        "#1f77b4",  # blue
    "MED":        "#2ca02c",  # green
    "GBD":        "#ff7f0e",  # orange
    "COM":        "#9467bd",  # purple
    "NEW":        "#17becf",  # teal
}
DEFAULT_COLOR = "#8c8c8c"

# AA rate threshold line — leadership benchmark
AA_TARGET_RATE = 94.0


def build_chart_dataframe(metrics: dict) -> pd.DataFrame:
    """
    Convert the metrics dict from metrics.py into a flat DataFrame for charting.

    Args:
        metrics: Output of calculate_metrics() — dict keyed by segment code.

    Returns:
        DataFrame with columns: segment_code, segment_name, aa_rate
    """
    rows = []
    for code, data in metrics.items():
        rows.append({
            "segment_code": code,
            "segment_name": data["segment_name"],
            "aa_rate": data["aa_rate"],
            "total_claims": data["total_claims"],
            "auto_claims": data["auto_claims"],
            "manual_claims": data["manual_claims"],
        })
    return pd.DataFrame(rows)


def generate_aa_rate_chart_base64(metrics: dict, report_date: str = "") -> str:
    """
    Generate a bar chart of AA rates per segment and return it as a base64 PNG.
    Used for inline embedding in HTML emails.

    Args:
        metrics: Output of calculate_metrics().
        report_date: Human-readable date string for the chart title.

    Returns:
        Base64-encoded PNG string (ready to use in <img src="data:image/png;base64,...">).
        Returns empty string if chart generation fails.
    """
    try:
        df = build_chart_dataframe(metrics)

        if df.empty:
            logger.warning("  [Charts] No metrics data — skipping chart generation.")
            return ""

        fig, ax = plt.subplots(figsize=(9, 5))

        colors = [SEGMENT_COLORS.get(code, DEFAULT_COLOR) for code in df["segment_code"]]
        bars = ax.bar(df["segment_name"], df["aa_rate"], color=colors, width=0.5, zorder=3)

        # Target line
        ax.axhline(
            y=AA_TARGET_RATE,
            color="#d62728",
            linestyle="--",
            linewidth=1.4,
            label=f"Target: {AA_TARGET_RATE}%",
            zorder=4,
        )

        # Value labels on top of each bar
        for bar, rate in zip(bars, df["aa_rate"]):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.8,
                f"{rate:.2f}%",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color="#333333",
            )

        ax.set_ylim(0, 110)
        ax.set_ylabel("AA Rate (%)", fontsize=11)
        ax.set_xlabel("Business Segment", fontsize=11)
        title = f"Auto-Adjudication Rate by Segment"
        if report_date:
            title += f"  |  {report_date}"
        ax.set_title(title, fontsize=13, fontweight="bold", pad=14)
        ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        target_patch = mpatches.Patch(color="#d62728", label=f"Target ({AA_TARGET_RATE}%)")
        ax.legend(handles=[target_patch], fontsize=9, loc="upper right")

        plt.tight_layout()

        # Write to in-memory buffer and encode
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode("utf-8")

        logger.info("  [Charts] AA rate chart generated successfully.")
        return encoded

    except Exception as e:
        logger.error(f"  [Charts] Chart generation failed: {e}")
        return ""


def generate_aa_rate_chart_figure(metrics: dict, report_date: str = ""):
    """
    Return a matplotlib Figure object — used by Streamlit for live rendering.

    Streamlit calls st.pyplot(fig) directly so we return the figure, not bytes.

    Args:
        metrics: Output of calculate_metrics().
        report_date: Human-readable date string for the chart title.

    Returns:
        matplotlib Figure object, or None on failure.
    """
    try:
        df = build_chart_dataframe(metrics)

        if df.empty:
            return None

        fig, ax = plt.subplots(figsize=(10, 5))
        colors = [SEGMENT_COLORS.get(code, DEFAULT_COLOR) for code in df["segment_code"]]
        bars = ax.bar(df["segment_name"], df["aa_rate"], color=colors, width=0.5, zorder=3)

        ax.axhline(
            y=AA_TARGET_RATE,
            color="#d62728",
            linestyle="--",
            linewidth=1.4,
            label=f"Target: {AA_TARGET_RATE}%",
            zorder=4,
        )

        for bar, rate in zip(bars, df["aa_rate"]):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.8,
                f"{rate:.2f}%",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color="#333333",
            )

        ax.set_ylim(0, 110)
        ax.set_ylabel("AA Rate (%)", fontsize=11)
        ax.set_xlabel("Business Segment", fontsize=11)
        title = f"Auto-Adjudication Rate by Segment"
        if report_date:
            title += f"  |  {report_date}"
        ax.set_title(title, fontsize=13, fontweight="bold", pad=14)
        ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        target_patch = mpatches.Patch(color="#d62728", label=f"Target ({AA_TARGET_RATE}%)")
        ax.legend(handles=[target_patch], fontsize=9, loc="upper right")
        plt.tight_layout()

        return fig

    except Exception as e:
        logger.error(f"  [Charts] Streamlit figure generation failed: {e}")
        return None
