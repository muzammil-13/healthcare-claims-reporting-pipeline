# Production Code Implementation Guide

## 📋 Overview

This guide shows how to implement enterprise-grade patterns from the production code (`DailyGBDRavenCommRate2025_redacted.py`) into your healthcare claims reporting pipeline.

---

## 🔍 Key Patterns Identified

### 1. **Multi-Segment Data Processing**
**Production Pattern:**
```python
# Filter by multiple segments
l = ['LOCAL - CA', 'LOCAL - NV', 'LOCAL - CO']
df1 = df1[df1['LOB'].isin(l)]

# Process each segment separately
dfa = df1[df1['LOB'].isin(['LOCAL - CA'])]
dfb = df1[df1['LOB'].isin(['LOCAL - NV'])]
dfc = df1[df1['LOB'].isin(['LOCAL - CO'])]
```

**Your Implementation:**
```python
def process_by_segments(df, segment_column, segments_dict):
    """
    Process data by multiple segments and return aggregated results.
    
    Args:
        df: Input DataFrame
        segment_column: Column name to filter on
        segments_dict: Dict mapping segment codes to names
    
    Returns:
        Dict of DataFrames, one per segment
    """
    segment_data = {}
    for code, name in segments_dict.items():
        segment_df = df[df[segment_column] == code].copy()
        segment_data[code] = segment_df
    return segment_data
```

---

### 2. **Advanced Metric Calculations**

**Production Pattern:**
```python
# Calculate totals for specific columns
selcols = ['ITS_RCVD', 'ITS_FNLZD', 'ITS_AA', 'CON_RCVD', 'CON_FNLZD', 'CON_AA']
totdict = {}
for i in selcols:
    totdict[i + ' Total'] = dfa[i].sum()

# Calculate derived metrics
Totaldf['Sum of TOT_AA'] = Totaldf['ITS_AA Total'] + Totaldf['CON_AA Total']
Totaldf['Manual PROCSD'] = Totaldf['Sum of TOT_CLMS'] - Totaldf['Sum of TOT_AA']
Totaldf['aa_rate %'] = round(Totaldf['Sum of TOT_AA'] / Totaldf['Sum of TOT_CLMS'], 4) * 100
```

**Your Implementation:**
```python
def calculate_advanced_metrics(df, metric_columns):
    """
    Calculate comprehensive metrics including totals, rates, and derived values.
    
    Args:
        df: Input DataFrame with claims data
        metric_columns: List of columns to aggregate
    
    Returns:
        DataFrame with calculated metrics
    """
    metrics = {}
    
    # Sum specified columns
    for col in metric_columns:
        metrics[f'{col}_Total'] = df[col].sum()
    
    # Calculate derived metrics
    metrics['Total_Claims'] = metrics.get('ITS_FNLZD_Total', 0) + metrics.get('CON_FNLZD_Total', 0)
    metrics['Total_AA'] = metrics.get('ITS_AA_Total', 0) + metrics.get('CON_AA_Total', 0)
    metrics['Manual_Claims'] = metrics['Total_Claims'] - metrics['Total_AA']
    
    # Calculate rates
    if metrics['Total_Claims'] > 0:
        metrics['AA_Rate_Pct'] = round((metrics['Total_AA'] / metrics['Total_Claims']) * 100, 2)
    else:
        metrics['AA_Rate_Pct'] = 0.0
    
    # First Pass (System + Auto Reject + Recycle)
    first_pass_cols = ['ITS_SYS_AA_Total', 'ITS_AUTO_REJ_AA_Total', 'ITS_RECY_AA_Total',
                       'CON_SYS_AA_Total', 'CON_AUTO_REJ_AA_Total', 'CON_RECY_AA_Total']
    metrics['First_Pass'] = sum(metrics.get(col, 0) for col in first_pass_cols)
    
    # Second Pass (OC + COGAI)
    second_pass_cols = ['ITS_OC_AA_Total', 'ITS_COGAI_AA_Total', 
                        'CON_OC_AA_Total', 'CON_COGAI_AA_Total']
    metrics['Second_Pass'] = sum(metrics.get(col, 0) for col in second_pass_cols)
    
    return pd.DataFrame([metrics])
```

---

### 3. **Excel Workbook Update with Duplicate Prevention**

