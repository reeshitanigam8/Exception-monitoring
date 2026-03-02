# Exception Monitoring Automation - User Guide

This automation monitors Dynatrace exception dumps, updates a production Excel baseline, and sends categorized alerts to Microsoft Teams.

## Project Structure
```text
Exception monitoring/
├── src/
│   └── monitor.py          # Unified monitoring & notification engine
├── data/
│   ├── table-data (2).csv  # Real exception dump (Input)
│   └── PC_Prod_Exception_Monitoring...xlsx # Production Baseline (Excel)
├── templates/
│   └── teams_notification.json # Teams Adaptive Card template
├── config.json             # Global configuration
└── docs/                   # Logs and project documentation
```

## Configuration (`config.json`)
Before running, update `config.json` in the project root:
- `TEAMS_WEBHOOK_URL`: Your Microsoft Teams Incoming Webhook URL.
- `ENABLE_NOTIFICATIONS`: Set to `true` to send real alerts to Teams.
- `DELAY_MINUTES`: Time to wait (e.g., 30) before re-checking trends (Verification stage).
- `INPUT_CSV`: The primary exception dump file.
- `SECOND_INPUT_CSV`: The file used for verification after the delay.

## How to Run
1.  **Preparation**: Download your latest Dynatrace exception dump and save it as `data/table-data (2).csv`.
2.  **Execution**: Run the following command from the project root:
    ```bash
    python src/monitor.py
    ```
3.  **Process**:
    - **Cycle 1**: The script reads `INPUT_CSV` and updates the `Current` sheet.
    - **Immediate Alert**: Any **New** exceptions trigger an immediate alert.
    - **Verification Window**: If **New** or **Elevated** exceptions are found, the script waits for `DELAY_MINUTES`.
    - **Cycle 2**: The script reads `SECOND_INPUT_CSV`. 
    - **Trending Alert**: A second alert is sent if the exception count has **increased** or if **new** exceptions appear in the updated file.

## Troubleshooting
- **Excel Errors**: Ensure the Excel file is closed before running the script (or the script may fail to save).
- **Notification Failures**: Verify your internet connection and the Webhook URL in `config.json`.
- **Missing Sheets**: Ensure your Excel file contains sheets named exactly `Current` and `30Days-Baseline`.
