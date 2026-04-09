import configparser
import pandas as pd
import os
from datetime import datetime
# import win32com.client as win32

# Import custom logger utilities
from logger import setup_logger, log_section_start, log_section_end, log_metrics, log_dataframe_info, log_error_with_context

def load_config(config_path='config.ini'):
    """Loads configuration and execution mode."""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def parse_and_merge_data(config, logger):
    """Parses MBU files, merges with reference CSV, and appends to YTD."""
    log_section_start(logger, "Data Parsing and Merging")
    
    try:
        # Get file paths from config
        mbu_path = config['Paths']['raw_mbu_data']
        reference_path = config['Paths']['reference_csv']
        ytd_path = config['Paths']['ytd_dataset']
        
        logger.info(f"Reading MBU data from: {mbu_path}")
        
        # Parse MBU text file (pipe-delimited)
        mbu_df = pd.read_csv(mbu_path, sep='|')
        logger.info(f"Loaded {len(mbu_df)} records from MBU report")
        log_dataframe_info(logger, mbu_df, "MBU Data")
        
        # Load reference CSV data
        logger.info(f"Reading reference data from: {reference_path}")
        reference_df = pd.read_csv(reference_path)
        logger.info(f"Loaded {len(reference_df)} reference records")
        log_dataframe_info(logger, reference_df, "Reference Data")
        
        # Merge datasets on SegmentCode
        merged_df = pd.merge(mbu_df, reference_df, on='SegmentCode', how='left')
        logger.info(f"Merged data: {len(merged_df)} records")
        
        # Append to YTD dataset
        if os.path.exists(ytd_path):
            logger.info(f"Appending to existing YTD dataset at: {ytd_path}")
            ytd_df = pd.read_csv(ytd_path)
            ytd_df = pd.concat([ytd_df, merged_df], ignore_index=True)
        else:
            logger.info(f"Creating new YTD dataset at: {ytd_path}")
            ytd_df = merged_df
        
        # Save updated YTD dataset
        ytd_df.to_csv(ytd_path, index=False)
        logger.info(f"YTD dataset updated: {len(ytd_df)} total records")
        
        log_section_end(logger, "Data Parsing and Merging", success=True)
        return merged_df, ytd_df
        
    except FileNotFoundError as e:
        log_error_with_context(logger, e, "File not found during data parsing")
        log_section_end(logger, "Data Parsing and Merging", success=False)
        raise
    except pd.errors.EmptyDataError as e:
        log_error_with_context(logger, e, "Empty data file encountered")
        log_section_end(logger, "Data Parsing and Merging", success=False)
        raise
    except Exception as e:
        log_error_with_context(logger, e, "Critical error during data parsing")
        log_section_end(logger, "Data Parsing and Merging", success=False)
        raise

def compute_metrics(merged_df, logger):
    """Computes AA rates, manual claims, etc., for multiple segments."""
    log_section_start(logger, "Metrics Computation")
    
    try:
        # Define segments to process
        segments = ['WGS', 'MED', 'GBD', 'COM', 'NEW']
        segment_names = {
            'WGS': 'WGS',
            'MED': 'Medicaid',
            'GBD': 'GBD',
            'COM': 'Commercial',
            'NEW': 'New States'
        }
        
        metrics_dict = {}
        
        for segment_code in segments:
            # Filter data for this segment
            segment_data = merged_df[merged_df['SegmentCode'] == segment_code]
            
            if len(segment_data) == 0:
                logger.warning(f"No data found for segment: {segment_code}")
                continue
            
            # Calculate metrics
            total_claims = len(segment_data)
            auto_claims = len(segment_data[segment_data['ProcessingType'] == 'AUTO'])
            manual_claims = len(segment_data[segment_data['ProcessingType'] == 'MANUAL'])
            
            # Calculate AA Rate
            aa_rate = (auto_claims / total_claims * 100) if total_claims > 0 else 0
            
            # Store metrics
            metrics_dict[segment_code] = {
                'segment_name': segment_names.get(segment_code, segment_code),
                'total_claims': total_claims,
                'auto_claims': auto_claims,
                'manual_claims': manual_claims,
                'aa_rate': round(aa_rate, 2)
            }
            
            # Log individual segment metrics
            segment_metrics = {
                'Total Claims': total_claims,
                'Auto Claims': auto_claims,
                'Manual Claims': manual_claims,
                'AA Rate (%)': f"{aa_rate:.2f}"
            }
            log_metrics(logger, segment_metrics, prefix=segment_code)
        
        log_section_end(logger, "Metrics Computation", success=True)
        return metrics_dict
        
    except Exception as e:
        log_error_with_context(logger, e, "Error computing metrics")
        log_section_end(logger, "Metrics Computation", success=False)
        raise

