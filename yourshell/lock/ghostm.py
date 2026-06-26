#!/usr/bin/env python3
"""
Ghost-X - Terminal Hacking Toolkit
For Termux / Mobile / Headless environments
"""

import os
import sys
import subprocess
import shutil
import time
import readline  # For better input handling

class GhostX:
    def __init__(self):
        self.tools_available = {}
        self._check_tools()
        self.running = True
        self.current_tool = None
        self.process = None
    
    def _check_tools(self):
        """Check which tools are installed"""
        tools = ['nmap', 'john', 'hashcat', 'hydra', 'sqlmap', 'nikto', 'dirb', 'traceroute']
        for tool in tools:
            path = shutil.which(tool)
            if path:
                self.tools_available[tool] = True
            else:
                self.tools_available[tool] = False
    
    def _clear_screen(self):
        """Clear the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def _print_banner(self):
        """Print the ASCII banner"""
        banner = """
╔═══════════════════════════════════════════════════╗
║       ________               __        __  ___    ║
║      / ____/ /_  ____  _____/ /_      /  |/  /    ║
║     / / __/ __ \/ __ \/ ___/ __/_____/ /|_/ /     ║
║    / /_/ / / / / /_/ (__  ) /_/_____/ /  / /      ║
║    \____/_/ /_/\____/____/\__/     /_/  /_/       ║
║                                                   ║
║                                                   ║
║   Ghost-M v1.0 - Terminal Hacking Toolkit         ║
║   [Termux / Mobile / Headless]                    ║
╚═══════════════════════════════════════════════════╝
"""
        print(banner)
        self._print_status()
    
    def _print_status(self):
        """Print tool availability status"""
        print("\n[+] Tool Status:")
        for tool, available in self.tools_available.items():
            status = "✓" if available else "✗"
            color = "\033[92m" if available else "\033[91m"
            print(f"    {color}{status}\033[0m {tool}")
        print("\n" + "─" * 60)
    
    def _print_menu(self):
        """Print the main menu"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  MAIN MENU")
        print("═" * 60)
        print("  [1] Network Tools")
        print("  [2] Web Tools")
        print("  [3] Crypto Tools")
        print("  [4] Recon Tools")
        print("  [5] System Info")
        print("  [0] Exit")
        print("═" * 60)
    
    def _print_network_menu(self):
        """Print network tools submenu"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  NETWORK TOOLS")
        print("═" * 60)
        print("  [1] Nmap - Port Scanner")
        print("  [2] Traceroute - Network Path")
        print("  [3] DNS Lookup")
        print("  [4] Ping Sweep")
        print("  [0] Back to Main Menu")
        print("═" * 60)
    
    def _print_web_menu(self):
        """Print web tools submenu"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  WEB TOOLS")
        print("═" * 60)
        print("  [1] Nikto - Web Server Scanner")
        print("  [2] Sqlmap - SQL Injection")
        print("  [3] Hydra - Brute Force")
        print("  [4] Dirbuster/Dirb - Directory Bruteforce")
        print("  [0] Back to Main Menu")
        print("═" * 60)
    
    def _print_crypto_menu(self):
        """Print crypto tools submenu"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  CRYPTO TOOLS")
        print("═" * 60)
        print("  [1] Hashcat - Password Cracking")
        print("  [2] John the Ripper")
        print("  [3] Hash Identifier")
        print("  [0] Back to Main Menu")
        print("═" * 60)
    
    def _print_recon_menu(self):
        """Print recon tools submenu"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  RECON TOOLS")
        print("═" * 60)
        print("  [1] WhoIs Lookup")
        print("  [2] Subdomain Scanner")
        print("  [3] Port Scanner (Quick)")
        print("  [0] Back to Main Menu")
        print("═" * 60)
    
    def _get_input(self, prompt):
        """Get user input with prompt"""
        return input(f"\n\033[92m[?]\033[0m {prompt}: ").strip()
    
    def _get_input_with_default(self, prompt, default):
        """Get user input with default value"""
        val = input(f"\n\033[92m[?]\033[0m {prompt} [{default}]: ").strip()
        return val if val else default
    
    def _print_output(self, text, color=None):
        """Print output with optional color"""
        colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'reset': '\033[0m'
        }
        if color and color in colors:
            print(f"{colors[color]}{text}{colors['reset']}")
        else:
            print(text)
    
    def _run_command(self, cmd, show_output=True):
        """Run a command and display output in real-time"""
        if not cmd:
            return
        
        self._print_output(f"\n[>] Running: {' '.join(cmd)}", 'cyan')
        print("─" * 60)
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
            
            process.wait()
            print("─" * 60)
            self._print_output(f"[✓] Process finished (exit code: {process.returncode})", 'green' if process.returncode == 0 else 'red')
            
            return process.returncode
            
        except FileNotFoundError:
            self._print_output(f"[✗] Command not found: {cmd[0]}", 'red')
            self._print_output("    Install it with: apt install " + cmd[0], 'yellow')
            return 1
        except Exception as e:
            self._print_output(f"[✗] Error: {str(e)}", 'red')
            return 1
    
    def _wait_for_enter(self):
        """Wait for Enter key press"""
        input("\n\033[90mPress Enter to continue...\033[0m")
    
    # ─── Network Tools ──────────────────────────────────────────────
    
    def _nmap_scan(self):
        """Run Nmap scan"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  NMAP - Port Scanner")
        print("═" * 60)
        
        if not self.tools_available.get('nmap', False):
            self._print_output("[✗] Nmap not installed. Run: apt install nmap", 'red')
            self._wait_for_enter()
            return
        
        target = self._get_input("Target (IP or domain)")
        if not target:
            self._print_output("[!] Target required", 'yellow')
            self._wait_for_enter()
            return
        
        print("\n[1] SYN Scan (-sS)")
        print("[2] TCP Connect Scan (-sT)")
        print("[3] UDP Scan (-sU)")
        print("[4] Ping Sweep (-sn)")
        scan_type = self._get_input("Select scan type (1-4)")
        
        scan_map = {
            '1': '-sS',
            '2': '-sT',
            '3': '-sU',
            '4': '-sn'
        }
        scan_flag = scan_map.get(scan_type, '-sS')
        
        ports = self._get_input_with_default("Ports (e.g., 1-1000 or 22,80,443)", "1-1000")
        
        os_detect = self._get_input("Enable OS Detection? (y/n)").lower() == 'y'
        verbose = self._get_input("Verbose? (y/n)").lower() == 'y'
        
        cmd = ['nmap', scan_flag, '-p', ports]
        if os_detect:
            cmd.append('-O')
        if verbose:
            cmd.append('-v')
        cmd.append(target)
        
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _traceroute_tool(self):
        """Run traceroute"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  TRACEROUTE - Network Path")
        print("═" * 60)
        
        target = self._get_input("Target (IP or domain)")
        if not target:
            self._print_output("[!] Target required", 'yellow')
            self._wait_for_enter()
            return
        
        hops = self._get_input_with_default("Max hops", "30")
        cmd = ['traceroute', '-m', hops, target] if hops else ['traceroute', target]
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _dns_lookup(self):
        """DNS lookup tool"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  DNS LOOKUP")
        print("═" * 60)
        
        target = self._get_input("Domain to lookup")
        if not target:
            self._print_output("[!] Domain required", 'yellow')
            self._wait_for_enter()
            return
        
        print("\n[1] A")
        print("[2] AAAA")
        print("[3] CNAME")
        print("[4] MX")
        print("[5] NS")
        print("[6] TXT")
        print("[7] ANY")
        record_type = self._get_input("Select record type (1-7)")
        
        record_map = {
            '1': 'A', '2': 'AAAA', '3': 'CNAME',
            '4': 'MX', '5': 'NS', '6': 'TXT', '7': 'ANY'
        }
        rtype = record_map.get(record_type, 'A')
        
        try:
            import dns.resolver
            self._print_output(f"\n[>] Looking up {rtype} records for {target}", 'cyan')
            print("─" * 60)
            answers = dns.resolver.resolve(target, rtype)
            for answer in answers:
                print(f"  {answer.to_text()}")
            print("─" * 60)
        except ImportError:
            self._print_output("[✗] dnspython not installed. Run: pip install dnspython", 'red')
        except dns.resolver.NoAnswer:
            self._print_output(f"[!] No {rtype} records found", 'yellow')
        except dns.resolver.NXDOMAIN:
            self._print_output(f"[!] Domain {target} does not exist", 'yellow')
        except Exception as e:
            self._print_output(f"[✗] Error: {str(e)}", 'red')
        
        self._wait_for_enter()
    
    def _ping_sweep(self):
        """Simple ping sweep"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  PING SWEEP")
        print("═" * 60)
        
        network = self._get_input("Network (e.g., 192.168.1)")
        if not network:
            self._print_output("[!] Network required", 'yellow')
            self._wait_for_enter()
            return
        
        start = int(self._get_input_with_default("Start IP (last octet)", "1"))
        end = int(self._get_input_with_default("End IP (last octet)", "254"))
        
        self._print_output(f"\n[>] Pinging {network}.{start}-{network}.{end}", 'cyan')
        print("─" * 60)
        
        import subprocess
        import threading
        import queue
        
        q = queue.Queue()
        results = []
        
        def ping_ip(ip):
            try:
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '1', ip],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=2
                )
                if result.returncode == 0:
                    results.append(ip)
            except:
                pass
        
        threads = []
        for i in range(start, end + 1):
            ip = f"{network}.{i}"
            t = threading.Thread(target=ping_ip, args=(ip,))
            t.daemon = True
            t.start()
            threads.append(t)
            # Show progress
            if i % 10 == 0:
                print(f"  Scanning... {i}/{end}", end='\r')
        
        for t in threads:
            t.join(timeout=5)
        
        print("─" * 60)
        self._print_output(f"[✓] Found {len(results)} active hosts:", 'green')
        for ip in results:
            print(f"  {ip}")
        print("─" * 60)
        self._wait_for_enter()
    
    # ─── Web Tools ──────────────────────────────────────────────────
    
    def _nikto_scan(self):
        """Run Nikto web scanner"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  NIKTO - Web Server Scanner")
        print("═" * 60)
        
        if not self.tools_available.get('nikto', False):
            self._print_output("[✗] Nikto not installed. Run: apt install nikto", 'red')
            self._wait_for_enter()
            return
        
        target = self._get_input("Target URL/IP (e.g., http://example.com)")
        if not target:
            self._print_output("[!] Target required", 'yellow')
            self._wait_for_enter()
            return
        
        port = self._get_input_with_default("Port", "80")
        ssl = self._get_input("Use SSL/HTTPS? (y/n)").lower() == 'y'
        verbose = self._get_input("Verbose? (y/n)").lower() == 'y'
        
        cmd = ['nikto', '-h', target, '-p', port]
        if ssl:
            cmd.append('-ssl')
        if verbose:
            cmd.append('-V')
        
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _sqlmap_tool(self):
        """Run sqlmap"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  SQLMAP - SQL Injection Tool")
        print("═" * 60)
        
        if not self.tools_available.get('sqlmap', False):
            self._print_output("[✗] sqlmap not installed. Run: apt install sqlmap", 'red')
            self._wait_for_enter()
            return
        
        url = self._get_input("Target URL (with parameter, e.g., http://example.com/page?id=1)")
        if not url:
            self._print_output("[!] URL required", 'yellow')
            self._wait_for_enter()
            return
        
        method = self._get_input("Method (GET/POST)").upper()
        data = ""
        if method == "POST":
            data = self._get_input("POST data (e.g., username=admin&password=test)")
        
        cookie = self._get_input("Cookie (optional)")
        level = self._get_input_with_default("Level (1-5)", "1")
        risk = self._get_input_with_default("Risk (1-3)", "1")
        
        cmd = ['sqlmap', '-u', url]
        if method == "POST" and data:
            cmd.extend(['--data', data])
        if cookie:
            cmd.extend(['--cookie', cookie])
        cmd.extend(['--level', level, '--risk', risk, '--batch'])
        
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _hydra_tool(self):
        """Run Hydra brute force"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  HYDRA - Brute Force Tool")
        print("═" * 60)
        
        if not self.tools_available.get('hydra', False):
            self._print_output("[✗] Hydra not installed. Run: apt install hydra", 'red')
            self._wait_for_enter()
            return
        
        target = self._get_input("Target IP")
        if not target:
            self._print_output("[!] Target required", 'yellow')
            self._wait_for_enter()
            return
        
        print("\n[1] ssh")
        print("[2] ftp")
        print("[3] http-post-form")
        print("[4] smb")
        print("[5] rdp")
        service = self._get_input("Select service (1-5)")
        service_map = {'1': 'ssh', '2': 'ftp', '3': 'http-post-form', '4': 'smb', '5': 'rdp'}
        service = service_map.get(service, 'ssh')
        
        username = self._get_input("Username (or -L for list)")
        wordlist = self._get_input("Password wordlist file path")
        if not wordlist:
            self._print_output("[!] Wordlist required", 'yellow')
            self._wait_for_enter()
            return
        
        cmd = ['hydra', target, service]
        if username.startswith('-L'):
            cmd.append(username)
        else:
            cmd.extend(['-l', username])
        cmd.extend(['-P', wordlist])
        
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _dirbuster_tool(self):
        """Run dirb directory bruteforce"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  DIRBUSTER - Directory Bruteforce")
        print("═" * 60)
        
        if not self.tools_available.get('dirb', False):
            self._print_output("[✗] dirb not installed. Run: apt install dirb", 'red')
            self._wait_for_enter()
            return
        
        target = self._get_input("Target URL (e.g., http://example.com)")
        if not target:
            self._print_output("[!] Target required", 'yellow')
            self._wait_for_enter()
            return
        
        wordlist = self._get_input("Wordlist file (optional, press Enter for default)")
        recursive = self._get_input("Recursive? (y/n)").lower() == 'y'
        
        cmd = ['dirb', target]
        if wordlist:
            cmd.append(wordlist)
        if recursive:
            cmd.append('-r')
        
        self._run_command(cmd)
        self._wait_for_enter()
    
    # ─── Crypto Tools ──────────────────────────────────────────────
    
    def _hashcat_tool(self):
        """Run Hashcat"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  HASHCAT - Password Cracking")
        print("═" * 60)
        
        if not self.tools_available.get('hashcat', False):
            self._print_output("[✗] hashcat not installed. Download from hashcat.net", 'red')
            self._wait_for_enter()
            return
        
        hash_file = self._get_input("Hash file path")
        if not hash_file:
            self._print_output("[!] Hash file required", 'yellow')
            self._wait_for_enter()
            return
        
        print("\n[1] MD5")
        print("[2] SHA1")
        print("[3] SHA256")
        print("[4] SHA512")
        print("[5] NTLM")
        print("[6] bcrypt")
        hash_type = self._get_input("Select hash type (1-6)")
        hash_map = {'1': '0', '2': '100', '3': '1400', '4': '1700', '5': '1000', '6': '3200'}
        hash_type = hash_map.get(hash_type, '0')
        
        print("\n[1] Wordlist Attack")
        print("[2] Brute Force")
        attack_type = self._get_input("Select attack mode (1-2)")
        attack_mode = '0' if attack_type == '1' else '3'
        
        wordlist = ""
        mask = ""
        if attack_type == '1':
            wordlist = self._get_input("Wordlist file path")
            if not wordlist:
                self._print_output("[!] Wordlist required", 'yellow')
                self._wait_for_enter()
                return
        else:
            mask = self._get_input_with_default("Mask (e.g., ?a?a?a?a?a?a)", "?a?a?a?a?a?a")
        
        cmd = ['hashcat', '-m', hash_type, '-a', attack_mode, hash_file]
        if wordlist:
            cmd.append(wordlist)
        if mask and attack_type == '2':
            cmd.extend(['-i', mask])
        
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _john_tool(self):
        """Run John the Ripper"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  JOHN THE RIPPER")
        print("═" * 60)
        
        if not self.tools_available.get('john', False):
            self._print_output("[✗] John not installed. Run: apt install john", 'red')
            self._wait_for_enter()
            return
        
        hash_file = self._get_input("Hash file path")
        if not hash_file:
            self._print_output("[!] Hash file required", 'yellow')
            self._wait_for_enter()
            return
        
        wordlist = self._get_input("Wordlist (optional)")
        format_type = self._get_input("Format (e.g., md5, sha1, nt - optional)")
        
        cmd = ['john']
        if wordlist:
            cmd.extend(['--wordlist', wordlist])
        if format_type:
            cmd.extend(['--format', format_type])
        cmd.append(hash_file)
        
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _hash_identifier(self):
        """Identify hash type"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  HASH IDENTIFIER")
        print("═" * 60)
        
        hash_input = self._get_input("Hash to identify")
        if not hash_input:
            self._print_output("[!] Hash required", 'yellow')
            self._wait_for_enter()
            return
        
        import re
        length = len(hash_input)
        hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
        is_hex = bool(hex_pattern.match(hash_input))
        
        print("\n" + "─" * 60)
        self._print_output(f"  Length: {length} characters", 'cyan')
        self._print_output(f"  Format: {'Hexadecimal' if is_hex else 'Mixed / Base64-like'}", 'cyan')
        
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
        
        if hash_input.startswith('$2') and length >= 60:
            self._print_output("  Likely: bcrypt", 'green')
        elif length in patterns:
            self._print_output(f"  Likely: {patterns[length]}", 'green')
        else:
            self._print_output("  Unknown format. Try: MD5, SHA-1, SHA-256, SHA-512, bcrypt", 'yellow')
        print("─" * 60)
        self._wait_for_enter()
    
    # ─── Recon Tools ───────────────────────────────────────────────
    
    def _whois_lookup(self):
        """WhoIs lookup"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  WHOIS LOOKUP")
        print("═" * 60)
        
        target = self._get_input("Domain to lookup")
        if not target:
            self._print_output("[!] Domain required", 'yellow')
            self._wait_for_enter()
            return
        
        cmd = ['whois', target]
        self._run_command(cmd)
        self._wait_for_enter()
    
    def _subdomain_scanner(self):
        """Simple subdomain scanner using dnsrecon or dnsenum"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  SUBDOMAIN SCANNER")
        print("═" * 60)
        
        domain = self._get_input("Domain (e.g., example.com)")
        if not domain:
            self._print_output("[!] Domain required", 'yellow')
            self._wait_for_enter()
            return
        
        # Try dnsrecon first
        if shutil.which('dnsrecon'):
            cmd = ['dnsrecon', '-d', domain]
            self._run_command(cmd)
        elif shutil.which('dnsenum'):
            cmd = ['dnsenum', domain]
            self._run_command(cmd)
        else:
            self._print_output("[✗] No subdomain scanner found.", 'red')
            self._print_output("    Install: apt install dnsrecon or dnsenum", 'yellow')
        
        self._wait_for_enter()
    
    def _quick_port_scan(self):
        """Quick port scan using netcat or nc"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  QUICK PORT SCAN")
        print("═" * 60)
        
        target = self._get_input("Target IP")
        if not target:
            self._print_output("[!] Target required", 'yellow')
            self._wait_for_enter()
            return
        
        ports = self._get_input_with_default("Ports (comma separated, e.g., 22,80,443)", "22,80,443")
        ports_list = [p.strip() for p in ports.split(',')]
        
        self._print_output(f"\n[>] Scanning {target}", 'cyan')
        print("─" * 60)
        
        for port in ports_list:
            try:
                # Use nc or python socket
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, int(port)))
                sock.close()
                
                if result == 0:
                    self._print_output(f"  Port {port}: OPEN", 'green')
                else:
                    self._print_output(f"  Port {port}: CLOSED", 'red')
            except Exception as e:
                self._print_output(f"  Port {port}: ERROR ({str(e)})", 'yellow')
        
        print("─" * 60)
        self._wait_for_enter()
    
    # ─── System Info ──────────────────────────────────────────────
    
    def _system_info(self):
        """Display system information"""
        self._clear_screen()
        self._print_banner()
        print("\n" + "═" * 60)
        print("  SYSTEM INFORMATION")
        print("═" * 60)
        
        # Basic system info
        uname = os.uname() if hasattr(os, 'uname') else None
        if uname:
            self._print_output(f"  System: {uname.sysname}", 'cyan')
            self._print_output(f"  Node: {uname.nodename}", 'cyan')
            self._print_output(f"  Release: {uname.release}", 'cyan')
            self._print_output(f"  Version: {uname.version}", 'cyan')
            self._print_output(f"  Machine: {uname.machine}", 'cyan')
        
        # Python version
        self._print_output(f"  Python: {sys.version}", 'cyan')
        
        # Tool status
        print("\n" + "─" * 60)
        self._print_output("  INSTALLED TOOLS:", 'green')
        for tool, available in self.tools_available.items():
            status = "✓" if available else "✗"
            color = '\033[92m' if available else '\033[91m'
            print(f"    {color}{status}\033[0m {tool}")
        
        # Disk info (if df is available)
        if shutil.which('df'):
            print("\n" + "─" * 60)
            self._print_output("  DISK USAGE:", 'green')
            subprocess.run(['df', '-h'], check=False)
        
        self._wait_for_enter()
    
    # ─── Main Loop ──────────────────────────────────────────────────
    
    def run(self):
        """Main application loop"""
        while self.running:
            self._print_menu()
            choice = self._get_input("Select an option")
            
            if choice == '0':
                self._print_output("\n[✓] Exiting Ghost-X", 'green')
                self.running = False
                break
            
            elif choice == '1':
                self._network_tools()
            elif choice == '2':
                self._web_tools()
            elif choice == '3':
                self._crypto_tools()
            elif choice == '4':
                self._recon_tools()
            elif choice == '5':
                self._system_info()
            else:
                self._print_output("[!] Invalid option", 'yellow')
                self._wait_for_enter()
    
    def _network_tools(self):
        """Network tools submenu"""
        while True:
            self._print_network_menu()
            choice = self._get_input("Select an option")
            
            if choice == '0':
                break
            elif choice == '1':
                self._nmap_scan()
            elif choice == '2':
                self._traceroute_tool()
            elif choice == '3':
                self._dns_lookup()
            elif choice == '4':
                self._ping_sweep()
            else:
                self._print_output("[!] Invalid option", 'yellow')
    
    def _web_tools(self):
        """Web tools submenu"""
        while True:
            self._print_web_menu()
            choice = self._get_input("Select an option")
            
            if choice == '0':
                break
            elif choice == '1':
                self._nikto_scan()
            elif choice == '2':
                self._sqlmap_tool()
            elif choice == '3':
                self._hydra_tool()
            elif choice == '4':
                self._dirbuster_tool()
            else:
                self._print_output("[!] Invalid option", 'yellow')
    
    def _crypto_tools(self):
        """Crypto tools submenu"""
        while True:
            self._print_crypto_menu()
            choice = self._get_input("Select an option")
            
            if choice == '0':
                break
            elif choice == '1':
                self._hashcat_tool()
            elif choice == '2':
                self._john_tool()
            elif choice == '3':
                self._hash_identifier()
            else:
                self._print_output("[!] Invalid option", 'yellow')
    
    def _recon_tools(self):
        """Recon tools submenu"""
        while True:
            self._print_recon_menu()
            choice = self._get_input("Select an option")
            
            if choice == '0':
                break
            elif choice == '1':
                self._whois_lookup()
            elif choice == '2':
                self._subdomain_scanner()
            elif choice == '3':
                self._quick_port_scan()
            else:
                self._print_output("[!] Invalid option", 'yellow')


if __name__ == "__main__":
    try:
        app = GhostX()
        app.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {str(e)}")
        sys.exit(1)
