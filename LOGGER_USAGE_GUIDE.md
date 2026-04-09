# Logger Module Usage Guide

## Overview

The `logger.py` module provides a centralized, reusable logging system for the Healthcare Claims Auto-Adjudication Pipeline. It enhances the basic Python logging with structured formatting, log rotation, and utility functions.

---

## Key Features

1. **File Logging with Rotation** - Automatically rotates log files when they reach 10MB
2. **Console Output** - Optional console logging for development
3. **Structured Formatting** - Consistent timestamp and level formatting
4. **Utility Functions** - Helper functions for common logging patterns
5. **Section Markers** - Visual separators for major pipeline phases

---

## Basic Usage

### 1. Setup Logger (in main.py)

```python
from logger import setup_logger

# Create logger instance
logger = setup_logger(
    name='pipeline',
    log_file='logs/pipeline.log',
    console_output=True  # Set to False in production
)
```

### 2. Basic Logging

```python
logger.info("Processing started")
logger.warning("Missing optional field")
logger.error("Failed to connect to database")
logger.critical("System shutdown required")
```

---

## Utility Functions

### 1. Section Markers

Use for major pipeline phases:

```python
from logger import log_section_start, log_section_end

log_section_start(logger, "Data Processing")
# ... do work ...
log_section_end(logger, "Data Processing", success=True)
```

**Output:**
```
============================================================
START: Data Processing
============================================================
... processing logs ...
END: Data Processing - SUCCESS
============================================================
```

### 2. DataFrame Information

Log pandas DataFrame details:

```python
from logger import log_dataframe_info

log_dataframe_info(logger, df, "Customer Data")
```

**Output:**
```
Customer Data - Shape: (1000, 15), Columns: ['id', 'name', 'email', ...]
Customer Data - Memory usage: 234.56 KB
```

### 3. Metrics Logging

Log structured metrics:

```python
from logger import log_metrics

metrics = {
    'total_records': 1000,
    'processed': 950,
    'errors': 50
}
log_metrics(logger, metrics, prefix='Daily Run')
```

**Output:**
```
Metrics - Daily Run:
  total_records: 1000
  processed: 950
  errors: 50
```

### 4. Error Logging with Context

Enhanced error logging:

```python
from logger import log_error_with_context

try:
    # ... code that might fail ...
except Exception as e:
    log_error_with_context(logger, e, "Failed during data merge")
    raise
```

**Output:**
```
Failed during data merge - Error: ValueError: Invalid column name
[Full stack trace included]
```

---

## Configuration Options

### setup_logger() Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | 'pipeline' | Logger name (use different names for different modules) |
| `log_file` | str | 'logs/pipeline.log' | Path to log file |
| `level` | int | logging.INFO | Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `console_output` | bool | True | Enable/disable console output |
| `max_bytes` | int | 10485760 | Max file size before rotation (10MB default) |
| `backup_count` | int | 5 | Number of backup files to keep |

---

## Integration Example

### Before (Old Approach)

```python
import logging

logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_data():
    logging.info("Starting data processing")
    try:
        # ... code ...
        logging.info("Processing complete")
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
```

### After (New Approach)

```python
from logger import setup_logger, log_section_start, log_section_end, log_error_with_context

logger = setup_logger(name='pipeline', log_file='logs/pipeline.log')

def process_data(logger):
    log_section_start(logger, "Data Processing")
    try:
        # ... code ...
        log_section_end(logger, "Data Processing", success=True)
    except Exception as e:
        log_error_with_context(logger, e, "Data processing failed")
        log_section_end(logger, "Data Processing", success=False)
        raise
```

---

## Best Practices

### 1. Pass Logger as Parameter

✅ **Good:**
```python
def process_data(config, logger):
    logger.info("Processing started")
```

❌ **Avoid:**
```python
def process_data(config):
    import logging
    logging.info("Processing started")  # Uses root logger
```

### 2. Use Appropriate Log Levels

- **DEBUG**: Detailed diagnostic information (not in production)
- **INFO**: General informational messages (normal operation)
- **WARNING**: Something unexpected but not critical
- **ERROR**: Error occurred but program continues
- **CRITICAL**: Serious error, program may not continue

### 3. Log at Key Points

```python
def process_claims(data, logger):
    log_section_start(logger, "Claims Processing")
    
    logger.info(f"Processing {len(data)} claims")
    
    # Log before expensive operations
    logger.info("Starting validation...")
    validated = validate_claims(data)
    logger.info(f"Validated {len(validated)} claims")
    
    # Log metrics
    metrics = calculate_metrics(validated)
    log_metrics(logger, metrics, prefix="Claims")
    
    log_section_end(logger, "Claims Processing", success=True)
```

### 4. Use Context in Error Logging

```python
try:
    df = pd.read_csv(file_path)
except FileNotFoundError as e:
    log_error_with_context(logger, e, f"Cannot find file: {file_path}")
    raise
```

---

## Log File Management

### Automatic Rotation

The logger automatically rotates files when they reach 10MB:

```
logs/
├── pipeline.log          # Current log
├── pipeline.log.1        # Previous rotation
├── pipeline.log.2        # Older rotation
├── pipeline.log.3
├── pipeline.log.4
└── pipeline.log.5        # Oldest (will be deleted on next rotation)
```

### Manual Cleanup

To clean old logs:

```python
import os
import glob

# Remove logs older than 30 days
log_files = glob.glob('logs/*.log.*')
for log_file in log_files:
    if os.path.getmtime(log_file) < time.time() - 30*86400:
        os.remove(log_file)
```

---

## Testing the Logger

Run the logger module directly to test:

```bash
python logger.py
```

This will create a test log file at `logs/test.log` with sample output.

---

## Troubleshooting

### Issue: Logs not appearing

**Solution:** Check if logs directory exists and has write permissions

```python
import os
os.makedirs('logs', exist_ok=True)
```

### Issue: Duplicate log entries

**Solution:** Logger handlers are being added multiple times. The module prevents this, but if you see duplicates:

```python
# Clear existing handlers
logger.handlers.clear()
logger = setup_logger(...)
```

### Issue: Console output too verbose

**Solution:** Disable console output in production:

```python
logger = setup_logger(
    name='pipeline',
    log_file='logs/pipeline.log',
    console_output=False  # Disable console
)
```

---

## Migration Checklist

When migrating existing code to use the new logger:

- [ ] Import logger utilities at top of file
- [ ] Replace `logging.basicConfig()` with `setup_logger()`
- [ ] Add `logger` parameter to all functions that log
- [ ] Replace `logging.info()` with `logger.info()`
- [ ] Add section markers for major phases
- [ ] Use `log_error_with_context()` for exceptions
- [ ] Use `log_metrics()` for structured data
- [ ] Test with both console and file output
- [ ] Verify log rotation works

---

## Summary

The logger module provides:

✅ Centralized logging configuration  
✅ Automatic log rotation  
✅ Structured formatting  
✅ Utility functions for common patterns  
✅ Better error context  
✅ Visual section separators  
✅ DataFrame inspection helpers  

This makes logs more readable, maintainable, and useful for debugging and monitoring.