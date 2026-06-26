import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import threading
import os
import sys
import shutil

class HackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YourShell Ghost-X")
        self.root.geometry("1200x800")
        
        # Colors
        self.colors = {
            'bg': '#0d1117',
            'bg2': '#161b22',
            'fg': '#c9d1d9',
            'accent': '#58a6ff',
            'border': '#30363d',
            'error': '#f85149',
            'success': '#3fb950'
        }
        
        # Store tool availability messages until output is ready
        self.startup_messages = []
        self.tools_available = {}
        
        # Check for tools and store messages
        self._check_tools()
        
        # Main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar
        self.sidebar = ttk.Frame(self.main_frame, width=200, relief=tk.RIDGE)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.sidebar.pack_propagate(False)
        
        # Content area
        self.content = ttk.Frame(self.main_frame)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Output area - create this BEFORE any _append_output calls
        self.output_frame = ttk.Frame(self.content)
        self.output_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.output = scrolledtext.ScrolledText(
            self.output_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            insertbackground='#c9d1d9'
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        
        # Now that output exists, flush the startup messages
        for msg in self.startup_messages:
            self._append_output(msg)
        self.startup_messages = []  # Clear them so we don't duplicate
        
        # Tool frame
        self.tool_frame = ttk.Frame(self.content)
        self.tool_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Build sidebar
        self._build_sidebar()
        
        # Status bar
        self.status = tk.Label(
            root,
            text="Ready",
            anchor=tk.W,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Segoe UI', 9)
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start with Nmap
        self.current_tool = None
        self.process = None
        self.show_nmap()
    
    def _check_tools(self):
        tools = ['nmap', 'john', 'hashcat', 'hydra', 'sqlmap', 'nikto']
        for tool in tools:
            path = shutil.which(tool)
            if path:
                self.tools_available[tool] = True
                self.startup_messages.append(f"[✓] {tool} found at {path}")
            else:
                self.tools_available[tool] = False
                self.startup_messages.append(f"[✗] {tool} not found in PATH")
    
    def _append_output(self, text):
        # Make sure output exists before writing
        if hasattr(self, 'output') and self.output:
            self.output.insert(tk.END, text + "\n")
            self.output.see(tk.END)
        else:
            # If output doesn't exist yet, store the message
            self.startup_messages.append(text)

    def _build_sidebar(self):
        categories = {
            'Network': ['Nmap', 'Traceroute', 'DNS Lookup'],
            'Web': ['Nikto', 'Sqlmap', 'Hydra', 'Dirbuster'],
            'Crypto': ['Hashcat', 'John the Ripper', 'Hash Identifier']
        }
    
        for cat, tools in categories.items():
            cat_label = ttk.Label(
                self.sidebar,
                text=cat,
                font=('Segoe UI', 10, 'bold')
            )
            cat_label.pack(anchor=tk.W, pady=(10, 5), padx=10)
        
            for tool in tools:
                btn = ttk.Button(
                    self.sidebar,
                    text=tool,
                    style='Sidebar.TButton',
                    command=lambda t=tool: self._switch_tool(t)
                )
                btn.pack(anchor=tk.W, pady=2, padx=20, fill=tk.X)

    def _switch_tool(self, tool):
        if tool == 'Nmap':
            self.show_nmap()
        elif tool == 'Hydra':
            self.show_hydra()
        elif tool == 'John the Ripper':
            self.show_john()
        elif tool == 'Sqlmap':
            self.show_sqlmap()
        elif tool == 'Hashcat':
            self.show_hashcat()
        elif tool == 'Nikto':
            self.show_nikto()
        elif tool == 'Traceroute':
            self.show_traceroute()
        elif tool == 'DNS Lookup':
            self.show_dns_lookup()
        elif tool == 'Dirbuster':
            self.show_dirbuster()
        elif tool == 'Hash Identifier':
            self.show_hash_identifier()
        else:
            self._show_placeholder(tool)

    def _show_placeholder(self, tool_name):
        """Show a placeholder message for tools not yet implemented"""
        self._clear_tool_frame()
    
        # Centered message
        frame = ttk.Frame(self.tool_frame)
        frame.pack(expand=True)
    
        ttk.Label(
            frame,
            text=f"🔧 {tool_name}",
            font=('Segoe UI', 18, 'bold')
        ).pack(pady=20)
    
        ttk.Label(
            frame,
            text="This tool is coming soon.",
            font=('Segoe UI', 12),
            foreground='#8b949e'
        ).pack(pady=10)
    
        ttk.Label(
            frame,
            text="If you need this specific tool, let me know and I'll prioritize it.",
            font=('Segoe UI', 10),
            foreground='#8b949e'
        ).pack(pady=5)
    
        self.current_tool = tool_name.lower().replace(' ', '_')

    def _clear_tool_frame(self):
        for widget in self.tool_frame.winfo_children():
            widget.destroy()
    
    def show_dns_lookup(self):
        self._clear_tool_frame()
        self.current_tool = 'dns_lookup'
    
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10, padx=5)
    
        ttk.Label(frame, text="Domain / Hostname:").pack(anchor=tk.W, padx=5, pady=5)
        self.dns_target = ttk.Entry(frame, width=50)
        self.dns_target.pack(anchor=tk.W, padx=5, pady=5)
        self.dns_target.insert(0, "example.com")
    
        ttk.Label(frame, text="Record Type:").pack(anchor=tk.W, padx=5, pady=5)
        self.dns_type = ttk.Combobox(
            frame,
            values=['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 'ANY'],
            width=10
        )
        self.dns_type.pack(anchor=tk.W, padx=5, pady=5)
        self.dns_type.set('A')
    
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
    
        ttk.Button(
            btn_frame,
            text="▶ Lookup",
            style='Accent.TButton',
            command=self._run_dns_lookup
        ).pack(side=tk.LEFT, padx=5)

    def _run_dns_lookup(self):
        target = self.dns_target.get().strip()
        if not target:
            self._append_output("[!] Domain required")
            return
    
        import socket
        import dns.resolver  # Requires dnspython: pip install dnspython
    
        record_type = self.dns_type.get()
        self._append_output(f"[>] Looking up {record_type} records for {target}")
    
        try:
            answers = dns.resolver.resolve(target, record_type)
            for answer in answers:
                self._append_output(f"  {answer.to_text()}")
        except dns.resolver.NoAnswer:
            self._append_output(f"[!] No {record_type} records found")
        except dns.resolver.NXDOMAIN:
            self._append_output(f"[!] Domain {target} does not exist")
        except Exception as e:
            self._append_output(f"[!] Error: {str(e)}")

    def show_hash_identifier(self):
        self._clear_tool_frame()
        self.current_tool = 'hash_identifier'
    
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10, padx=5)
    
        ttk.Label(frame, text="Hash to identify:").pack(anchor=tk.W, padx=5, pady=5)
        self.hash_id_input = ttk.Entry(frame, width=70)
        self.hash_id_input.pack(anchor=tk.W, padx=5, pady=5)
        self.hash_id_input.insert(0, "5f4dcc3b5aa765d61d8327deb882cf99")
    
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
    
        ttk.Button(
            btn_frame,
            text="▶ Identify",
            style='Accent.TButton',
            command=self._run_hash_identifier
        ).pack(side=tk.LEFT, padx=5)

    def _run_hash_identifier(self):
        hash_input = self.hash_id_input.get().strip()
        if not hash_input:
            self._append_output("[!] Hash required")
            return
    
        self._append_output(f"[>] Identifying hash: {hash_input}")
    
        import re
        length = len(hash_input)
        hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
        is_hex = bool(hex_pattern.match(hash_input))
    
        self._append_output(f"  Length: {length} characters")
        self._append_output(f"  Format: {'Hexadecimal' if is_hex else 'Mixed / Base64-like'}")
    
        # Common hash patterns
        patterns = {
            32: "MD5",
            40: "SHA-1",
            64: "SHA-256",
            96: "SHA-384",
            128: "SHA-512",
            60: "bcrypt ($2a$/$2b$)",
            56: "SHA-512(Unix) / NTLM (if hex)",
            16: "MySQL < 4.1 / MD5 (16 byte)"
        }
    
        # Check for bcrypt format
        if hash_input.startswith('$2') and length >= 60:
            self._append_output("  Likely: bcrypt")
            return
    
        # Check for standard lengths
        if length in patterns:
            self._append_output(f"  Likely: {patterns[length]}")
        else:
            self._append_output("  Unknown format. Try: MD5, SHA-1, SHA-256, SHA-512, bcrypt")

    def show_traceroute(self):
        self._clear_tool_frame()
        self.current_tool = 'traceroute'
    
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10, padx=5)
    
        ttk.Label(frame, text="Target:").pack(anchor=tk.W, padx=5, pady=5)
        self.traceroute_target = ttk.Entry(frame, width=50)
        self.traceroute_target.pack(anchor=tk.W, padx=5, pady=5)
        self.traceroute_target.insert(0, "8.8.8.8")
    
        ttk.Label(frame, text="Max Hops:").pack(anchor=tk.W, padx=5, pady=5)
        self.traceroute_hops = ttk.Entry(frame, width=10)
        self.traceroute_hops.pack(anchor=tk.W, padx=5, pady=5)
        self.traceroute_hops.insert(0, "30")
    
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
    
        self.traceroute_run = ttk.Button(
            btn_frame,
            text="▶ Run Traceroute",
            style='Accent.TButton',
            command=self._run_traceroute
        )
        self.traceroute_run.pack(side=tk.LEFT, padx=5)

    def _run_traceroute(self):
        target = self.traceroute_target.get().strip()
        if not target:
            self._append_output("[!] Target required")
            return
    
        hops = self.traceroute_hops.get().strip()
        cmd = ['traceroute', '-m', hops, target] if hops else ['traceroute', target]
        self._run_subprocess(cmd)

    def show_dirbuster(self):
        self._clear_tool_frame()
        self.current_tool = 'dirbuster'
    
        # Check if dirb is available
        dirb_path = shutil.which('dirb')
        if not dirb_path:
            ttk.Label(
                self.tool_frame,
                text="⚠ dirb not installed. Run: apt-get install dirb (Linux) or use alternative",
                foreground='#f85149'
            ).pack(pady=20)
            return
    
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10, padx=5)
    
        ttk.Label(frame, text="Target URL:").pack(anchor=tk.W, padx=5, pady=5)
        self.dirbuster_target = ttk.Entry(frame, width=60)
        self.dirbuster_target.pack(anchor=tk.W, padx=5, pady=5)
        self.dirbuster_target.insert(0, "http://example.com")
    
        ttk.Label(frame, text="Wordlist:").pack(anchor=tk.W, padx=5, pady=5)
        self.dirbuster_wordlist = ttk.Entry(frame, width=60)
        self.dirbuster_wordlist.pack(anchor=tk.W, padx=5, pady=5)
    
        ttk.Button(
            frame,
            text="Browse Wordlist",
            command=self._browse_dirbuster_wordlist
        ).pack(anchor=tk.W, padx=5, pady=5)
    
        # Options
        options_frame = ttk.LabelFrame(self.tool_frame, text="Options")
        options_frame.pack(fill=tk.X, pady=10, padx=5)
    
        self.dirbuster_recursive = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Recursive (-r)",
            variable=self.dirbuster_recursive
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        self.dirbuster_verbose = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Verbose (-v)",
            variable=self.dirbuster_verbose
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
    
        self.dirbuster_run = ttk.Button(
            btn_frame,
            text="▶ Run Dirbuster",
            style='Accent.TButton',
            command=self._run_dirbuster
        )
        self.dirbuster_run.pack(side=tk.LEFT, padx=5)

    def _run_dirbuster(self):
        target = self.dirbuster_target.get().strip()
        if not target:
            self._append_output("[!] Target URL required")
            return
    
        cmd = ['dirb', target]
    
        wordlist = self.dirbuster_wordlist.get().strip()
        if wordlist:
            cmd.append(wordlist)
    
        if self.dirbuster_recursive.get():
            cmd.append('-r')
        if self.dirbuster_verbose.get():
            cmd.append('-v')
    
        self._run_subprocess(cmd)

    def _browse_dirbuster_wordlist(self):
        filepath = filedialog.askopenfilename(
            title="Select Wordlist",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self.dirbuster_wordlist.delete(0, tk.END)
            self.dirbuster_wordlist.insert(0, filepath)

    def show_sqlmap(self):
        self._clear_tool_frame()
        self.current_tool = 'sqlmap'
    
        if not self.tools_available.get('sqlmap', False):
            ttk.Label(
                self.tool_frame,
                text="⚠ sqlmap not installed. Run: apt-get install sqlmap (Linux) or download from sqlmap.org",
                foreground='#f85149'
            ).pack(pady=20)
            return
    
        # Main frame
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10, padx=5)
    
        # URL
        ttk.Label(frame, text="Target URL:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_url = ttk.Entry(frame, width=60)
        self.sqlmap_url.grid(row=0, column=1, padx=5, pady=5, columnspan=3)
        self.sqlmap_url.insert(0, "http://example.com/page?id=1")
    
        # Method
        ttk.Label(frame, text="Method:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_method = ttk.Combobox(
            frame,
            values=['GET', 'POST'],
            width=10
        )
        self.sqlmap_method.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_method.set('GET')
    
        # Data (for POST)
        ttk.Label(frame, text="POST Data:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_data = ttk.Entry(frame, width=30)
        self.sqlmap_data.grid(row=1, column=3, padx=5, pady=5)
        self.sqlmap_data.insert(0, "username=admin&password=test")
    
        # Cookie
        ttk.Label(frame, text="Cookie:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_cookie = ttk.Entry(frame, width=60)
        self.sqlmap_cookie.grid(row=2, column=1, padx=5, pady=5, columnspan=3)
    
        # Level and Risk
        ttk.Label(frame, text="Level:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_level = ttk.Combobox(
            frame,
            values=['1', '2', '3', '4', '5'],
            width=5
        )
        self.sqlmap_level.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_level.set('1')
    
        ttk.Label(frame, text="Risk:").grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_risk = ttk.Combobox(
            frame,
            values=['1', '2', '3'],
            width=5
        )
        self.sqlmap_risk.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        self.sqlmap_risk.set('1')
    
        # Options
        options_frame = ttk.LabelFrame(self.tool_frame, text="Options")
        options_frame.pack(fill=tk.X, pady=10, padx=5)
    
        self.sqlmap_dbs = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Enumerate Databases (--dbs)",
            variable=self.sqlmap_dbs
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        self.sqlmap_tables = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Enumerate Tables (--tables)",
            variable=self.sqlmap_tables
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        self.sqlmap_dump = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Dump All (--dump-all)",
            variable=self.sqlmap_dump
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        self.sqlmap_batch = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Batch Mode (--batch - no prompts)",
            variable=self.sqlmap_batch
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        # Buttons
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
    
        self.sqlmap_run = ttk.Button(
            btn_frame,
            text="▶ Run sqlmap",
            style='Accent.TButton',
            command=self._run_sqlmap
        )
        self.sqlmap_run.pack(side=tk.LEFT, padx=5)
    
        self.sqlmap_stop = ttk.Button(
            btn_frame,
            text="■ Stop",
            command=self._stop_process
        )
        self.sqlmap_stop.pack(side=tk.LEFT, padx=5)
        self.sqlmap_stop.config(state=tk.DISABLED)

    def _browse_hashcat_file(self):
        """Browse for hash file for hashcat"""
        filepath = filedialog.askopenfilename(
            title="Select Hash File",
            filetypes=[("All files", "*.*")]
        )
        if filepath:
            self.hashcat_file.delete(0, tk.END)
            self.hashcat_file.insert(0, filepath)

    def _browse_hashcat_wordlist(self):
        """Browse for wordlist for hashcat"""
        filepath = filedialog.askopenfilename(
            title="Select Wordlist",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self.hashcat_wordlist.delete(0, tk.END)
            self.hashcat_wordlist.insert(0, filepath)

    def show_hashcat(self):
        self._clear_tool_frame()
        self.current_tool = 'hashcat'
    
        if not self.tools_available.get('hashcat', False):
            ttk.Label(
                self.tool_frame,
                text="⚠ hashcat not installed. Download from hashcat.net",
                foreground='#f85149'
            ).pack(pady=20)
            return
    
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10, padx=5)
    
        # Hash file
        ttk.Label(frame, text="Hash File:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.hashcat_file = ttk.Entry(frame, width=50)
        self.hashcat_file.grid(row=0, column=1, padx=5, pady=5)
    
        ttk.Button(
            frame,
            text="Browse",
            command=self._browse_hashcat_file
        ).grid(row=0, column=2, padx=5, pady=5)
    
        # Hash type
        ttk.Label(frame, text="Hash Type:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.hashcat_type = ttk.Combobox(
            frame,
            values=[
                '0 - MD5',
                '100 - SHA1',
                '1400 - SHA256',
                '1700 - SHA512',
                '1000 - NTLM',
                '1800 - SHA-512(Unix)',
                '3200 - bcrypt($2*$)',
                '7400 - SHA-256(Unix)',
                '5500 - NetNTLMv1',
                '5600 - NetNTLMv2'
            ],
            width=25
        )
        self.hashcat_type.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.hashcat_type.set('0 - MD5')
    
        # Attack mode
        ttk.Label(frame, text="Attack Mode:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.hashcat_attack = ttk.Combobox(
            frame,
            values=[
                '0 - Straight (wordlist)',
                '3 - Brute-force',
                '6 - Hybrid wordlist + mask',
                '7 - Hybrid mask + wordlist'
            ],
            width=25
        )
        self.hashcat_attack.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.hashcat_attack.set('0 - Straight (wordlist)')
    
        # Wordlist
        ttk.Label(frame, text="Wordlist:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.hashcat_wordlist = ttk.Entry(frame, width=50)
        self.hashcat_wordlist.grid(row=3, column=1, padx=5, pady=5)
    
        ttk.Button(
            frame,
            text="Browse",
            command=self._browse_hashcat_wordlist
        ).grid(row=3, column=2, padx=5, pady=5)
    
        # Mask (for brute-force)
        ttk.Label(frame, text="Mask (optional):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.hashcat_mask = ttk.Entry(frame, width=50)
        self.hashcat_mask.grid(row=4, column=1, padx=5, pady=5)
        self.hashcat_mask.insert(0, "?a?a?a?a?a?a")
    
        # Buttons
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
    
        self.hashcat_run = ttk.Button(
            btn_frame,
            text="▶ Run hashcat",
            style='Accent.TButton',
            command=self._run_hashcat
        )
        self.hashcat_run.pack(side=tk.LEFT, padx=5)
    
        self.hashcat_stop = ttk.Button(
            btn_frame,
            text="■ Stop",
            command=self._stop_process
        )
        self.hashcat_stop.pack(side=tk.LEFT, padx=5)
        self.hashcat_stop.config(state=tk.DISABLED)

    def show_nikto(self):
        self._clear_tool_frame()
        self.current_tool = 'nikto'
    
        if not self.tools_available.get('nikto', False):
            ttk.Label(
                self.tool_frame,
                text="⚠ nikto not installed. Run: apt-get install nikto (Linux) or download from github.com/sullo/nikto",
                foreground='#f85149'
            ).pack(pady=20)
            return
    
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10, padx=5)
    
        # Target
        ttk.Label(frame, text="Target URL/IP:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nikto_target = ttk.Entry(frame, width=50)
        self.nikto_target.grid(row=0, column=1, padx=5, pady=5)
        self.nikto_target.insert(0, "http://example.com")
    
        # Port
        ttk.Label(frame, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.nikto_port = ttk.Entry(frame, width=10)
        self.nikto_port.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.nikto_port.insert(0, "80")
    
        # SSL
        self.nikto_ssl = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Use SSL/HTTPS (-ssl)",
            variable=self.nikto_ssl
        ).grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
    
        # Options
        options_frame = ttk.LabelFrame(self.tool_frame, text="Options")
        options_frame.pack(fill=tk.X, pady=10, padx=5)
    
        self.nikto_verbose = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Verbose (-V)",
            variable=self.nikto_verbose
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        self.nikto_findonly = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Find Only (-findonly - don't exploit)",
            variable=self.nikto_findonly
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        self.nikto_mutate = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Mutate Tests (-mutate) - aggressive",
            variable=self.nikto_mutate
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        self.nikto_cache = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="No Cache (-nocache)",
            variable=self.nikto_cache
        ).pack(anchor=tk.W, padx=10, pady=2)
    
        # Buttons
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
    
        self.nikto_run = ttk.Button(
            btn_frame,
            text="▶ Run nikto",
            style='Accent.TButton',
            command=self._run_nikto
        )
        self.nikto_run.pack(side=tk.LEFT, padx=5)
    
        self.nikto_stop = ttk.Button(
            btn_frame,
            text="■ Stop",
            command=self._stop_process
        )
        self.nikto_stop.pack(side=tk.LEFT, padx=5)
        self.nikto_stop.config(state=tk.DISABLED)

    def show_nmap(self):
        self._clear_tool_frame()
        self.current_tool = 'nmap'
        
        # Check if tool is available
        if not self.tools_available.get('nmap', False):
            ttk.Label(
                self.tool_frame,
                text="⚠ Nmap not installed. Run: apt-get install nmap (Linux) or download from nmap.org",
                foreground='#f85149'
            ).pack(pady=20)
            return
        
        # Input frame
        input_frame = ttk.Frame(self.tool_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Target:").grid(row=0, column=0, padx=5, pady=5)
        self.target_entry = ttk.Entry(input_frame, width=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Scan Type:").grid(row=0, column=2, padx=5, pady=5)
        self.scan_type = ttk.Combobox(
            input_frame,
            values=['SYN (-sS)', 'TCP (-sT)', 'UDP (-sU)'],
            width=15
        )
        self.scan_type.grid(row=0, column=3, padx=5, pady=5)
        self.scan_type.set('SYN (-sS)')
        
        ttk.Label(input_frame, text="Ports:").grid(row=1, column=0, padx=5, pady=5)
        self.ports_entry = ttk.Entry(input_frame, width=30)
        self.ports_entry.grid(row=1, column=1, padx=5, pady=5)
        self.ports_entry.insert(0, '1-1000')
        
        # Buttons
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.run_btn = ttk.Button(
            btn_frame,
            text="▶ Run Scan",
            style='Accent.TButton',
            command=self._run_nmap
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            btn_frame,
            text="■ Stop",
            command=self._stop_process
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn.config(state=tk.DISABLED)
        
        # Options
        options_frame = ttk.LabelFrame(self.tool_frame, text="Options")
        options_frame.pack(fill=tk.X, pady=10)
        
        self.os_detect = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="OS Detection (-O)",
            variable=self.os_detect
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        self.verbose = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Verbose (-v)",
            variable=self.verbose
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        # Output hint
        ttk.Label(
            self.tool_frame,
            text="Enter target IP or domain (e.g., 192.168.1.1 or scanme.nmap.org)",
            foreground='#8b949e'
        ).pack(pady=5)
    
    def show_hydra(self):
        self._clear_tool_frame()
        self.current_tool = 'hydra'
        
        if not self.tools_available.get('hydra', False):
            ttk.Label(
                self.tool_frame,
                text="⚠ Hydra not installed. Run: apt-get install hydra",
                foreground='#f85149'
            ).pack(pady=20)
            return
        
        # Hydra interface
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame, text="Target IP:").grid(row=0, column=0, padx=5, pady=5)
        self.hydra_target = ttk.Entry(frame, width=20)
        self.hydra_target.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Service:").grid(row=0, column=2, padx=5, pady=5)
        self.hydra_service = ttk.Combobox(
            frame,
            values=['ssh', 'ftp', 'http-post-form', 'smb', 'rdp', 'telnet'],
            width=15
        )
        self.hydra_service.grid(row=0, column=3, padx=5, pady=5)
        self.hydra_service.set('ssh')
        
        ttk.Label(frame, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        self.hydra_user = ttk.Entry(frame, width=20)
        self.hydra_user.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Password List:").grid(row=1, column=2, padx=5, pady=5)
        self.hydra_wordlist = ttk.Entry(frame, width=20)
        self.hydra_wordlist.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(
            frame,
            text="Browse",
            command=self._browse_wordlist
        ).grid(row=1, column=4, padx=5, pady=5)
        
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.hydra_run = ttk.Button(
            btn_frame,
            text="▶ Run Hydra",
            style='Accent.TButton',
            command=self._run_hydra
        )
        self.hydra_run.pack(side=tk.LEFT, padx=5)
    
    def show_john(self):
        self._clear_tool_frame()
        self.current_tool = 'john'
        
        if not self.tools_available.get('john', False):
            ttk.Label(
                self.tool_frame,
                text="⚠ John the Ripper not installed. Run: apt-get install john",
                foreground='#f85149'
            ).pack(pady=20)
            return
        
        frame = ttk.Frame(self.tool_frame)
        frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame, text="Hash File:").pack(anchor=tk.W, padx=5, pady=5)
        self.john_file = ttk.Entry(frame, width=50)
        self.john_file.pack(anchor=tk.W, padx=5, pady=5)
        
        ttk.Button(
            frame,
            text="Browse Hash File",
            command=self._browse_hash_file
        ).pack(anchor=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Wordlist:").pack(anchor=tk.W, padx=5, pady=5)
        self.john_wordlist = ttk.Entry(frame, width=50)
        self.john_wordlist.pack(anchor=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Format (e.g., md5, sha1, nt):").pack(anchor=tk.W, padx=5, pady=5)
        self.john_format = ttk.Entry(frame, width=30)
        self.john_format.pack(anchor=tk.W, padx=5, pady=5)
        
        btn_frame = ttk.Frame(self.tool_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.john_run = ttk.Button(
            btn_frame,
            text="▶ Run John",
            style='Accent.TButton',
            command=self._run_john
        )
        self.john_run.pack(side=tk.LEFT, padx=5)
    
    def _run_sqlmap(self):
        url = self.sqlmap_url.get().strip()
        if not url:
            self._append_output("[!] URL required")
            return
    
        cmd = ['sqlmap', '-u', url]
    
        # Method
        method = self.sqlmap_method.get()
        if method == 'POST':
            data = self.sqlmap_data.get().strip()
            if data:
                cmd.extend(['--data', data])
    
        # Cookie
        cookie = self.sqlmap_cookie.get().strip()
        if cookie:
            cmd.extend(['--cookie', cookie])
    
        # Level and Risk
        level = self.sqlmap_level.get()
        risk = self.sqlmap_risk.get()
        cmd.extend(['--level', level, '--risk', risk])
    
        # Options
        if self.sqlmap_dbs.get():
            cmd.append('--dbs')
        if self.sqlmap_tables.get():
            cmd.append('--tables')
        if self.sqlmap_dump.get():
            cmd.append('--dump-all')
        if self.sqlmap_batch.get():
            cmd.append('--batch')
    
        self._run_subprocess(cmd)

    def _run_hashcat(self):
        hash_file = self.hashcat_file.get().strip()
        if not hash_file:
            self._append_output("[!] Hash file required")
            return
    
        # Extract hash type number from the combo box
        hash_type_str = self.hashcat_type.get()
        hash_type = hash_type_str.split(' - ')[0]
    
        # Extract attack mode number
        attack_str = self.hashcat_attack.get()
        attack_mode = attack_str.split(' - ')[0]
    
        cmd = ['hashcat', '-m', hash_type, '-a', attack_mode, hash_file]
    
        wordlist = self.hashcat_wordlist.get().strip()
        if wordlist:
            cmd.append(wordlist)
        else:
            self._append_output("[!] Wordlist required for straight attack")
            return
    
        mask = self.hashcat_mask.get().strip()
        if mask and attack_mode == '3':
            cmd.extend(['-i', mask])
    
        self._run_subprocess(cmd)

    def _run_nikto(self):
        target = self.nikto_target.get().strip()
        if not target:
            self._append_output("[!] Target URL/IP required")
            return
    
        cmd = ['nikto', '-h', target]
    
        port = self.nikto_port.get().strip()
        if port:
            cmd.extend(['-p', port])
    
        if self.nikto_ssl.get():
            cmd.append('-ssl')
        if self.nikto_verbose.get():
            cmd.append('-V')
        if self.nikto_findonly.get():
            cmd.append('-findonly')
        if self.nikto_mutate.get():
            cmd.append('-mutate')
        if self.nikto_cache.get():
            cmd.append('-nocache')
    
        self._run_subprocess(cmd)

    def _run_nmap(self):
        target = self.target_entry.get().strip()
        if not target:
            self._append_output("[!] Target required")
            return
        
        # Build command
        cmd = ['nmap']
        
        # Scan type
        scan_type = self.scan_type.get()
        if 'SYN' in scan_type:
            cmd.append('-sS')
        elif 'TCP' in scan_type:
            cmd.append('-sT')
        elif 'UDP' in scan_type:
            cmd.append('-sU')
        
        # Ports
        ports = self.ports_entry.get().strip()
        if ports:
            cmd.extend(['-p', ports])
        
        # Options
        if self.os_detect.get():
            cmd.append('-O')
        if self.verbose.get():
            cmd.append('-v')
        
        cmd.append(target)
        
        self._run_subprocess(cmd)
    
    def _run_hydra(self):
        target = self.hydra_target.get().strip()
        service = self.hydra_service.get().strip()
        user = self.hydra_user.get().strip()
        wordlist = self.hydra_wordlist.get().strip()
        
        if not all([target, service, user, wordlist]):
            self._append_output("[!] All fields required")
            return
        
        cmd = ['hydra', '-l', user, '-P', wordlist, target, service]
        self._run_subprocess(cmd)
    
    def _run_john(self):
        hash_file = self.john_file.get().strip()
        wordlist = self.john_wordlist.get().strip()
        format_type = self.john_format.get().strip()
        
        if not hash_file:
            self._append_output("[!] Hash file required")
            return
        
        cmd = ['john']
        if wordlist:
            cmd.extend(['--wordlist', wordlist])
        if format_type:
            cmd.extend(['--format', format_type])
        cmd.append(hash_file)
        
        self._run_subprocess(cmd)
    
    def _run_subprocess(self, cmd):
        self._append_output(f"[>] Running: {' '.join(cmd)}")
        
        if self.process and self.process.poll() is None:
            self._append_output("[!] Another process is already running. Stop it first.")
            return
        
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status.config(text="Running...")
        
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        def read_output():
            try:
                for line in iter(self.process.stdout.readline, ''):
                    self._append_output(line.rstrip())
                for line in iter(self.process.stderr.readline, ''):
                    self._append_output(f"[!] {line.rstrip()}")
                self.process.wait()
                self.root.after(0, self._process_finished)
            except Exception as e:
                self.root.after(0, lambda: self._append_output(f"[!] Error: {str(e)}"))
                self.root.after(0, self._process_finished)
        
        thread = threading.Thread(target=read_output)
        thread.daemon = True
        thread.start()
    
    def _stop_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self._append_output("[!] Process terminated")
            self.process = None
            self._process_finished()
    
    def _process_finished(self):
        self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.status.config(text="Finished"))
        self.root.after(0, lambda: self._append_output("--- Process finished ---"))
    
    def _append_output(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
    
    def _browse_wordlist(self):
        filepath = filedialog.askopenfilename(
            title="Select Wordlist",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self.hydra_wordlist.delete(0, tk.END)
            self.hydra_wordlist.insert(0, filepath)
    
    def _browse_hash_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Hash File",
            filetypes=[("All files", "*.*")]
        )
        if filepath:
            self.john_file.delete(0, tk.END)
            self.john_file.insert(0, filepath)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Apply a dark theme manually
    root.tk_setPalette(
        background='#0d1117',
        foreground='#c9d1d9',
        activeBackground='#161b22',
        activeForeground='#c9d1d9'
    )
    
    app = HackingApp(root)
    root.mainloop()
