import logging
from config import SEGMENT_CODES

logger = logging.getLogger(__name__)

def calculate_metrics(df):
    """Calculate metrics per segment: total, auto, manual, AA rate."""
    metrics = {}
    
    for segment_code in SEGMENT_CODES:
        segment_data = df[df["SegmentCode"] == segment_code]
        
        if len(segment_data) == 0:
            continue
        
        total = int(segment_data["TOT_CLMS"].sum())
        auto = int(segment_data["TOT_AA"].sum())
        manual = total - auto
        aa_rate = round(auto / total * 100, 2) if total > 0 else 0
        
        metrics[segment_code] = {
            "segment_name": SEGMENT_CODES.get(segment_code, segment_code),
            "total_claims": total,
            "auto_claims": auto,
            "manual_claims": manual,
            "aa_rate": aa_rate,
        }
    
    return metrics

def print_metrics(metrics):
    """Pretty print metrics."""
    logger.info("=" * 70)
    logger.info("METRICS SUMMARY")
    logger.info("=" * 70)
    
    for segment_code, data in metrics.items():
        logger.info(f"{data['segment_name']} ({segment_code}):")
        logger.info(f"  Total Claims: {data['total_claims']}")
        logger.info(f"  Auto Claims:  {data['auto_claims']}")
        logger.info(f"  Manual Claims: {data['manual_claims']}")
        logger.info(f"  AA Rate (%): {data['aa_rate']}")
    
    logger.info("=" * 70)

def save_excel_report(metrics, excel_path):
    """Save metrics to Excel workbook."""
    import pandas as pd
    import os
    
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    
    rows = []
    for segment_code, data in metrics.items():
        rows.append({
            "Segment Code": segment_code,
            "Segment Name": data["segment_name"],
            "Total Claims": data["total_claims"],
            "Auto Claims": data["auto_claims"],
            "Manual Claims": data["manual_claims"],
            "AA Rate (%)": data["aa_rate"],
        })
    
    df = pd.DataFrame(rows)
    
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="West Market Summary", index=False)
    
    logger.info(f"  Excel report saved to {excel_path}")
