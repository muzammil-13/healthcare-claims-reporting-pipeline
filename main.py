import sys
import logging
from config import PATHS, ensure_dirs, EMAIL, LOG_FILE
from src.ingestion import load_text_delimited, load_csv
from src.validation import validate
from src.processing import merge_data, append_to_ytd, save_csv
from src.metrics import calculate_metrics, print_metrics, save_excel_report
from src.report import generate_and_send_email
import shutil
from datetime import datetime, timedelta

def main():
    # Create directories first so the logs/ folder exists for the FileHandler
    ensure_dirs()
    
    # Configure logging to write to both the console and the log file
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)

    try:
        # The pipeline reports on yesterday's claims (T-1)
        report_date = datetime.today() - timedelta(days=1)
        report_date_str = report_date.strftime('%Y%m%d')
        formatted_date = report_date.strftime('%B %d, %Y')
        
        logger.info("=" * 70)
        logger.info(f"Healthcare Claims Auto-Adjudication Pipeline - STARTED (Reporting for {formatted_date})")
        logger.info("=" * 70)
        
        # Step 1: Load data
        logger.info("[1] Loading data...")
        mbu_df = load_text_delimited(PATHS["raw_mbu_data"])
        reference_df = load_csv(PATHS["reference_csv"])
        logger.info(f"  Loaded {len(mbu_df)} MBU records, {len(reference_df)} reference records")
        
        # Step 2: Validate
        logger.info("[2] Validating data...")
        mbu_df = validate(mbu_df)
        reference_df = validate(reference_df, required_cols=["SegmentCode"])
        logger.info("  Validation passed")
        
        # Step 3: Process
        logger.info("[3] Processing data...")
        merged_df = merge_data(mbu_df, reference_df)
        ytd_df = append_to_ytd(merged_df)
        # After ytd_df.to_csv(ytd_path...) line, add:
        processed_filename = f"mbu_{report_date_str}.csv"
        shutil.copy(PATHS["raw_mbu_data"], f"data/processed/{processed_filename}")
        logger.info(f"  MBU file archived to: data/processed/{processed_filename}")
        save_csv(ytd_df, PATHS["ytd_dataset"])
        logger.info(f"  Merged {len(merged_df)} records")
        
        # Step 4: Calculate metrics
        logger.info("[4] Calculating metrics...")
        metrics = calculate_metrics(merged_df)
        print_metrics(metrics)
        
        # Step 5: Save report
        logger.info("[5] Saving Excel report...")
        save_excel_report(metrics, PATHS["excel_report"])
        
        ytd_excel_path = f"data/output/YTD_{report_date_str}.xlsx"
        ytd_df.to_excel(ytd_excel_path, sheet_name=f"YTD_{report_date_str}", index=False)
        logger.info(f"  YTD dataset saved as a separate file to {ytd_excel_path}")
        
        # Step 6: Send email report
        logger.info("[6] Sending email notification...")
        generate_and_send_email(metrics, EMAIL, [PATHS["excel_report"], ytd_excel_path], formatted_date)

        logger.info("=" * 70)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()