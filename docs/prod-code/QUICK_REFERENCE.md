# Quick Reference Guide - Production Patterns Implementation

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install pandas openpyxl pywin32
```

### 2. Set Environment Variables
```bash
# Windows PowerShell
$env:SEND_EMAIL="false"
$env:TO_LIST="recipient@domain.com"
$env:CC_LIST="manager@domain.com"

# Windows CMD
set SEND_EMAIL=false
set TO_LIST=recipient@domain.com
set CC_LIST=manager@domain.com

# Linux/Mac
export SEND_EMAIL=false
export TO_LIST=recipient@domain.com
export CC_LIST=manager@domain.com
```

### 3. Import Enhanced Functions
```python
from enhanced_pipeline import (
    process_by_segments,
    calculate_advanced_metrics,
    update_excel_with_duplicate_check,
    generate_html_email_body,
    send_outlook_email,
    accumulate_ytd_data
)
```

---

## 📋 Function Reference

### 1. Multi-Segment Processing

```python
segments = {
    'WGS': 'WGS Market',
    'MED': 'Medicaid',
    'GBD': 'GBD Rates'
}

segment_data = process_by_segments(
    df=merged_df,
    segment_column='SegmentCode',
    segments_dict=segments,
    logger=logger
)
# Returns: {'WGS': df_wgs, 'MED': df_med, 'GBD': df_gbd}
```

### 2. Advanced Metrics Calculation

```python
metric_columns = [
    'ITS_RCVD', 'ITS_FNLZD', 'ITS_AA',
    'CON_RCVD', 'CON_FNLZD', 'CON_AA',
    'ITS_SYS_AA', 'ITS_AUTO_REJ_AA', 'ITS_RECY_AA',
    'CON_SYS_AA', 'CON_AUTO_REJ_AA', 'CON_RECY_AA',
    'ITS_OC_AA', 'ITS_COGAI_AA',
    'CON_OC_AA', 'CON_COGAI_AA'
]

metrics_df = calculate_advanced_metrics(
    df=segment_df,
    metric_columns=metric_columns,
    logger=logger
)
# Returns DataFrame with: Total_Claims, Total_AA, Manual_Claims, 
#                        AA_Rate_Pct, First_Pass, Second_Pass
```

### 3. Excel Update with Duplicate Check

```python
success = update_excel_with_duplicate_check(
    excel_path='data/output/West_Market_Summary.xlsx',
    sheet_name='Summary',
    date_value='04/17/2026',
    data_row=metrics_df.iloc[0],  # or dict
    logger=logger
)
# Returns: True if updated, False if duplicate found
```

### 4. HTML Email Generation

```python
html_body = generate_html_email_body(
    metrics_dict={
        'WGS Market': df_wgs_metrics,
        'Medicaid': df_med_metrics,
        'GBD Rates': df_gbd_metrics
    },
    report_date='04/17/2026',
    title="Healthcare Claims Report"
)
# Returns: HTML string with styled tables
```

### 5. Outlook Email Sending

```python
success = send_outlook_email(
    subject='Healthcare Claims Report - 04/17/2026',
    html_body=html_body,
    to_list='recipient1@domain.com; recipient2@domain.com',
    cc_list='manager@domain.com',
    attachments=['data/output/West_Market_Summary.xlsx'],
    logger=logger
)
# Returns: True if sent, False if SEND_EMAIL not enabled
```

### 6. YTD Data Accumulation

```python
ytd_df = accumulate_ytd_data(
    new_data_df=merged_df,
    ytd_file_path='data/processed/ytd_data.csv',
    date_column='ReportDate',
    logger=logger
)
# Returns: Updated YTD DataFrame (duplicates removed)
```

---

## 🎯 Common Use Cases

### Use Case 1: Daily Report Processing

```python
def daily_report_workflow(config, logger):
    # 1. Load and merge data
    merged_df = load_and_merge_data(config, logger)
    
    # 2. Process by segments
    segments = {'WGS': 'WGS Market', 'MED': 'Medicaid'}
    segment_data = process_by_segments(merged_df, 'SegmentCode', segments, logger)
    
    # 3. Calculate metrics
    metrics_dict = {}
    metric_columns = ['ITS_RCVD', 'ITS_FNLZD', 'ITS_AA', 'CON_RCVD', 'CON_FNLZD', 'CON_AA']
    
    for code, segment_df in segment_data.items():
        metrics_dict[segments[code]] = calculate_advanced_metrics(
            segment_df, metric_columns, logger
        )
    
    # 4. Update Excel
    today = datetime.now().strftime('%m/%d/%Y')
    update_excel_with_duplicate_check(
        'data/output/report.xlsx', 'Summary', today,
        metrics_dict['WGS Market'].iloc[0], logger
    )
    
    # 5. Send email
    html_body = generate_html_email_body(metrics_dict, today)
    send_outlook_email(
        f'Daily Report - {today}', html_body,
        config['Email']['recipients'],
        attachments=['data/output/report.xlsx'],
        logger=logger
    )