**Production Pattern:**
```python
import openpyxl
from openpyxl import load_workbook

workbook = openpyxl.load_workbook(workpath)
worksheet = workbook['Westmarketaarate']
exceldf = pd.read_excel(workpath)

# Check for duplicates
if today in exceldf['Unnamed: 0'].values:
    print("This data already present in Excel")
    break
else:
    last_row = worksheet.max_row + 1
    worksheet.cell(row=last_row, column=1).value = today
    for col_index, value in enumerate(com.iloc[-1]):
        worksheet.cell(row=last_row, column=col_index+2).value = value
    workbook.save(workpath)
```

**Your Implementation:**
```python
def update_excel_with_duplicate_check(excel_path, sheet_name, date_value, data_row, logger):
    """
    Update Excel workbook with new data, checking for duplicates first.
    
    Args:
        excel_path: Path to Excel file
        sheet_name: Name of worksheet to update
        date_value: Date value to check for duplicates
        data_row: Pandas Series or dict with data to append
        logger: Logger instance
    
    Returns:
        bool: True if updated, False if duplicate found
    """
    import openpyxl
    from openpyxl import load_workbook
    
    try:
        # Load workbook
        workbook = openpyxl.load_workbook(excel_path)
        worksheet = workbook[sheet_name]
        
        # Read existing data to check for duplicates
        existing_df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # Check if date already exists (assuming first column is date)
        date_column = existing_df.columns[0]
        if date_value in existing_df[date_column].values:
            logger.warning(f"Data for {date_value} already exists in Excel. Skipping update.")
            return False
        
        # Append new row
        last_row = worksheet.max_row + 1
        
        # Write date in first column
        worksheet.cell(row=last_row, column=1).value = date_value
        
        # Write data values
        if isinstance(data_row, pd.Series):
            for col_index, value in enumerate(data_row):
                worksheet.cell(row=last_row, column=col_index + 2).value = value
        elif isinstance(data_row, dict):
            for col_index, (key, value) in enumerate(data_row.items()):
                worksheet.cell(row=last_row, column=col_index + 2).value = value
        
        # Save workbook
        workbook.save(excel_path)
        logger.info(f"Successfully updated Excel with data for {date_value}")
        return True
        
    except FileNotFoundError:
        logger.error(f"Excel file not found: {excel_path}")
        raise
    except PermissionError:
        logger.error(f"Permission denied. Please close Excel file: {excel_path}")
        raise
    except Exception as e:
        logger.error(f"Error updating Excel: {str(e)}")
        raise
```

---

### 4. **HTML Email Generation**

**Production Pattern:**
```python
# Format numbers with commas
numeric_columns = com.select_dtypes(include=['number']).columns[:-1]
for colum in numeric_columns:
    if pd.api.types.is_numeric_dtype(com[colum]):
        com[colum] = com[colum].apply(lambda y: '{:,}'.format(y))

# Generate HTML table
htmltable = com.to_html()

# Create email body with multiple tables
html_body = f"""<html><body>
    <h2>WGS Report</h2>
    {htmltable_wgs}
    <h2>GBD Rates</h2>
    {htmltable_gbd}
    <h2>Medicaid</h2>
    {htmltable1}
</body></html>"""
```

**Your Implementation:**
```python
def format_dataframe_for_html(df, format_numbers=True):
    """
    Format DataFrame for HTML display with proper number formatting.
    
    Args:
        df: Input DataFrame
        format_numbers: Whether to format numeric columns with commas
    
    Returns:
        DataFrame with formatted values
    """
    df_formatted = df.copy()
    
    if format_numbers:
        # Get numeric columns (excluding percentage columns)
        numeric_cols = df_formatted.select_dtypes(include=['number']).columns
        
        for col in numeric_cols:
            # Format integers with commas, keep decimals for percentages
            if 'rate' in col.lower() or '%' in col.lower() or 'pct' in col.lower():
                df_formatted[col] = df_formatted[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "")
            else:
                df_formatted[col] = df_formatted[col].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "")
    
    return df_formatted


def generate_html_email_body(metrics_dict, report_date):
    """
    Generate comprehensive HTML email body with multiple formatted tables.
    
    Args:
        metrics_dict: Dictionary of DataFrames for each segment
        report_date: Date of the report
    
    Returns:
        str: HTML formatted email body
    """
    html_parts = [
        "<html>",
        "<head>",
        "<style>",
        "table { border-collapse: collapse; margin: 20px 0; font-family: Arial, sans-serif; }",
        "th { background-color: #4CAF50; color: white; padding: 12px; text-align: left; }",
        "td { border: 1px solid #ddd; padding: 8px; }",
        "tr:nth-child(even) { background-color: #f2f2f2; }",
        "h2 { color: #333; font-family: Arial, sans-serif; }",
        "h3 { color: #666; font-family: Arial, sans-serif; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h2>Healthcare Claims Auto-Adjudication Report - {report_date}</h2>",
    ]
    
    # Add each segment's table
    for segment_name, df in metrics_dict.items():
        html_parts.append(f"<h3>{segment_name}</h3>")
        
        # Format DataFrame and convert to HTML
        df_formatted = format_dataframe_for_html(df)
        table_html = df_formatted.to_html(index=True, escape=False, border=1)
        html_parts.append(table_html)
    
    html_parts.extend(["</body>", "</html>"])
    
    return "\n".join(html_parts)
```