def update_excel_report(config, metrics_dict, logger):
    """Updates the Excel reporting workbook."""
    log_section_start(logger, "Excel Report Generation")
    
    try:
        report_path = config['Paths']['excel_report']
        logger.info(f"Creating Excel report at: {report_path}")
        
        # Create a DataFrame from metrics
        metrics_list = []
        for segment_code, metrics in metrics_dict.items():
            metrics_list.append({
                'Segment Code': segment_code,
                'Segment Name': metrics['segment_name'],
                'Total Claims': metrics['total_claims'],
                'Auto Claims': metrics['auto_claims'],
                'Manual Claims': metrics['manual_claims'],
                'AA Rate (%)': metrics['aa_rate']
            })
        
        metrics_df = pd.DataFrame(metrics_list)
        log_dataframe_info(logger, metrics_df, "Excel Report Data")
        
        # Create Excel writer object
        with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
            # Write metrics to Excel
            metrics_df.to_excel(writer, sheet_name='West Market Summary', index=False)
            
            # Get the worksheet to apply formatting
            worksheet = writer.sheets['West Market Summary']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        logger.info(f"Excel report created successfully with {len(metrics_list)} segments")
        log_section_end(logger, "Excel Report Generation", success=True)
        return report_path
        
    except PermissionError as e:
        report_path = config['Paths']['excel_report']
        log_error_with_context(logger, e, f"Permission denied: Please close the Excel file at {report_path}")
        log_section_end(logger, "Excel Report Generation", success=False)
        raise
    except Exception as e:
        log_error_with_context(logger, e, "Failed to update Excel report")
        log_section_end(logger, "Excel Report Generation", success=False)
        raise

def generate_and_send_email(config, logger):
    """Generates formatted HTML report and sends via Outlook."""
    logger.info("Generating HTML email and sending via Outlook...")
    logger.info("Email functionality - placeholder for Phase 2")
    # Add logic here in Phase 2
    pass

def main():
    # Step 1: Load configuration
    config = load_config()
    
    # Step 2: Setup logger using custom logger module
    log_file = config['Logging'].get('log_file', 'logs/pipeline.log')
    logger = setup_logger(
        name='pipeline',
        log_file=log_file,
        console_output=True
    )
    
    logger.info("=" * 70)
    logger.info("Healthcare Claims Auto-Adjudication Pipeline - STARTED")
    logger.info("=" * 70)
    
    try:
        # Following the workflow outlined in the README
        # Step 2-4: Parse, merge, and append data
        merged_df, ytd_df = parse_and_merge_data(config, logger)
        
        # Step 5: Compute metrics for all segments
        metrics_dict = compute_metrics(merged_df, logger)
        
        # Step 6: Update Excel report
        report_path = update_excel_report(config, metrics_dict, logger)
        
        # Step 7-8: Generate and send email (placeholder for Phase 2)
        generate_and_send_email(config, logger)
        
        logger.info("=" * 70)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.critical("=" * 70)
        log_error_with_context(logger, e, "Pipeline aborted due to critical error")
        logger.critical("=" * 70)
        raise
    finally:
        # This ensures the completion message is logged whether it succeeds or fails
        logger.info("Healthcare Claims Auto-Adjudication Pipeline - FINISHED")
        logger.info("=" * 70)

if __name__ == "__main__":
    main()