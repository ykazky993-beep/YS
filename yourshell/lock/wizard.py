#!/usr/bin/env python3
# ============================================
# HACKING TOOLS WIZARD - DARK AI VIP
# Menu interaktif untuk semua tools
# ============================================

import os
import sys
import subprocess
import platform

# Warna untuk tampilan
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

class HackingWizard:
    def __init__(self):
        self.tools = HackingTools()
        self.running = True
        self.current_target = ""
        self.current_wordlist = "/usr/share/wordlists/rockyou.txt"
        
    def clear_screen(self):
        os.system('clear' if platform.system() != 'Windows' else 'cls')
    
    def print_banner(self):
        banner = f"""
{Colors.RED}
╔═════════════════════════════════════════════╗
║                   Ghost-V                   ║
║  ONE                FOR                ALL  ║
╚═════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(banner)
    
    def print_menu(self):
        self.clear_screen()
        self.print_banner()
        
        menu = f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.RESET}
{Colors.GREEN}  📡 NETWORK RECONNAISSANCE{Colors.RESET}
{Colors.WHITE}   1.  nmap          - Port scanning dengan version detection
   2.  masscan       - Fast asynchronous port scanner
   3.  netdiscover   - ARP reconnaissance local network
   4.  bettercap     - Network manipulation framework
   5.  arp-scan      - ARP scanning local discovery
   6.  rustscan      - Fast port scanner (Rust)
   7.  unicornscan   - Unorthodox port scanner
   8.  zmap          - Internet-scale scanner{Colors.RESET}

{Colors.YELLOW}  🌐 WEB APPLICATION TESTING{Colors.RESET}
{Colors.WHITE}   9.  sqlmap        - Automated SQL injection
   10. nikto         - Web server vulnerability scanner
   11. dirb          - Directory brute-force
   12. gobuster      - Directory/file brute-force (Go)
   13. ffuf          - Fast web fuzzer
   14. wpscan        - WordPress vulnerability scanner
   15. dalfox        - XSS scanner
   16. nuclei        - Vulnerability scanner dengan templates
   17. arjun         - HTTP parameter discovery
   18. waybackurls   - Fetch URLs dari Wayback Machine{Colors.RESET}

{Colors.RED}  🔑 PASSWORD CRACKING{Colors.RESET}
{Colors.WHITE}   19. hashcat       - GPU-accelerated password cracking
   20. john          - CPU-based password cracking
   21. hydra         - Network login brute-forcer
   22. medusa        - Parallel brute-forcer
   23. aircrack-ng   - Wi-Fi WEP/WPA cracking
   24. ncrack        - Network authentication cracker{Colors.RESET}

{Colors.PURPLE}  💣 EXPLOITATION FRAMEWORKS{Colors.RESET}
{Colors.WHITE}   25. msfconsole    - Metasploit Framework
   26. searchsploit  - Exploit database search
   27. setoolkit     - Social Engineering Toolkit
   28. beef          - Browser exploitation framework
   29. veil          - Payload generation framework
   30. shellter      - Dynamic shellcode injection
   31. thefatrat     - Payload generation tool{Colors.RESET}

{Colors.CYAN}  🕵️ POST-EXPLOITATION{Colors.RESET}
{Colors.WHITE}   32. responder     - LLMNR/NBT-NS poisoning
   33. impacket      - Network protocols toolkit
   34. bloodhound    - AD attack path mapping
   35. empire        - PowerShell post-exploitation
   36. covenant      - .NET Core post-exploitation{Colors.RESET}

{Colors.GREEN}  🔍 OSINT (Open Source Intelligence){Colors.RESET}
{Colors.WHITE}   37. theharvester  - Email/domain gathering
   38. recon-ng      - Web reconnaissance framework
   39. sherlock      - Social media username search
   40. holehe        - Email verifier
   41. gitleaks      - Scan git for secrets
   42. trufflehog    - Scan for high-entropy secrets
   43. spiderfoot    - Automated OSINT gathering{Colors.RESET}

{Colors.YELLOW}  📶 WIRELESS & BLUETOOTH{Colors.RESET}
{Colors.WHITE}   44. wifite        - Automated Wi-Fi auditing
   45. reaver        - WPS brute-force
   46. mdk4          - Multi-purpose Wi-Fi toolkit
   47. kismet        - Wi-Fi detector and sniffer
   48. bluez         - Bluetooth utilities
   49. btlejack      - BLE sniffing{Colors.RESET}

{Colors.RED}  🖼️ STEGANOGRAPHY & FORENSICS{Colors.RESET}
{Colors.WHITE}   50. steghide      - Steganography in image/audio
   51. xortool       - XOR brute-force
   52. foremost      - File recovery
   53. binwalk       - Firmware analysis
   54. volatility    - Memory forensics
   55. exiftool      - Metadata reader{Colors.RESET}

{Colors.PURPLE}  🔧 REVERSE ENGINEERING{Colors.RESET}
{Colors.WHITE}   56. ghidra        - NSA reverse engineering framework
   57. radare2       - Advanced reverse engineering
   58. jadx          - Android APK decompiler
   59. apktool       - APK reverse engineering
   60. dex2jar       - DEX to JAR converter{Colors.RESET}

{Colors.CYAN}  ⚡ CUSTOM TOOLS{Colors.RESET}
{Colors.WHITE}   61. ghostx        - Ghost-X terminal toolkit
   62. pwntools      - CTF exploit library
   63. angr          - Binary analysis framework{Colors.RESET}

{Colors.RED}{Colors.BOLD}─────────────────────────────────────────────────────────────────{Colors.RESET}
{Colors.WHITE}   99. [⚙️] SETTINGS    - Konfigudefault{Colors.RESET}
{Colors.RED}    0. [✖] EXIT       -  exit{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.RESET}
        """
        print(menu)
    
    def get_input(self, prompt, default=""):
        if default:
            prompt = f"{Colors.CYAN}{prompt} [{default}]: {Colors.RESET}"
        else:
            prompt = f"{Colors.CYAN}{prompt}: {Colors.RESET}"
        value = input(prompt)
        return value if value else default
    
    def get_target(self):
        target = self.get_input("target (IP/Domain)", self.current_target)
        self.current_target = target
        return target
    
    def get_wordlist(self):
        wordlist = self.get_input("input path wordlist", self.current_wordlist)
        self.current_wordlist = wordlist
        return wordlist
    
    def run_tool(self, tool_func, *args):
        try:
            print(f"\n{Colors.GREEN}[+] running tool...{Colors.RESET}\n")
            tool_func(*args)
            print(f"\n{Colors.GREEN}[+] done.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")
        
        input(f"\n{Colors.DIM}enter to back menu...{Colors.RESET}")
    
    # ==========================================
    # MENU HANDLER
    # ==========================================
    
    def menu_network(self):
        target = self.get_target()
        print("\n" + "="*50)
        print("1. Scan all port (1-65535)")
        print("2. Scan port (1-1000)")
        print("3. Scan port spesific")
        choice = input("Option (1-3): ")
        
        if choice == "1":
            self.run_tool(self.tools.nmap, target, "-p- -sV")
        elif choice == "2":
            self.run_tool(self.tools.nmap, target, "-sV")
        elif choice == "3":
            ports = self.get_input("port (example: 22,80,443)")
            self.run_tool(self.tools.nmap, target, f"-p {ports} -sV")
        else:
            self.run_tool(self.tools.nmap, target)
    
    def menu_sqlmap(self):
        url = self.get_input("URL target")
        data = self.get_input("Data POST (opsional)")
        if data:
            self.run_tool(self.tools.sqlmap, url, data)
        else:
            self.run_tool(self.tools.sqlmap, url)
    
    def menu_hashcat(self):
        hash_file = self.get_input("path file hash")
        wordlist = self.get_wordlist()
        hash_type = self.get_input("hash type (0=MD5, 100=SHA1, 1400=SHA256)", "0")
        self.run_tool(self.tools.hashcat, hash_file, wordlist, hash_type)
    
    def menu_hydra(self):
        target = self.get_target()
        service = self.get_input("Service (ssh, ftp, http, etc)", "ssh")
        userlist = self.get_input("Path userlist file", "users.txt")
        passlist = self.get_input("Path passlist file", "pass.txt")
        self.run_tool(self.tools.hydra, target, service, userlist, passlist)
    
    def menu_impacket(self):
        tool = self.get_input("Tool (psexec/wmiexec/secretsdump/smbexec)", "psexec")
        target = self.get_target()
        user = self.get_input("Username")
        passwd = self.get_input("Password")
        cmd = self.get_input("Command to execute", "whoami")
        self.run_tool(self.tools.impacket, tool, target, user, passwd, cmd)
    
    def menu_aircrack(self):
        cap_file = self.get_input("input path .cap file")
        wordlist = self.get_wordlist()
        self.run_tool(self.tools.aircrack, cap_file, wordlist)
    
    def menu_steghide(self):
        file = self.get_input("input path file photo/audio")
        passphrase = self.get_input("Passphrase (opsional)")
        self.run_tool(self.tools.steghide, file, passphrase)
    
    def menu_volatility(self):
        memory_dump = self.get_input("path memory dump")
        profile = self.get_input("Profile (Win7SP1x64, Win10x64, etc)", "Win7SP1x64")
        command = self.get_input("Command (pslist, filescan, hivelist, etc)", "pslist")
        self.run_tool(self.tools.volatility, memory_dump, profile, command)
    
    def menu_john(self):
        hash_file = self.get_input("path file hash")
        wordlist = self.get_wordlist()
        self.run_tool(self.tools.john, hash_file, wordlist)
    
    def menu_theharvester(self):
        domain = self.get_input("domain")
        sources = self.get_input("Sources (google,bing,linkedin)", "google,bing")
        self.run_tool(self.tools.theharvester, domain, sources)
    
    def menu_sherlock(self):
        username = self.get_input("username")
        self.run_tool(self.tools.sherlock, username)
    
    def menu_wifite(self):
        interface = self.get_input("Interface (wlan0, wlan1)", "wlan0")
        self.run_tool(self.tools.wifite, interface)
    
    def menu_reaver(self):
        bssid = self.get_input("BSSID target")
        interface = self.get_input("Interface", "wlan0")
        self.run_tool(self.tools.reaver, bssid, interface)
    
    def menu_jadx(self):
        apk_file = self.get_input("path APK file")
        self.run_tool(self.tools.jadx, apk_file)
    
    def menu_apktool(self):
        apk_file = self.get_input("path APK file")
        command = self.get_input("Command (d=decode, b=build)", "d")
        self.run_tool(self.tools.apktool, apk_file, command)
    
    def menu_radare2(self):
        file = self.get_input("path file binary")
        self.run_tool(self.tools.radare2, file)
    
    def menu_angr(self):
        binary = self.get_input("path binary")
        self.run_tool(self.tools.angr, binary)
    
    def menu_gitleaks(self):
        repo_path = self.get_input("path repository")
        self.run_tool(self.tools.gitleaks, repo_path)
    
    def menu_binwalk(self):
        file = self.get_input("path file")
        self.run_tool(self.tools.binwalk, file)
    
    def menu_foremost(self):
        file = self.get_input("path file")
        self.run_tool(self.tools.foremost, file)
    
    def menu_xortool(self):
        file = self.get_input("path file")
        self.run_tool(self.tools.xortool, file)
    
    def menu_settings(self):
        self.clear_screen()
        print(f"{Colors.BOLD}⚙️ SETTINGS{Colors.RESET}\n")
        print(f"1. Default Wordlist : {self.current_wordlist}")
        print(f"2. Default Target   : {self.current_target}")
        print("\n[1] change wordlist")
        print("[2] change target default")
        print("[0] back")
        
        choice = input("\npick: ")
        if choice == "1":
            self.current_wordlist = self.get_input("Path wordlist (new)", self.current_wordlist)
        elif choice == "2":
            self.current_target = self.get_input("Target default (new)", self.current_target)
    
    # ==========================================
    # MAIN LOOP
    # ==========================================
    
    def run(self):
        # Mapping menu ke fungsi
        menu_handlers = {
            "1": ("nmap", self.menu_network),
            "2": ("masscan", lambda: self.run_tool(self.tools.masscan, self.get_target(), "1-1000", "1000")),
            "3": ("netdiscover", lambda: self.run_tool(self.tools.netdiscover, "eth0", "192.168.1.0/24")),
            "4": ("bettercap", lambda: self.run_tool(self.tools.bettercap, "eth0")),
            "5": ("arp-scan", lambda: self.run_tool(self.tools.arp_scan, self.get_target())),
            "6": ("rustscan", lambda: self.run_tool(self.tools.rustscan, self.get_target())),
            "7": ("unicornscan", lambda: self.run_tool(self.tools.unicornscan, self.get_target())),
            "8": ("zmap", lambda: self.run_tool(self.tools.zmap, self.get_target())),
            "9": ("sqlmap", self.menu_sqlmap),
            "10": ("nikto", lambda: self.run_tool(self.tools.nikto, self.get_target())),
            "11": ("dirb", lambda: self.run_tool(self.tools.dirb, self.get_target())),
            "12": ("gobuster", lambda: self.run_tool(self.tools.gobuster, self.get_target())),
            "13": ("ffuf", lambda: self.run_tool(self.tools.ffuf, self.get_target())),
            "14": ("wpscan", lambda: self.run_tool(self.tools.wpscan, self.get_target())),
            "15": ("dalfox", lambda: self.run_tool(self.tools.dalfox, self.get_target())),
            "16": ("nuclei", lambda: self.run_tool(self.tools.nuclei, self.get_target())),
            "17": ("arjun", lambda: self.run_tool(self.tools.arjun, self.get_target())),
            "18": ("waybackurls", lambda: self.run_tool(self.tools.waybackurls, self.get_target())),
            "19": ("hashcat", self.menu_hashcat),
            "20": ("john", self.menu_john),
            "21": ("hydra", self.menu_hydra),
            "22": ("medusa", lambda: self.run_tool(self.tools.medusa, self.get_target(), "ssh", "users.txt", "pass.txt")),
            "23": ("aircrack-ng", self.menu_aircrack),
            "24": ("ncrack", lambda: self.run_tool(self.tools.ncrack, self.get_target(), "ssh", "users.txt", "pass.txt")),
            "25": ("msfconsole", lambda: self.run_tool(self.tools.msfconsole)),
            "26": ("searchsploit", lambda: self.run_tool(self.tools.searchsploit, self.get_input("Keyword"))),
            "27": ("setoolkit", lambda: self.run_tool(self.tools.setoolkit)),
            "28": ("beef", lambda: self.run_tool(self.tools.beef)),
            "29": ("veil", lambda: self.run_tool(self.tools.veil)),
            "30": ("shellter", lambda: self.run_tool(self.tools.shellter)),
            "31": ("thefatrat", lambda: self.run_tool(self.tools.thefatrat)),
            "32": ("responder", lambda: self.run_tool(self.tools.responder, "eth0")),
            "33": ("impacket", self.menu_impacket),
            "34": ("bloodhound", lambda: self.run_tool(self.tools.bloodhound)),
            "35": ("empire", lambda: self.run_tool(self.tools.empire)),
            "36": ("covenant", lambda: self.run_tool(self.tools.covenant)),
            "37": ("theharvester", self.menu_theharvester),
            "38": ("recon-ng", lambda: self.run_tool(self.tools.recon_ng)),
            "39": ("sherlock", self.menu_sherlock),
            "40": ("holehe", lambda: self.run_tool(self.tools.holehe, self.get_input("Email"))),
            "41": ("gitleaks", self.menu_gitleaks),
            "42": ("trufflehog", lambda: self.run_tool(self.tools.trufflehog, self.get_input("Path repo"))),
            "43": ("spiderfoot", lambda: self.run_tool(self.tools.spiderfoot)),
            "44": ("wifite", self.menu_wifite),
            "45": ("reaver", self.menu_reaver),
            "46": ("mdk4", lambda: self.run_tool(self.tools.mdk4, "wlan0")),
            "47": ("kismet", lambda: self.run_tool(self.tools.kismet, "wlan0")),
            "48": ("bluez", lambda: self.run_tool(self.tools.bluez)),
            "49": ("btlejack", lambda: self.run_tool(self.tools.btlejack, "hci0")),
            "50": ("steghide", self.menu_steghide),
            "51": ("xortool", self.menu_xortool),
            "52": ("foremost", self.menu_foremost),
            "53": ("binwalk", self.menu_binwalk),
            "54": ("volatility", self.menu_volatility),
            "55": ("exiftool", lambda: self.run_tool(self.tools.exiftool, self.get_input("File path"))),
            "56": ("ghidra", lambda: self.run_tool(self.tools.ghidra)),
            "57": ("radare2", self.menu_radare2),
            "58": ("jadx", self.menu_jadx),
            "59": ("apktool", self.menu_apktool),
            "60": ("dex2jar", lambda: self.run_tool(self.tools.dex2jar, self.get_input("DEX file path"))),
            "61": ("ghostx", lambda: self.run_tool(self.tools.ghostx)),
            "62": ("pwntools", lambda: self.run_tool(self.tools.pwntools)),
            "63": ("angr", self.menu_angr),
            "99": ("settings", self.menu_settings),
        }
        
        while self.running:
            self.print_menu()
            choice = input(f"{Colors.BOLD}┌─[{Colors.GREEN}YourS{Colors.RED}hell{Colors.RESET}Ghost{Colors.RESET}{Colors.BOLD}@GHOST-V]{Colors.RESET}\n└──╼ {Colors.CYAN}$ {Colors.RESET}")
            
            if choice == "0":
                self.clear_screen()
                print(f"{Colors.RED}exit{Colors.RESET}")
                self.running = False
                break
            
            if choice in menu_handlers:
                handler = menu_handlers[choice]
                if isinstance(handler, tuple):
                    name, func = handler
                else:
                    func = handler
                func()
            else:
                print(f"{Colors.RED}[!] invalid choice!{Colors.RESET}")
                input("enter to continue...")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    # Import HackingTools dari file yang sama atau external
    # Jika file terpisah, tambahkan: from hacking_tools import HackingTools
    
    # Sementara kita definisikan dummy class (akan di-replace dengan import)
    try:
        from hacking_tools import HackingTools
    except ImportError:
        # Fallback: definisikan class kosong yang akan diisi
        class HackingTools:
            pass
        
        print(f"{Colors.YELLOW}[!] hacking_tools.py tidak ditemukan, gunakan versi standalone{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Pastikan hacking_tools.py berada di direktori yang sama{Colors.RESET}")
        sys.exit(1)
    
    wizard = HackingWizard()
    wizard.run()