---

### 5. **Outlook Email Automation**

**Production Pattern:**
```python
SEND_EMAIL = os.getenv('SEND_EMAIL', 'false').lower() == 'true'

if SEND_EMAIL:
    import win32com.client as win
    outlook_app = win.Dispatch('Outlook.Application')
    mail = outlook_app.CreateItem(0)
    mail.Subject = sub
    mail.HTMLBody = html_body
    mail.To = TO_LIST
    mail.CC = CC_LIST
    mail.Attachments.Add(attachment)
    mail.Send()
```

**Your Implementation:**
```python
def send_outlook_email(subject, html_body, to_list, cc_list=None, attachments=None, logger=None):
    """
    Send email via Outlook with HTML body and attachments.
    
    Args:
        subject: Email subject
        html_body: HTML formatted email body
        to_list: Semicolon-separated recipient emails
        cc_list: Semicolon-separated CC emails (optional)
        attachments: List of file paths to attach (optional)
        logger: Logger instance (optional)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    # Check if email sending is enabled
    send_email = os.getenv('SEND_EMAIL', 'false').lower() == 'true'
    
    if not send_email:
        if logger:
            logger.info("Email sending disabled (SEND_EMAIL not set to 'true')")
        return False
    
    try:
        import win32com.client as win
        
        # Create Outlook application instance
        outlook_app = win.Dispatch('Outlook.Application')
        mail = outlook_app.CreateItem(0)  # 0 = MailItem
        
        # Set email properties
        mail.Subject = subject
        mail.HTMLBody = html_body
        mail.To = to_list
        
        if cc_list:
            mail.CC = cc_list
        
        # Add attachments
        if attachments:
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    mail.Attachments.Add(attachment_path)
                    if logger:
                        logger.info(f"Attached: {attachment_path}")
                else:
                    if logger:
                        logger.warning(f"Attachment not found: {attachment_path}")
        
        # Send email
        mail.Send()
        
        if logger:
            logger.info(f"Email sent successfully to: {to_list}")
        
        return True
        
    except ImportError:
        if logger:
            logger.error("win32com.client not available. Install pywin32: pip install pywin32")
        return False
    except Exception as e:
        if logger:
            logger.error(f"Failed to send email: {str(e)}")
        return False
```

---

### 6. **YTD Data Accumulation**

**Production Pattern:**
```python
# Append to MTD file
mtddf1 = pd.read_csv(netfile)
mtddf2 = df1
mtdmerged = pd.concat([mtddf1, mtddf2], ignore_index=True)
mtdmerged.to_csv(output_path7)
```

**Your Implementation:**
```python
def accumulate_ytd_data(new_data_df, ytd_file_path, date_column='ReportDate', logger=None):
    """
    Accumulate new data into YTD dataset with duplicate prevention.
    
    Args:
        new_data_df: DataFrame with new data to append
        ytd_file_path: Path to YTD CSV file
        date_column: Column name containing dates for duplicate checking
        logger: Logger instance
    
    Returns:
        DataFrame: Updated YTD dataset
    """
    try:
        # Load existing YTD data if it exists
        if os.path.exists(ytd_file_path):
            ytd_df = pd.read_csv(ytd_file_path)
            if logger:
                logger.info(f"Loaded existing YTD data: {len(ytd_df)} records")
            
            # Check for duplicates based on date
            if date_column in new_data_df.columns and date_column in ytd_df.columns:
                new_dates = new_data_df[date_column].unique()
                existing_dates = ytd_df[date_column].unique()
                duplicate_dates = set(new_dates) & set(existing_dates)
                
                if duplicate_dates:
                    if logger:
                        logger.warning(f"Found duplicate dates: {duplicate_dates}")
                    # Remove duplicates from new data
                    new_data_df = new_data_df[~new_data_df[date_column].isin(duplicate_dates)]
            
            # Append new data
            ytd_df = pd.concat([ytd_df, new_data_df], ignore_index=True)
        else:
            if logger:
                logger.info("Creating new YTD dataset")
            ytd_df = new_data_df
        
        # Save updated YTD data
        ytd_df.to_csv(ytd_file_path, index=False)
        
        if logger:
            logger.info(f"YTD data updated: {len(ytd_df)} total records")
        
        return ytd_df
        
    except Exception as e:
        if logger:
            logger.error(f"Error accumulating YTD data: {str(e)}")
        raise
```