```

### Use Case 2: Month-End Processing

```python
def month_end_workflow(config, logger):
    # 1. Load month data
    month_df = load_month_data(config, logger)
    
    # 2. Accumulate to YTD
    ytd_df = accumulate_ytd_data(
        month_df,
        'data/processed/ytd_data.csv',
        'ReportDate',
        logger
    )
    
    # 3. Calculate YTD metrics
    ytd_metrics = calculate_advanced_metrics(ytd_df, metric_columns, logger)
    
    # 4. Generate comprehensive report
    # ... (similar to daily workflow)
```

### Use Case 3: Ad-Hoc Analysis

```python
def analyze_segment_performance(df, segment_code, logger):
    # Filter to specific segment
    segment_df = df[df['SegmentCode'] == segment_code]
    
    # Calculate metrics
    metrics = calculate_advanced_metrics(segment_df, metric_columns, logger)
    
    # Format for display
    formatted_df = format_dataframe_for_html(metrics)
    
    return formatted_df
```

---

## 🔧 Configuration Examples

### config.ini
```ini
[Settings]
execution_mode = MTD

[Paths]
raw_mbu_data = data/input/mbu_report.txt
reference_csv = data/input/reference_data.csv
ytd_dataset = data/processed/ytd_data.csv
excel_report = data/output/West_Market_Summary.xlsx

[Email]
sender = reports@domain.com
recipients = team@domain.com; manager@domain.com
subject = Healthcare Claims Auto-Adjudication Report

[Logging]
log_file = logs/pipeline.log
```

### .env (for sensitive data)
```
SEND_EMAIL=false
TO_LIST=recipient1@domain.com;recipient2@domain.com
CC_LIST=manager@domain.com
SENDER_MAIL=sender@domain.com
```

---

## 📊 Data Structure Requirements

### Input DataFrame Columns

**Minimum Required:**
```python
required_columns = [
    'SegmentCode',      # Segment identifier (WGS, MED, GBD, etc.)
    'ITS_RCVD',         # Institutional claims received
    'ITS_FNLZD',        # Institutional claims finalized
    'ITS_AA',           # Institutional auto-adjudicated
    'CON_RCVD',         # Conventional claims received
    'CON_FNLZD',        # Conventional claims finalized
    'CON_AA'            # Conventional auto-adjudicated
]
```

**Optional (for advanced metrics):**
```python
optional_columns = [
    'ITS_SYS_AA',       # Institutional system AA
    'ITS_AUTO_REJ_AA',  # Institutional auto-reject AA
    'ITS_RECY_AA',      # Institutional recycle AA
    'CON_SYS_AA',       # Conventional system AA
    'CON_AUTO_REJ_AA',  # Conventional auto-reject AA
    'CON_RECY_AA',      # Conventional recycle AA
    'ITS_OC_AA',        # Institutional OC AA
    'ITS_COGAI_AA',     # Institutional COGAI AA
    'CON_OC_AA',        # Conventional OC AA
    'CON_COGAI_AA'      # Conventional COGAI AA
]
```

### Output Metrics

```python
output_metrics = {
    'Total_Claims': int,        # Sum of finalized claims
    'Total_AA': int,            # Sum of auto-adjudicated
    'Manual_Claims': int,       # Total - AA
    'Total_RCVD': int,          # Sum of received
    'First_Pass': int,          # System + AutoReject + Recycle
    'Second_Pass': int,         # OC + COGAI
    'AA_Rate_Pct': float        # (AA / Total) * 100
}
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: Excel File Permission Error
```
PermissionError: [Errno 13] Permission denied: 'report.xlsx'
```
**Solution:** Close the Excel file before running the script.

