import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import requests
import time
import threading
import subprocess
import platform
import json
import socket
from datetime import datetime
from urllib.parse import urlparse

# Set tema dan warna dasar UI
ctk.set_appearance_mode("Dark")  # Mode gelap lebih terlihat profesional
ctk.set_default_color_theme("blue")

class HTTPDetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🔍 Advanced Network & HTTP Toolkit Pro")
        self.geometry("1000x850")
        self.minsize(900, 700)

        # Variabel Kontrol
        self.is_looping = False

        # --- Layout Utama ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1) 

        self.create_header()
        self.create_config_frame()
        self.create_info_frame()
        self.create_control_frame()
        self.create_tabview_area()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            header_frame, text="⚡ Network & HTTP Request Toolkit Pro",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, sticky="w")

        # Utility Buttons
        self.btn_clear = ctk.CTkButton(header_frame, text="🗑️ Clear Logs", width=100, command=self.clear_logs)
        self.btn_clear.grid(row=0, column=1, padx=5)

        self.btn_save = ctk.CTkButton(header_frame, text="💾 Save Logs", width=100, command=self.save_logs)
        self.btn_save.grid(row=0, column=2, padx=5)

    def create_config_frame(self):
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.config_frame.grid_columnconfigure(1, weight=1)

        self.url_label = ctk.CTkLabel(self.config_frame, text="URL / IP Target:", font=ctk.CTkFont(weight="bold"))
        self.url_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.url_input = ctk.CTkEntry(self.config_frame, placeholder_text="https://httpbin.org/anything")
        self.url_input.grid(row=0, column=1, columnspan=3, padx=15, pady=10, sticky="ew")
        self.url_input.insert(0, "https://httpbin.org/anything")

        self.interval_label = ctk.CTkLabel(self.config_frame, text="Loop Interval (s):")
        self.interval_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.interval_input = ctk.CTkEntry(self.config_frame, width=80)
        self.interval_input.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.interval_input.insert(0, "1")

        self.timeout_label = ctk.CTkLabel(self.config_frame, text="Timeout (s):")
        self.timeout_label.grid(row=1, column=2, padx=15, pady=5, sticky="e")
        self.timeout_input = ctk.CTkEntry(self.config_frame, width=80)
        self.timeout_input.grid(row=1, column=3, padx=15, pady=5, sticky="e")
        self.timeout_input.insert(0, "5")

    def create_info_frame(self):
        self.info_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.info_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        for i in range(5):
            self.info_frame.grid_columnconfigure(i, weight=1)

        font_info = ctk.CTkFont(size=12, weight="bold")
        self.lbl_proto = ctk.CTkLabel(self.info_frame, text="Protocol: -", font=font_info, text_color="#4CAF50")
        self.lbl_proto.grid(row=0, column=0, padx=5, pady=5)

        self.lbl_host = ctk.CTkLabel(self.info_frame, text="Host: -", font=font_info, text_color="#2196F3")
        self.lbl_host.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_ip = ctk.CTkLabel(self.info_frame, text="IP: -", font=font_info, text_color="#FF9800")
        self.lbl_ip.grid(row=0, column=2, padx=5, pady=5)

        self.lbl_port = ctk.CTkLabel(self.info_frame, text="Port: -", font=font_info, text_color="#9C27B0")
        self.lbl_port.grid(row=0, column=3, padx=5, pady=5)

        self.lbl_path = ctk.CTkLabel(self.info_frame, text="Path: -", font=font_info, text_color="#E91E63")
        self.lbl_path.grid(row=0, column=4, padx=5, pady=5)

    def create_control_frame(self):
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        for i in range(5):
            self.control_frame.grid_columnconfigure(i, weight=1)

        # Baris 1: Manual Requests
        self.btn_get = ctk.CTkButton(self.control_frame, text="GET", fg_color="#4CAF50", hover_color="#388E3C", command=lambda: self.start_request_thread("GET"))
        self.btn_get.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.btn_post = ctk.CTkButton(self.control_frame, text="POST", fg_color="#2196F3", hover_color="#1976D2", command=lambda: self.start_request_thread("POST"))
        self.btn_post.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.btn_put = ctk.CTkButton(self.control_frame, text="PUT", fg_color="#FF9800", hover_color="#F57C00", command=lambda: self.start_request_thread("PUT"))
        self.btn_put.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        self.btn_delete = ctk.CTkButton(self.control_frame, text="DELETE", fg_color="#f44336", hover_color="#d32f2f", command=lambda: self.start_request_thread("DELETE"))
        self.btn_delete.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        self.btn_ping = ctk.CTkButton(self.control_frame, text="⚡ PING IP", fg_color="#795548", hover_color="#5D4037", command=self.start_ping_thread)
        self.btn_ping.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        # Baris 2: Looping & Monitoring
        self.loop_method_var = ctk.StringVar(value="GET")
        self.dropdown_loop = ctk.CTkOptionMenu(self.control_frame, values=["GET", "POST", "PUT", "DELETE"], variable=self.loop_method_var)
        self.dropdown_loop.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.btn_loop_http = ctk.CTkButton(self.control_frame, text="🔄 Loop HTTP", fg_color="#9C27B0", hover_color="#7B1FA2", command=self.toggle_loop_http)
        self.btn_loop_http.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.btn_loop_ping = ctk.CTkButton(self.control_frame, text="🔄 Loop PING", fg_color="#E91E63", hover_color="#C2185B", command=self.toggle_loop_ping)
        self.btn_loop_ping.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        self.lbl_status = ctk.CTkLabel(self.control_frame, text="Status: Ready", text_color="gray", font=ctk.CTkFont(weight="bold"))
        self.lbl_status.grid(row=1, column=4, padx=5, pady=5, sticky="w")

    def create_tabview_area(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="nsew")

        self.tab_console = self.tabview.add("Console Logs")
        self.tab_payload = self.tabview.add("Custom Payload (JSON)")

        # Tab Console
        self.tab_console.grid_columnconfigure(0, weight=1)
        self.tab_console.grid_rowconfigure(0, weight=1)
        self.txt_output = ctk.CTkTextbox(self.tab_console, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#1e1e1e", text_color="#00FF00")
        self.txt_output.grid(row=0, column=0, sticky="nsew")
        self.txt_output.insert("0.0", "Aplikasi siap. Masukkan URL lalu pilih metode pengujian di atas.\n" + "="*80 + "\n")

        # Tab Payload
        self.tab_payload.grid_columnconfigure(0, weight=1)
        self.tab_payload.grid_rowconfigure(1, weight=1)
        self.lbl_payload = ctk.CTkLabel(self.tab_payload, text="Masukkan JSON Payload untuk POST/PUT requests:")
        self.lbl_payload.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.txt_payload = ctk.CTkTextbox(self.tab_payload, font=ctk.CTkFont(family="Consolas", size=13))
        self.txt_payload.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        default_payload = '{\n  "title": "foo",\n  "body": "bar",\n  "userId": 1\n}'
        self.txt_payload.insert("0.0", default_payload)

    # --- Utility Functions ---
    def safe_ui_update(self, func, *args, **kwargs):
        """Mengeksekusi update UI secara aman dari thread lain"""
        self.after(0, lambda: func(*args, **kwargs))

    def log(self, message):
        """Menambahkan log ke console secara aman"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        def append_text():
            self.txt_output.insert(tk.END, f"[{timestamp}] {message}\n")
            self.txt_output.see(tk.END)
        self.safe_ui_update(append_text)

    def clear_logs(self):
        self.txt_output.delete("1.0", tk.END)
        self.log("Console dibersihkan.\n" + "="*80)

    def save_logs(self):
        logs = self.txt_output.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(logs)
            messagebox.showinfo("Success", "Logs berhasil disimpan!")

    def update_url_info(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            parsed_url = urlparse(f"http://{url}")
        else:
            parsed_url = urlparse(url)

        protocol = parsed_url.scheme.upper() if parsed_url.scheme else "HTTP"
        host = parsed_url.hostname if parsed_url.hostname else "Unknown"
        port = parsed_url.port if parsed_url.port else ("443" if protocol == "HTTPS" else "80")
        path = parsed_url.path if parsed_url.path else "/"

        # Resolve DNS
        resolved_ip = "Resolving..."
        try:
            resolved_ip = socket.gethostbyname(host) if host != "Unknown" else "-"
        except socket.gaierror:
            resolved_ip = "Unresolved"

        self.safe_ui_update(lambda: self.lbl_proto.configure(text=f"Proto: {protocol}"))
        self.safe_ui_update(lambda: self.lbl_host.configure(text=f"Host: {host}"))
        self.safe_ui_update(lambda: self.lbl_ip.configure(text=f"IP: {resolved_ip}"))
        self.safe_ui_update(lambda: self.lbl_port.configure(text=f"Port: {port}"))
        self.safe_ui_update(lambda: self.lbl_path.configure(text=f"Path: {path}"))

    def clean_url_for_ping(self, url):
        cleaned = url.replace("https://", "").replace("http://", "")
        return cleaned.split("/")[0].split(":")[0]

    # --- Core Execution Logic ---
    def start_request_thread(self, method):
        url = self.url_input.get()
        timeout = int(self.timeout_input.get() or 5)
        
        # Ambil custom payload dari tab jika metodenya POST/PUT
        payload_data = None
        if method in ["POST", "PUT", "PATCH"]:
            try:
                raw_payload = self.txt_payload.get("1.0", tk.END).strip()
                if raw_payload:
                    payload_data = json.loads(raw_payload)
            except json.JSONDecodeError:
                messagebox.showerror("Format Error", "JSON Payload tidak valid! Pastikan formatnya benar.")
                return

        threading.Thread(target=self.execute_http_request, args=(method, url, timeout, payload_data), daemon=True).start()

    def execute_http_request(self, method, url, timeout, payload=None, silently=False):
        self.update_url_info(url)
        if not silently:
            self.safe_ui_update(lambda: self.lbl_status.configure(text=f"Sending {method}...", text_color="#2196F3"))

        start_time = time.time()
        try:
            res = requests.request(method, url, json=payload, timeout=timeout)
            duration = int((time.time() - start_time) * 1000)

            status_icon = "🟢" if 200 <= res.status_code < 300 else "🟡" if 300 <= res.status_code < 400 else "🔴"
            output_msg = f"{status_icon} {method} Success ({duration}ms) | Status: {res.status_code} {res.reason}\n"
            
            try:
                output_msg += json.dumps(res.json(), indent=2)
            except:
                output_msg += res.text[:500] + ("\n[Output dipotong...]" if len(res.text) > 500 else "")

            self.log(output_msg + f"\n{'-'*80}")
            return True
        except Exception as e:
            self.log(f"🔴 {method} Error: {str(e)}\n{'-'*80}")
            return False
        finally:
            if not silently:
                self.safe_ui_update(lambda: self.lbl_status.configure(text="Status: Ready", text_color="gray"))

    def start_ping_thread(self):
        url = self.url_input.get()
        target = self.clean_url_for_ping(url)
        threading.Thread(target=self.execute_ping, args=(target,), daemon=True).start()

    def execute_ping(self, target, silently=False):
        self.update_url_info(target)
        if not silently:
            self.safe_ui_update(lambda: self.lbl_status.configure(text="Pinging...", text_color="#795548"))
            self.log(f"⚡ Pinging target Host: {target}")

        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', target]

        try:
            # Gunakan creationflags untuk hide console window di Windows saat ping berjalan
            creation_flags = subprocess.CREATE_NO_WINDOW if platform.system().lower()=='windows' else 0
            output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5, creationflags=creation_flags)
            
            if output.returncode == 0:
                self.log(f"🟢 PING Success to {target}\n{output.stdout.strip()}\n{'-'*80}")
                return True
            else:
                self.log(f"🔴 PING Failed to {target}\n{output.stderr.strip()}\n{'-'*80}")
                return False
        except Exception as e:
            self.log(f"🔴 PING System Error: {str(e)}\n{'-'*80}")
            return False
        finally:
            if not silently:
                self.safe_ui_update(lambda: self.lbl_status.configure(text="Status: Ready", text_color="gray"))

    # --- Loop Monitoring ---
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
        self.log(f"🛑 Loop monitoring dihentikan oleh pengguna.\n{'-'*80}")

    def loop_worker(self, mode):
        url = self.url_input.get()
        target_host = self.clean_url_for_ping(url)

        try:
            interval = max(0.5, float(self.interval_input.get() or 1))
            timeout = int(self.timeout_input.get() or 5)
        except ValueError:
            self.log("Sistem Error: Interval/Timeout harus berupa angka!")
            self.safe_ui_update(self.stop_loop)
            return

        self.log(f"▶️ Memulai Loop {mode} Monitoring setiap {interval} detik...")
        
        # Ambil payload untuk loop jika diperlukan
        payload_data = None
        if mode in ["POST", "PUT"]:
            try:
                raw = self.txt_payload.get("1.0", tk.END).strip()
                if raw: payload_data = json.loads(raw)
            except:
                pass # Abaikan jika JSON error saat loop, kirim tanpa payload

        while self.is_looping:
            if mode in ["GET", "POST", "PUT", "DELETE"]:
                success = self.execute_http_request(mode, url, timeout, payload=payload_data, silently=True)
            else:
                success = self.execute_command_ping_status(target_host)

            if not success:
                self.log("🚨 [ALERT] TARGET TIDAK MERESPONS / DOWN!")

            time.sleep(interval)

    def execute_command_ping_status(self, target):
        param = '-n' if platform.system().lower()=='windows' else '-c'
        creation_flags = subprocess.CREATE_NO_WINDOW if platform.system().lower()=='windows' else 0
        try:
            res = subprocess.run(['ping', param, '1', target], stdout=subprocess.PIPE, text=True, timeout=2, creationflags=creation_flags)
            if res.returncode == 0:
                self.log(f"🟢 [PING UP] Terkoneksi ke {target}")
                return True
            else:
                self.log(f"🔴 [PING DOWN] Gagal tersambung ke {target}")
                return False
        except:
            self.log(f"🔴 [PING DOWN] Timeout/Error ke {target}")
            return False

if __name__ == "__main__":
    app = HTTPDetectorApp()
    app.mainloop()