---

## 🚀 Integration Steps

### Step 1: Update `main.py` with Enhanced Functions

Add these imports at the top:
```python
import openpyxl
from openpyxl import load_workbook
import os
from datetime import datetime
```

### Step 2: Create Enhanced Metrics Module

Create `metrics_calculator.py`:
```python
import pandas as pd
import numpy as np

def calculate_segment_metrics(df, segment_column, segment_value, metric_columns):
    """Calculate comprehensive metrics for a specific segment."""
    segment_df = df[df[segment_column] == segment_value].copy()
    
    # Convert columns to numeric
    for col in metric_columns:
        if col in segment_df.columns:
            segment_df[col] = pd.to_numeric(segment_df[col], errors='coerce')
    
    # Calculate metrics
    metrics = {}
    for col in metric_columns:
        if col in segment_df.columns:
            metrics[f'{col}_Total'] = segment_df[col].sum()
    
    return metrics
```

### Step 3: Update Configuration

Add to `config.ini`:
```ini
[Email]
send_email = false
outlook_enabled = true
attachment_paths = data/output/West_Market_Summary.xlsx

[Processing]
check_duplicates = true
date_format = %m/%d/%Y
```

### Step 4: Environment Variables

Create `.env` file:
```
SEND_EMAIL=false
TO_LIST=recipient1@domain.com;recipient2@domain.com
CC_LIST=manager@domain.com
SENDER_MAIL=sender@domain.com
```

---

## 📊 Usage Example

```python
from enhanced_pipeline import (
    process_by_segments,
    calculate_advanced_metrics,
    update_excel_with_duplicate_check,
    generate_html_email_body,
    send_outlook_email
)

# Process data by segments
segments = {
    'WGS': 'WGS Market',
    'MED': 'Medicaid',
    'GBD': 'GBD Rates',
    'COM': 'Commercial'
}

segment_data = process_by_segments(df, 'SegmentCode', segments)

# Calculate metrics for each segment
metrics_dict = {}
for code, segment_df in segment_data.items():
    metrics = calculate_advanced_metrics(segment_df, metric_columns)
    metrics_dict[segments[code]] = metrics

# Update Excel
today = datetime.now().strftime('%m/%d/%Y')
update_excel_with_duplicate_check(
    excel_path='data/output/West_Market_Summary.xlsx',
    sheet_name='Summary',
    date_value=today,
    data_row=metrics_dict['WGS Market'].iloc[-1],
    logger=logger
)

# Generate and send email
html_body = generate_html_email_body(metrics_dict, today)
send_outlook_email(
    subject=f'Healthcare Claims Report - {today}',
    html_body=html_body,
    to_list=config['Email']['recipients'],
    attachments=['data/output/West_Market_Summary.xlsx'],
    logger=logger
)
```

---

## ✅ Best Practices Learned

1. **Always check for duplicates** before inserting data into Excel
2. **Use environment variables** for sensitive configuration
3. **Format numbers properly** in HTML tables (commas for thousands)
4. **Calculate grand totals** separately to avoid rounding errors
5. **Log every major operation** for debugging and auditing
6. **Handle file permissions** gracefully (Excel file open errors)
7. **Use conditional email sending** for testing environments
8. **Maintain YTD datasets** for historical analysis

---

## 🔧 Dependencies to Add

```bash
pip install openpyxl pywin32
```

---

## 📝 Next Steps

1. Implement segment-based processing in your pipeline
2. Add Excel update functionality with duplicate checking
3. Create HTML email templates
4. Set up Outlook automation (Windows only)
5. Test with sample data
6. Add comprehensive error handling
7. Create unit tests for each function

---

**Made with Bob** 🤖