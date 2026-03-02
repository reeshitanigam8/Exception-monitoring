# Production Setup & Configuration Guide

This guide provides step-by-step instructions on how to obtain the real-world configurations and data required to run the Exception Monitoring automation.

---

## 1. Dynatrace Exception Data (Input CSV)
To get the latest exception dump:
1.  **Log in** to your Dynatrace environment.
2.  Navigate to **Notebooks**.
3.  Open the **Release Monitoring** notebook (or your custom Exception Monitoring notebook).
4.  Locate the section containing the **Exception Monitoring Query**.
5.  **Run the query** for the desired time frame (e.g., last 1 hour or last 24 hours).
6.  Click the **Download/Export** icon and select **Export as CSV**.
7.  Rename the downloaded file to `table-data (2).csv` (or update the filename in `config.json`) and place it in the `data/` folder.

---

## 2. Microsoft Teams Webhook (Alert Notifications)
To enable real-time alerts in your Teams channel:
1.  Open **Microsoft Teams** and go to the channel where you want to receive alerts.
2.  Click the **three dots (...)** next to the channel name and select **Connectors**.
3.  Search for **Incoming Webhook** and click **Add**.
4.  Provide a name (e.g., "Exception Monitor") and click **Create**.
5.  **Copy the Webhook URL** provided.
6.  Open `config.json` in the project root and paste the URL into the `TEAMS_WEBHOOK_URL` field.
7.  Set `ENABLE_NOTIFICATIONS` to `true`.

---

## 3. Production Baseline Excel
The automation depends on an Excel workbook used for tracking:
1.  Ensure you have the file named `PC_Prod_Exception_Monitoring_R02_2026-DT 2.xlsx` in the `data/` folder.
2.  **Required Sheets**:
    - **`Current`**: This sheet must exist; it will be automatically overwritten by the script.
    - **`30Days-Baseline`**: This sheet must contain your baseline data in Column A (Exception Name) and Column B (Count/Average).
3.  **Permissions**: Ensure the file is not currently open in Excel when you run the script, as this may prevent the automation from saving updates.

---

## 4. Configuration File (`config.json`)
The `config.json` file in the project root should look like this once configured:

```json
{
    "TEAMS_WEBHOOK_URL": "https://outlook.office.com/webhook/...",
    "ENABLE_NOTIFICATIONS": true,
    "DELAY_MINUTES": 30,
    "DATA_DIR": "data",
    "TEMPLATES_DIR": "templates",
    "INPUT_CSV": "table-data (2).csv",
    "BASELINE_EXCEL": "PC_Prod_Exception_Monitoring_R02_2026-DT 2.xlsx"
}
```

- **`DELAY_MINUTES`**: This is the time the script waits before re-checking "Elevated" exceptions to confirm a rising trend.