### Issue 2: Email Not Sending
```
Email sending disabled (SEND_EMAIL not set to 'true')
```
**Solution:** Set environment variable: `set SEND_EMAIL=true`

### Issue 3: win32com Import Error
```
ImportError: No module named 'win32com'
```
**Solution:** Install pywin32: `pip install pywin32`

### Issue 4: Duplicate Data Warning
```
Data for 04/17/2026 already exists in Excel. Skipping update.
```
**Solution:** This is expected behavior. Delete the row in Excel if you want to re-insert.

### Issue 5: Missing Columns
```
KeyError: 'ITS_RCVD'
```
**Solution:** Ensure your DataFrame has all required columns. Check column names match exactly.

---

## 📈 Performance Tips

1. **Batch Processing:** Process multiple segments in one call
2. **Column Selection:** Only include necessary columns in metric_columns
3. **Memory Management:** Use `del` to free large DataFrames after use
4. **Excel Updates:** Update multiple sheets in one workbook open/save cycle
5. **Email Attachments:** Compress large files before attaching

---

## 🧪 Testing

### Test with Sample Data
```python
# Create sample data
sample_data = {
    'SegmentCode': ['WGS', 'WGS', 'MED', 'MED'],
    'ITS_RCVD': [1000, 1500, 800, 900],
    'ITS_FNLZD': [950, 1400, 750, 850],
    'ITS_AA': [900, 1300, 700, 800],
    'CON_RCVD': [500, 600, 400, 450],
    'CON_FNLZD': [480, 580, 380, 430],
    'CON_AA': [450, 550, 360, 410]
}
df = pd.DataFrame(sample_data)

# Test processing
segments = {'WGS': 'WGS Market', 'MED': 'Medicaid'}
segment_data = process_by_segments(df, 'SegmentCode', segments)

# Verify results
for code, segment_df in segment_data.items():
    print(f"{code}: {len(segment_df)} records")
```

---

## 📚 Additional Resources

- **Implementation Guide:** See `IMPLEMENTATION_GUIDE.md` for detailed patterns
- **Production Analysis:** See `PRODUCTION_CODE_ANALYSIS.md` for insights
- **Enhanced Module:** See `enhanced_pipeline.py` for function implementations
- **Logger Guide:** See `LOGGER_USAGE_GUIDE.md` for logging best practices

---

## 🎓 Best Practices

1. ✅ Always use logger for tracking operations
2. ✅ Check for duplicates before inserting data
3. ✅ Format numbers properly in reports (commas, decimals)
4. ✅ Recalculate rates for grand totals (don't sum percentages)
5. ✅ Use environment variables for sensitive configuration
6. ✅ Test with SEND_EMAIL=false before production
7. ✅ Backup Excel files before updates
8. ✅ Validate data before processing
9. ✅ Handle errors gracefully with try-except
10. ✅ Document your configuration changes

---

**Quick Reference Version:** 1.0  
**Last Updated:** 2026-04-17  
**Made with Bob** 🤖