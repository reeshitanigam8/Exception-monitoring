import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import threading
import sys
import io
from datetime import datetime

# Import monitor logic
import monitor
from monitor import main as run_monitor, load_config

class ExceptionMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exception Monitoring Dashboard")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f2f5")
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f2f5")
        self.style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1a73e8")
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), foreground="white", background="#1a73e8")
        
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
        self.config = load_config()
        
        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_frame, text="Exception Monitoring Automation", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")

        # --- Configuration Section ---
        config_frame = ttk.LabelFrame(main_frame, text=" Configuration Settings ", padding="15")
        config_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 20))

        # Webhook URL
        ttk.Label(config_frame, text="Teams Webhook URL:").grid(row=0, column=0, sticky="w", pady=5)
        self.webhook_var = tk.StringVar()
        self.webhook_entry = ttk.Entry(config_frame, textvariable=self.webhook_var)
        self.webhook_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10)

        # Delay
        ttk.Label(config_frame, text="Delay (Minutes):").grid(row=1, column=0, sticky="w", pady=5)
        self.delay_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.delay_var, width=10).grid(row=1, column=1, sticky="w", padx=10)

        # Flags
        self.notif_var = tk.BooleanVar()
        ttk.Checkbutton(config_frame, text="Enable Notifications", variable=self.notif_var).grid(row=1, column=2, sticky="w")

        self.manual_var = tk.BooleanVar()
        ttk.Checkbutton(config_frame, text="Manual Mode (Wait for CSV downloads)", variable=self.manual_var).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # --- File Selection Section ---
        files_frame = ttk.LabelFrame(main_frame, text=" Data Files ", padding="15")
        files_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 20))

        # Input CSV
        ttk.Label(files_frame, text="Cycle 1 CSV (Input):").grid(row=0, column=0, sticky="w", pady=5)
        self.input_csv_var = tk.StringVar()
        ttk.Entry(files_frame, textvariable=self.input_csv_var).grid(row=0, column=1, sticky="ew", padx=10)
        ttk.Button(files_frame, text="Browse", command=lambda: self.browse_file(self.input_csv_var)).grid(row=0, column=2)

        # Second Input CSV
        ttk.Label(files_frame, text="Cycle 2 CSV (Verify):").grid(row=1, column=0, sticky="w", pady=5)
        self.second_csv_var = tk.StringVar()
        ttk.Entry(files_frame, textvariable=self.second_csv_var).grid(row=1, column=1, sticky="ew", padx=10)
        ttk.Button(files_frame, text="Browse", command=lambda: self.browse_file(self.second_csv_var)).grid(row=1, column=2)

        # Baseline Excel
        ttk.Label(files_frame, text="Baseline Excel:").grid(row=2, column=0, sticky="w", pady=5)
        self.excel_var = tk.StringVar()
        ttk.Entry(files_frame, textvariable=self.excel_var).grid(row=2, column=1, sticky="ew", padx=10)
        ttk.Button(files_frame, text="Browse", command=lambda: self.browse_file(self.excel_var)).grid(row=2, column=2)

        # --- Log Section ---
        log_frame = ttk.LabelFrame(main_frame, text=" Activity Log ", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

        self.log_text = tk.Text(log_frame, height=12, state='disabled', font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4")
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text['yscrollcommand'] = scrollbar.set

        # --- Action Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))

        self.run_btn = ttk.Button(button_frame, text="▶ START MONITORING", command=self.start_monitoring, width=25)
        self.run_btn.pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame, text="💾 SAVE SETTINGS", command=self.save_settings, width=20).pack(side=tk.LEFT, padx=10)

        # Configure layout weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        config_frame.columnconfigure(1, weight=1)
        files_frame.columnconfigure(1, weight=1)

    def load_settings(self):
        self.webhook_var.set(self.config.get("TEAMS_WEBHOOK_URL", ""))
        self.delay_var.set(str(self.config.get("DELAY_MINUTES", 30)))
        self.notif_var.set(self.config.get("ENABLE_NOTIFICATIONS", False))
        self.manual_var.set(self.config.get("MANUAL_MODE", False))
        self.input_csv_var.set(self.config.get("INPUT_CSV", ""))
        self.second_csv_var.set(self.config.get("SECOND_INPUT_CSV", ""))
        self.excel_var.set(self.config.get("BASELINE_EXCEL", ""))

    def save_settings(self):
        try:
            self.config["TEAMS_WEBHOOK_URL"] = self.webhook_var.get()
            self.config["DELAY_MINUTES"] = int(self.delay_var.get())
            self.config["ENABLE_NOTIFICATIONS"] = self.notif_var.get()
            self.config["MANUAL_MODE"] = self.manual_var.get()
            self.config["INPUT_CSV"] = self.input_csv_var.get()
            self.config["SECOND_INPUT_CSV"] = self.second_csv_var.get()
            self.config["BASELINE_EXCEL"] = self.excel_var.get()

            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def browse_file(self, var):
        filename = filedialog.askopenfilename(initialdir="data")
        if filename:
            var.set(os.path.basename(filename))

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()

    def start_monitoring(self):
        self.save_settings()
        self.run_btn.config(state='disabled')
        self.log("--- Starting Monitoring Pipeline ---")
        
        # Run in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.run_pipeline)
        thread.daemon = True
        thread.start()

    def run_pipeline(self):
        # Override monitor's input with a GUI dialog
        def gui_input(prompt):
            self.log(f"PAUSED: {prompt}")
            messagebox.showinfo("Waiting for User", prompt)
            return ""

        monitor.get_user_input = gui_input

        # Redirect stdout to capture print messages from monitor.py
        class RedirectStream:
            def __init__(self, log_func):
                self.log_func = log_func
            def write(self, s):
                if s.strip():
                    self.log_func(s.strip())
            def flush(self):
                pass

        old_stdout = sys.stdout
        sys.stdout = RedirectStream(self.log)
        
        try:
            run_monitor()
        except Exception as e:
            self.log(f"CRITICAL ERROR: {e}")
            messagebox.showerror("Pipeline Error", str(e))
        finally:
            sys.stdout = old_stdout
            self.run_btn.config(state='normal')
            self.log("--- Monitoring Pipeline Finished ---")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExceptionMonitorApp(root)
    root.mainloop()
