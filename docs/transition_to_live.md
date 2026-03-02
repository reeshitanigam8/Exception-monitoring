# Guide: Transitioning to Real Dynatrace Extraction

The current monitoring automation uses a simulated run engine (`simulator.py`) and static CSV files. This guide explains how to transition to live Dynatrace extraction once environment access is granted.

## 1. Replacing Static Inputs
The `load_real_input(filepath)` function in `src/monitor.py` currently reads a CSV file from the `data/` directory. To automate extraction:
- **Direct API Access**: If API access is granted, the `load_real_input` function should be refactored to use `requests` to query the Dynatrace API endpoint (e.g., `/api/v2/metrics/query` or the Notebooks API).
- **Scheduled Exports**: If using manual exports, a script could be written using a browser automation tool (like Selenium or Playwright) to log into Dynatrace, run the "Exception Monitoring Query" notebook, and download the CSV to `data/table-data (2).csv`.

## 2. Removing Simulation Logic
Once live data is flowing:
- **Switch back to `monitor.py`**: The `simulator.py` script is for testing only. The production logic resides in `src/monitor.py`.
- **Enable Notifications**: Set `"ENABLE_NOTIFICATIONS": true` in `config.json` and provide the real `TEAMS_WEBHOOK_URL`.
- **Set Thresholds**: Adjust `DELAY_MINUTES` in `config.json` to the desired verification window (e.g., 30 minutes).

## 3. Workflow Integration
1. **Automation Host**: Deploy the `src/` directory to a server or local machine that can run Python.
2. **Scheduling**: Use a task scheduler (Cron on Linux, Task Scheduler on Windows) to execute `python src/monitor.py` at the required intervals (e.g., every 1 hour, or every 30 minutes during releases).
3. **Log Monitoring**: Monitor the `docs/` folder for logs to ensure the logic remains healthy and the Excel baseline is updating correctly.

---

### Prepared for Real Access
The `TeamsNotifier` and `Parser` logic are already production-ready. The system will immediately begin sending real alerts once the CSV input is replaced by a live data stream.
