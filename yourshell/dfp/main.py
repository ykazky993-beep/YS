import tkinter as tk
import customtkinter as ctk
import requests
import time
import threading
import subprocess
import platform
import json
from datetime import datetime
from urllib.parse import urlparse  

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class HTTPDetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🔍 Advanced HTTP & Network Toolkit")
        self.geometry("950://800")
        self.geometry("950x800")
        self.minsize(850, 650)

        self.is_looping = False

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. Header Title
        self.header_label = ctk.CTkLabel(
            self, text="⚡ Network & HTTP Request Toolkit",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # 2. Input Konfig
        self.create_config_frame()

        # 2b. Info URL
        self.create_info_frame()

        # 3. Control Buttons
        self.create_control_frame()

        # 4. Area Output/Response
        self.create_output_frame()

    def create_config_frame(self):
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.config_frame.grid_columnconfigure(1, weight=1)

        # Input URL
        self.url_label = ctk.CTkLabel(self.config_frame, text="URL / IP Target:", font=ctk.CTkFont(weight="bold"))
        self.url_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.url_input = ctk.CTkEntry(self.config_frame, placeholder_text="https://httpbin.org/anything atau google.com")
        self.url_input.grid(row=0, column=1, columnspan=3, padx=15, pady=10, sticky="ew")
        self.url_input.insert(0, "https://httpbin.org/anything")

        # Input Loop Interval & Timeout
        self.interval_label = ctk.CTkLabel(self.config_frame, text="Loop Interval (sec):")
        self.interval_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")

        self.interval_input = ctk.CTkEntry(self.config_frame, width=80)
        self.interval_input.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.interval_input.insert(0, "1")

        self.timeout_label = ctk.CTkLabel(self.config_frame, text="Timeout (sec):")
        self.timeout_label.grid(row=1, column=2, padx=15, pady=5, sticky="w")

        self.timeout_input = ctk.CTkEntry(self.config_frame, width=80)
        self.timeout_input.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.timeout_input.insert(0, "5")

    def create_info_frame(self):
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        for i in range(4):
            self.info_frame.grid_columnconfigure(i, weight=1)

        self.lbl_proto = ctk.CTkLabel(self.info_frame, text="Protocol: -", font=ctk.CTkFont(size=11), text_color="#A0A0A0")
        self.lbl_proto.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.lbl_host = ctk.CTkLabel(self.info_frame, text="Host: -", font=ctk.CTkFont(size=11), text_color="#A0A0A0")
        self.lbl_host.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.lbl_port = ctk.CTkLabel(self.info_frame, text="Port: -", font=ctk.CTkFont(size=11), text_color="#A0A0A0")
        self.lbl_port.grid(row=0, column=2, padx=5, pady=2, sticky="w")

        self.lbl_path = ctk.CTkLabel(self.info_frame, text="Path: -", font=ctk.CTkFont(size=11), text_color="#A0A0A0")
        self.lbl_path.grid(row=0, column=3, padx=5, pady=2, sticky="w")

    def create_control_frame(self):
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        for i in range(5):
            self.control_frame.grid_columnconfigure(i, weight=1)

        # HTTP Methods (Single Request)
        self.btn_get = ctk.CTkButton(self.control_frame, text="GET", fg_color="#4CAF50", hover_color="#388E3C", command=lambda: self.start_request_thread("GET"))
        self.btn_get.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.btn_post = ctk.CTkButton(self.control_frame, text="POST", fg_color="#2196F3", hover_color="#1976D2", command=lambda: self.start_request_thread("POST"))
        self.btn_post.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.btn_put = ctk.CTkButton(self.control_frame, text="PUT", fg_color="#FF9800", hover_color="#F57C00", command=lambda: self.start_request_thread("PUT"))
        self.btn_put.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        self.btn_delete = ctk.CTkButton(self.control_frame, text="DELETE", fg_color="#f44336", hover_color="#d32f2f", command=lambda: self.start_request_thread("DELETE"))
        self.btn_delete.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        # Spesial: Ping
        self.btn_ping = ctk.CTkButton(self.control_frame, text="⚡ PING IP", fg_color="#795548", hover_color="#5D4037", command=self.start_ping_thread)
        self.btn_ping.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        # Loop Monitoring
        self.loop_method_var = ctk.StringVar(value="GET")
        self.dropdown_loop = ctk.CTkOptionMenu(self.control_frame, values=["GET", "POST", "PUT", "DELETE"], variable=self.loop_method_var, fg_color="#9C27B0", button_color="#7B1FA2")
        self.dropdown_loop.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.btn_loop_http = ctk.CTkButton(self.control_frame, text="🔄 Loop HTTP", fg_color="#9C27B0", hover_color="#7B1FA2", command=self.toggle_loop_http)
        self.btn_loop_http.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.btn_loop_ping = ctk.CTkButton(self.control_frame, text="🔄 Loop PING", fg_color="#E91E63", hover_color="#C2185B", command=self.toggle_loop_ping)
        self.btn_loop_ping.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        self.lbl_status = ctk.CTkLabel(self.control_frame, text="Status: Ready", text_color="gray")
        self.lbl_status.grid(row=1, column=4, padx=5, pady=5, sticky="w")

    def create_output_frame(self):
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=1)

        self.output_label = ctk.CTkLabel(self.output_frame, text="📥 Console Output / Response Logs:", font=ctk.CTkFont(weight="bold"))
        self.output_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")

        self.txt_output = ctk.CTkTextbox(self.output_frame, font=ctk.CTkFont(family="Courier New", size=12))
        self.txt_output.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
        self.txt_output.insert("0.0", "App ready. Enter URL and select test method above.\n" + "-"*60 + "\n")

    def update_url_info(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            parsed_url = urlparse(f"http://{url}")
        else:
            parsed_url = urlparse(url)
        
        protocol = parsed_url.scheme.upper() if parsed_url.scheme else "HTTP (ASSUMED)"
        host = parsed_url.hostname if parsed_url.hostname else "Unknown"
        port = parsed_url.port if parsed_url.port else ("443" if parsed_url.scheme == "https" else "80")
        path = parsed_url.path if parsed_url.path else "/"

        self.lbl_proto.configure(text=f"Protocol: {protocol}")
        self.lbl_host.configure(text=f"Host: {host}")
        self.lbl_port.configure(text=f"Port: {port}")
        self.lbl_path.configure(text=f"Path: {path}")

    def log(self, message):
        self.txt_output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.txt_output.see(tk.END)

    def clean_url_for_ping(self, url):
        cleaned = url.replace("https://", "").replace("http://", "")
        return cleaned.split("/")[0].split(":")[0]

    def start_request_thread(self, method):
        url = self.url_input.get()
        self.update_url_info(url) # info web
        timeout = int(self.timeout_input.get() or 5)
        threading.Thread(target=self.execute_http_request, args=(method, url, timeout), daemon=True).start()

    def execute_http_request(self, method, url, timeout, silently=False):
        if not silently:
            self.lbl_status.configure(text=f"Sending {method}...", text_color="#2196F3")

        payload = {"source": "Python HTTP Detector", "timestamp": datetime.now().isoformat()} if method in ["POST", "PUT", "DELETE", "PATCH"] else None
        start_time = time.time()

        try:
            res = requests.request(method, url, json=payload, timeout=timeout)
            duration = int((time.time() - start_time) * 1000)

            output_msg = f"✓ {method} Success ({duration}ms) | Status: {res.status_code}\n"
            try:
                output_msg += json.dumps(res.json(), indent=2)
            except:
                output_msg += res.text[:500] + "\n[Output cut...]"

            self.log(output_msg + f"\n{'-'*60}")
            return True
        except Exception as e:
            self.log(f"✗ {method} Error: {str(e)}\n{'-'*60}")
            return False
        finally:
            if not silently:
                self.lbl_status.configure(text="Status: Ready", text_color="gray")

    def start_ping_thread(self):
        url = self.url_input.get()
        self.update_url_info(url)
        target = self.clean_url_for_ping(url)
        threading.Thread(target=self.execute_ping, args=(target,), daemon=True).start()

    def execute_ping(self, target, silently=False):
        if not silently:
            self.lbl_status.configure(text="Pinging...", text_color="#795548")
            self.log(f"Pinging target Host: {target}")

        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', target]

        try:
            output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            if output.returncode == 0:
                self.log(f"✓ PING Success to {target}\n{output.stdout.strip()}\n{'-'*60}")
                return True
            else:
                self.log(f"✗ PING Failed to {target}\n{output.stderr.strip()}\n{'-'*60}")
                return False
        except Exception as e:
            self.log(f"✗ PING System Error: {str(e)}\n{'-'*60}")
            return False
        finally:
            if not silently:
                self.lbl_status.configure(text="Status: Ready", text_color="gray")

    def toggle_loop_http(self):
        if self.is_looping:
            self.stop_loop()
        else:
            self.is_looping = True
            method = self.loop_method_var.get()
            self.btn_loop_http.configure(text="🛑 STOP LOOP", fg_color="#f44336")
            self.dropdown_loop.configure(state="disabled")
            self.btn_loop_ping.configure(state="disabled")
            self.lbl_status.configure(text=f"Looping {method}...", text_color="#9C27B0")
            threading.Thread(target=self.loop_worker, args=(method,), daemon=True).start()

    def toggle_loop_ping(self):
        if self.is_looping:
            self.stop_loop()
        else:
            self.is_looping = True
            self.btn_loop_ping.configure(text="🛑 STOP LOOP", fg_color="#f44336")
            self.dropdown_loop.configure(state="disabled")
            self.btn_loop_http.configure(state="disabled")
            self.lbl_status.configure(text="Looping Ping...", text_color="#E91E63")
            threading.Thread(target=self.loop_worker, args=("PING",), daemon=True).start()

    def stop_loop(self):
        self.is_looping = False
        self.btn_loop_http.configure(text="🔄 Loop HTTP", fg_color="#9C27B0", state="normal")
        self.btn_loop_ping.configure(text="🔄 Loop PING", fg_color="#E91E63", state="normal")
        self.dropdown_loop.configure(state="normal")
        self.lbl_status.configure(text="Status: Ready", text_color="gray")
        self.log(f"🛑 Loop monitoring stoped by user.\n{'-'*60}")

    def loop_worker(self, mode):
        url = self.url_input.get()
        self.update_url_info(url) # info web
        target_host = self.clean_url_for_ping(url)

        try:
            interval = max(0.5, float(self.interval_input.get() or 1))
            timeout = int(self.timeout_input.get() or 5)
        except ValueError:
            self.log("System Error: Interval/Timeout!")
            self.stop_loop()
            return

        self.log(f"▶️ Start Loop {mode} Monitoring every {interval} sec to target {url}.")

        while self.is_looping:
            if mode in ["GET", "POST", "PUT", "DELETE"]:
                success = self.execute_http_request(mode, url, timeout, silently=True)
            else:
                success = self.execute_command_ping_status(target_host)

            if not success:
                self.log("🚨 [ALERT] TARGET NOT RESPONDING / DOWN!")

            time.sleep(interval)

    def execute_command_ping_status(self, target):
        param = '-n' if platform.system().lower()=='windows' else '-c'
        try:
            res = subprocess.run(['ping', param, '1', target], stdout=subprocess.PIPE, text=True, timeout=2)
            if res.returncode == 0:
                self.log(f"🟢 [PING UP] Connected to {target}")
                return True
            else:
                self.log(f"🔴 [PING DOWN] Failed to connect to {target}")
                return False
        except:
            self.log(f"🔴 [PING DOWN] Timeout/Error to {target}")
            return False

if __name__ == "__main__":
    app = HTTPDetectorApp()
    app.mainloop()
