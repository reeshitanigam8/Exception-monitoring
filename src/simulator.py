import json
import csv
import os
import time
from datetime import datetime
from monitor import TeamsNotifier, load_config, load_real_input, update_excel_workbook, load_baseline_from_excel

def run_simulation():
    # 1. Setup
    config = load_config()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, config.get("DATA_DIR", "data"))
    docs_dir = os.path.join(project_root, "docs")
    
    # Files
    run1_csv = os.path.join(data_dir, "table-data (2).csv")
    run2_csv = os.path.join(data_dir, "table-data (2) - run2.csv")
    workbook_file = os.path.join(data_dir, "PC_Prod_Exception_Monitoring_R02_2026-DT 2_SIM.xlsx")
    
    # Initialize Notifier (Force simulation mode for safety, but use existing template logic)
    notifier = TeamsNotifier(config.get("TEAMS_WEBHOOK_URL"), enabled=True) # Always enabled for simulation output
    # Overwrite webhook to ensure no real messages are sent during pure simulation unless explicitly configured
    if config.get("ENABLE_NOTIFICATIONS") is not True:
        notifier.webhook_url = None 
    
    print("=== [SIMULATION] Starting End-to-End Execution Pipeline ===")
    
    # --- RUN 1 ---
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] --- CYCLE 1 (Input: Run 1 CSV) ---")
    run1_data = load_real_input(run1_csv)
    baseline = load_baseline_from_excel(workbook_file)
    
    run1_findings = {"New": [], "Elevated": [], "Ok": []}
    alert_log = []

    for entry in run1_data:
        name, count = entry['name'], entry['count']
        base_count = baseline.get(name)
        
        if base_count is None:
            # New in Run 1
            run1_findings["New"].append({"name": name, "count": count, "baseline": 0})
            print(f"[NEW ALERT] {name[:50]}...")
            notifier.send_alert(name, count, 0, "New", category="New")
            alert_log.append({"cycle": 1, "status": "New", "exception": name, "count": count})
        elif count > base_count:
            run1_findings["Elevated"].append({"name": name, "count": count, "baseline": base_count})
        else:
            run1_findings["Ok"].append({"name": name, "count": count, "baseline": base_count})
            
    # Save Run 1 JSON Log
    with open(os.path.join(docs_dir, "run1_results.json"), "w") as f:
        json.dump(run1_findings, f, indent=4)
    print(f"Cycle 1 Complete. Logged to docs/run1_results.json")

    # --- WAIT (Simulated) ---
    print(f"\n[WAITING] Simulated 30-minute verification window...")
    time.sleep(2)

    # --- RUN 2 ---
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] --- CYCLE 2 (Input: Run 2 CSV) ---")
    run2_data = load_real_input(run2_csv)
    # Update Excel with Run 2 data (as it would be the 'latest' source of truth)
    update_excel_workbook(workbook_file, run2_data)
    
    run2_findings = {"New": [], "Elevated": [], "Ok": []}
    
    # Create lookup for Run 1 counts to detect rising trends
    run1_counts = {e['name']: e['count'] for e in run1_findings["Elevated"]}

    for entry in run2_data:
        name, count = entry['name'], entry['count']
        base_count = baseline.get(name)
        
        if base_count is None:
            # Check if it was already New in Run 1
            if not any(e['name'] == name for e in run1_findings["New"]):
                run2_findings["New"].append({"name": name, "count": count, "baseline": 0})
                print(f"[NEW ALERT] {name[:50]}...")
                notifier.send_alert(name, count, 0, "New", category="New")
                alert_log.append({"cycle": 2, "status": "New", "exception": name, "count": count})
            else:
                run2_findings["Ok"].append({"name": name, "count": count, "baseline": 0}) # Still there, but alert already sent
        elif count > base_count:
            run2_findings["Elevated"].append({"name": name, "count": count, "baseline": base_count})
            # TREND LOGIC: If count increased vs Run 1
            if name in run1_counts:
                if count > run1_counts[name]:
                    print(f"[ELEVATED ALERT] Rising Trend Confirmed: {name[:50]}... ({run1_counts[name]} -> {count})")
                    notifier.send_alert(name, count, base_count, "Elevated", category="Elevated")
                    alert_log.append({"cycle": 2, "status": "Elevated", "exception": name, "count": count, "previous": run1_counts[name]})
                else:
                    print(f"[STABILIZED] {name[:50]}... ({run1_counts[name]} -> {count})")
        else:
            run2_findings["Ok"].append({"name": name, "count": count, "baseline": base_count})

    # Save Run 2 JSON Log
    with open(os.path.join(docs_dir, "run2_results.json"), "w") as f:
        json.dump(run2_findings, f, indent=4)
    print(f"Cycle 2 Complete. Logged to docs/run2_results.json")

    # --- DIFF REPORT ---
    print(f"\n--- TRENDING REPORT ---")
    with open(os.path.join(docs_dir, "trending_report.md"), "w") as f:
        f.write("# Trending Report (Simulated Run)\n\n")
        f.write(f"**Execution Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Alerts Triggered\n")
        if not alert_log:
            f.write("No alerts triggered.\n")
        else:
            f.write("| Cycle | Status | Exception Fragment | Count | Delta/Previous |\n")
            f.write("|---|---|---|---|---|\n")
            for alert in alert_log:
                name_frag = alert['exception'][:60].replace('|', '\\|')
                delta = f"vs {alert['previous']}" if 'previous' in alert else "N/A"
                f.write(f"| {alert['cycle']} | {alert['status']} | {name_frag}... | {alert['count']} | {delta} |\n")
        
    print(f"Diff report generated: docs/trending_report.md")
    print("\n=== SIMULATION COMPLETE ===")

if __name__ == "__main__":
    run_simulation()
