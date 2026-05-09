import sys
from config import PATHS, ensure_dirs, EMAIL
from src.ingestion import load_text_delimited, load_csv
from src.validation import validate
from src.processing import merge_data, append_to_ytd, save_csv
from src.metrics import calculate_metrics, print_metrics, save_excel_report
from src.report import generate_and_send_email
import shutil
from datetime import datetime

def main():
    try:
        ensure_dirs()
        
        print("=" * 70)
        print("Healthcare Claims Auto-Adjudication Pipeline - STARTED")
        print("=" * 70)
        
        # Step 1: Load data
        print("\n[1] Loading data...")
        mbu_df = load_text_delimited(PATHS["raw_mbu_data"])
        reference_df = load_csv(PATHS["reference_csv"])
        print(f"  Loaded {len(mbu_df)} MBU records, {len(reference_df)} reference records")
        
        # Step 2: Validate
        print("\n[2] Validating data...")
        mbu_df = validate(mbu_df)
        reference_df = validate(reference_df, required_cols=["SegmentCode"])
        print(f"  Validation passed")
        
        # Step 3: Process
        print("\n[3] Processing data...")
        merged_df = merge_data(mbu_df, reference_df)
        ytd_df = append_to_ytd(merged_df)
        # After ytd_df.to_csv(ytd_path...) line, add:
        processed_filename = f"mbu_{datetime.today().strftime('%Y%m%d')}.csv"
        shutil.copy(PATHS["raw_mbu_data"], f"data/processed/{processed_filename}")
        print(f"  MBU file archived to: data/processed/{processed_filename}")
        save_csv(ytd_df, PATHS["ytd_dataset"])
        print(f"  Merged {len(merged_df)} records")
        
        # Step 4: Calculate metrics
        print("\n[4] Calculating metrics...")
        metrics = calculate_metrics(merged_df)
        print_metrics(metrics)
        
        # Step 5: Save report
        print("\n[5] Saving Excel report...")
        save_excel_report(metrics, PATHS["excel_report"])
        
        ytd_excel_path = f"data/output/YTD_{datetime.today().strftime('%Y%m%d')}.xlsx"
        ytd_df.to_excel(ytd_excel_path, index=False)
        print(f"  YTD dataset saved as a separate file to {ytd_excel_path}")
        
        # Step 6: Send email report
        print("\n[6] Sending email notification...")
        generate_and_send_email(metrics, EMAIL, [PATHS["excel_report"], ytd_excel_path])

        print("=" * 70)
        print("Pipeline completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        print("=" * 70)
        raise

if __name__ == "__main__":
    main()