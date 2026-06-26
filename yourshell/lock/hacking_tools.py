#!/usr/bin/env python3
# ============================================
# HACKING TOOLS SHORTCUT - DARK AI VIP
# Semua tools dalam satu function panggilan
# ============================================

import os
import subprocess
import sys

class HackingTools:
    def __init__(self):
        self.tools = {
            # Network Reconnaissance
            "nmap": "nmap",
            "masscan": "masscan",
            "zmap": "zmap",
            "unicornscan": "unicornscan",
            "rustscan": "rustscan",
            "netdiscover": "netdiscover",
            "bettercap": "bettercap",
            "arp-scan": "arp-scan",
            "netsniff-ng": "netsniff-ng",
            
            # Web Application Testing
            "sqlmap": "sqlmap",
            "nikto": "nikto",
            "dirb": "dirb",
            "gobuster": "gobuster",
            "ffuf": "ffuf",
            "wpscan": "wpscan",
            "dalfox": "dalfox",
            "kiterunner": "kiterunner",
            "arjun": "arjun",
            "waybackurls": "waybackurls",
            "httpx": "httpx",
            "nuclei": "nuclei",
            
            # Password Cracking
            "hashcat": "hashcat",
            "john": "john",
            "hash-identifier": "hash-identifier",
            "findmyhash": "findmyhash",
            "crackle": "crackle",
            "aircrack-ng": "aircrack-ng",
            "hydra": "hydra",
            "medusa": "medusa",
            "ncrack": "ncrack",
            
            # Exploitation Frameworks
            "msfconsole": "msfconsole",
            "searchsploit": "searchsploit",
            "beef": "beef-xss",
            "veil": "veil",
            "setoolkit": "setoolkit",
            "shellter": "shellter",
            "thefatrat": "TheFatRat",
            
            # Post-Exploitation
            "bloodhound": "bloodhound",
            "responder": "responder",
            "impacket": "impacket",
            "empire": "powershell-empire",
            "covenant": "covenant",
            
            # OSINT
            "theharvester": "theharvester",
            "recon-ng": "recon-ng",
            "spiderfoot": "spiderfoot",
            "sherlock": "sherlock",
            "holehe": "holehe",
            "gitleaks": "gitleaks",
            "trufflehog": "trufflehog",
            
            # Wireless
            "wifite": "wifite",
            "kismet": "kismet",
            "reaver": "reaver",
            "bully": "bully",
            "mdk4": "mdk4",
            
            # Bluetooth
            "bluez": "bluez-tools",
            "spooftooph": "spooftooph",
            "btlejack": "btlejack",
            
            # Steganography
            "steghide": "steghide",
            "stegosuite": "stegosuite",
            "outguess": "outguess",
            "xortool": "xortool",
            "hashpump": "hashpump",
            
            # Forensics
            "autopsy": "autopsy",
            "sleuthkit": "sleuthkit",
            "foremost": "foremost",
            "binwalk": "binwalk",
            "strings": "strings",
            "exiftool": "exiftool",
            "volatility": "volatility",
            
            # Reverse Engineering
            "ghidra": "ghidra",
            "radare2": "radare2",
            "cutter": "cutter",
            "jadx": "jadx",
            "apktool": "apktool",
            "dex2jar": "dex2jar",
            "androbugs": "androbugs",
        }
    
    # ==========================================
    # NETWORK RECONNAISSANCE
    # ==========================================
    
    def nmap(self, target, flags="-sV -O"):
        """nmap port scanning with version and OS detection"""
        os.system(f"nmap {flags} {target}")
    
    def masscan(self, target, ports="1-1000", rate="1000"):
        """masscan fast port scanner"""
        os.system(f"masscan -p{ports} --rate={rate} {target}")
    
    def zmap(self, target, port="80"):
        """zmap internet-scale scanner"""
        os.system(f"zmap -p {port} {target}")
    
    def unicornscan(self, target, ports="1-1000"):
        """unicornscan unorthodox port scanner"""
        os.system(f"unicornscan -mU {target}:{ports}")
    
    def rustscan(self, target, ports="1-1000"):
        """rustscan fast port scanner"""
        os.system(f"rustscan -a {target} -p {ports}")
    
    def netdiscover(self, interface="eth0", range="192.168.1.0/24"):
        """netdiscover ARP reconnaissance"""
        os.system(f"netdiscover -i {interface} -r {range}")
    
    def bettercap(self, interface="eth0"):
        """bettercap network manipulation framework"""
        os.system(f"bettercap -iface {interface}")
    
    def arp_scan(self, target="192.168.1.0/24"):
        """arp-scan local network discovery"""
        os.system(f"arp-scan {target}")
    
    def netsniff_ng(self, interface="eth0"):
        """netsniff-ng packet sniffing"""
        os.system(f"netsniff-ng -i {interface}")
    
    # ==========================================
    # WEB APPLICATION TESTING
    # ==========================================
    
    def sqlmap(self, url, data=""):
        """sqlmap automated SQL injection"""
        if data:
            os.system(f"sqlmap -u {url} --data='{data}' --batch")
        else:
            os.system(f"sqlmap -u {url} --batch")
    
    def nikto(self, target):
        """nikto web server scanner"""
        os.system(f"nikto -h {target}")
    
    def dirb(self, target, wordlist="/usr/share/wordlists/dirb/common.txt"):
        """dirb directory brute-force"""
        os.system(f"dirb {target} {wordlist}")
    
    def gobuster(self, target, wordlist="/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"):
        """gobuster directory/file brute-force"""
        os.system(f"gobuster dir -u {target} -w {wordlist}")
    
    def ffuf(self, target, wordlist="/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"):
        """ffuf fast web fuzzer"""
        os.system(f"ffuf -u {target} -w {wordlist}")
    
    def wpscan(self, target, token=""):
        """wpscan WordPress vulnerability scanner"""
        if token:
            os.system(f"wpscan --url {target} --api-token {token}")
        else:
            os.system(f"wpscan --url {target}")
    
    def dalfox(self, target):
        """dalfox XSS scanner"""
        os.system(f"dalfox url {target}")
    
    def kiterunner(self, target):
        """kiterunner API/endpoint fuzzer"""
        os.system(f"kiterunner scan -u {target}")
    
    def arjun(self, target):
        """arjun HTTP parameter discovery"""
        os.system(f"arjun -u {target}")
    
    def waybackurls(self, domain):
        """waybackurls fetch URLs from Wayback Machine"""
        os.system(f"echo {domain} | waybackurls")
    
    def httpx(self, target):
        """httpx HTTP probing"""
        os.system(f"httpx -u {target}")
    
    def nuclei(self, target, templates="critical"):
        """nuclei vulnerability scanner"""
        os.system(f"nuclei -u {target} -t {templates}")
    
    # ==========================================
    # PASSWORD CRACKING
    # ==========================================
    
    def hashcat(self, hash_file, wordlist="/usr/share/wordlists/rockyou.txt", hash_type="0"):
        """hashcat GPU-accelerated password cracking"""
        os.system(f"hashcat -m {hash_type} -a 0 {hash_file} {wordlist}")
    
    def john(self, hash_file, wordlist="/usr/share/wordlists/rockyou.txt"):
        """john the ripper CPU-based cracking"""
        os.system(f"john --wordlist={wordlist} {hash_file}")
    
    def hash_identifier(self, hash_value):
        """hash-identifier identify hash type"""
        os.system(f"hash-identifier '{hash_value}'")
    
    def findmyhash(self, hash_value):
        """findmyhash online hash lookup"""
        os.system(f"findmyhash {hash_value}")
    
    def crackle(self, pcap_file):
        """crackle BLE cracker"""
        os.system(f"crackle -i {pcap_file}")
    
    def aircrack(self, cap_file, wordlist="/usr/share/wordlists/rockyou.txt"):
        """aircrack-ng Wi-Fi WEP/WPA cracking"""
        os.system(f"aircrack-ng -w {wordlist} {cap_file}")
    
    def hydra(self, target, service="ssh", userlist="users.txt", passlist="pass.txt"):
        """hydra network login brute-forcer"""
        os.system(f"hydra -L {userlist} -P {passlist} {target} {service}")
    
    def medusa(self, target, service="ssh", userlist="users.txt", passlist="pass.txt"):
        """medusa parallel brute-forcer"""
        os.system(f"medusa -h {target} -U {userlist} -P {passlist} -M {service}")
    
    def ncrack(self, target, service="ssh", userlist="users.txt", passlist="pass.txt"):
        """ncrack network authentication cracker"""
        os.system(f"ncrack -U {userlist} -P {passlist} {target}:{service}")
    
    # ==========================================
    # EXPLOITATION FRAMEWORKS
    # ==========================================
    
    def msfconsole(self):
        """metasploit framework console"""
        os.system("msfdb start 2>/dev/null && msfconsole")
    
    def searchsploit(self, keyword):
        """searchsploit exploit database search"""
        os.system(f"searchsploit {keyword}")
    
    def beef(self):
        """beef-framework browser exploitation"""
        os.system("beef-xss")
    
    def veil(self):
        """veil payload generation"""
        os.system("veil")
    
    def setoolkit(self):
        """Social Engineering Toolkit"""
        os.system("setoolkit")
    
    def shellter(self):
        """shellter dynamic shellcode injection"""
        os.system("shellter")
    
    def thefatrat(self):
        """TheFatRat payload generator"""
        os.system("python3 /opt/TheFatRat/TheFatRat.py")
    
    # ==========================================
    # POST-EXPLOITATION
    # ==========================================
    
    def bloodhound(self):
        """bloodhound AD attack path mapping"""
        os.system("bloodhound")
    
    def responder(self, interface="eth0"):
        """responder LLMNR/NBT-NS poisoning"""
        os.system(f"responder -I {interface}")
    
    def impacket(self, tool="psexec", target="", user="", passwd="", cmd=""):
        """impacket network protocols toolkit"""
        if tool == "psexec":
            os.system(f"impacket-psexec {user}:{passwd}@{target} '{cmd}'")
        elif tool == "wmiexec":
            os.system(f"impacket-wmiexec {user}:{passwd}@{target} '{cmd}'")
        elif tool == "secretsdump":
            os.system(f"impacket-secretsdump {user}:{passwd}@{target}")
        elif tool == "smbexec":
            os.system(f"impacket-smbexec {user}:{passwd}@{target}")
        else:
            print(f"[!] Tool {tool} not recognized. Use: psexec, wmiexec, secretsdump, smbexec")
    
    def empire(self):
        """powershell-empire post-exploitation"""
        os.system("powershell-empire")
    
    def covenant(self):
        """covenant .NET Core post-exploitation"""
        os.system("dotnet /opt/Covenant/Covenant.dll")
    
    # ==========================================
    # OSINT
    # ==========================================
    
    def theharvester(self, domain, sources="google,bing,linkedin"):
        """theharvester email/domain gathering"""
        os.system(f"theharvester -d {domain} -b {sources}")
    
    def recon_ng(self):
        """recon-ng web reconnaissance framework"""
        os.system("recon-ng")
    
    def spiderfoot(self):
        """spiderfoot automated OSINT"""
        os.system("spiderfoot")
    
    def sherlock(self, username):
        """sherlock social media username search"""
        os.system(f"sherlock {username}")
    
    def holehe(self, email):
        """holehe email verifier"""
        os.system(f"holehe {email}")
    
    def gitleaks(self, repo_path):
        """gitleaks scan git for secrets"""
        os.system(f"gitleaks detect --source {repo_path}")
    
    def trufflehog(self, repo_path):
        """trufflehog scan for secrets"""
        os.system(f"trufflehog filesystem {repo_path}")
    
    # ==========================================
    # WIRELESS TESTING
    # ==========================================
    
    def wifite(self, interface="wlan0"):
        """wifite automated Wi-Fi auditing"""
        os.system(f"wifite -i {interface}")
    
    def kismet(self, interface="wlan0"):
        """kismet Wi-Fi detector and sniffer"""
        os.system(f"kismet -c {interface}")
    
    def reaver(self, bssid, interface="wlan0"):
        """reaver WPS brute-force"""
        os.system(f"reaver -i {interface} -b {bssid} -vv")
    
    def bully(self, bssid, interface="wlan0"):
        """bully WPS brute-force"""
        os.system(f"bully {interface} -b {bssid}")
    
    def mdk4(self, interface="wlan0"):
        """mdk4 multi-purpose Wi-Fi toolkit"""
        os.system(f"mdk4 {interface}")
    
    # ==========================================
    # BLUETOOTH TESTING
    # ==========================================
    
    def bluez(self):
        """bluez-tools Bluetooth utilities"""
        os.system("bluetoothctl")
    
    def spooftooph(self, interface="hci0"):
        """spooftooph Bluetooth name spoofing"""
        os.system(f"spooftooph -i {interface}")
    
    def btlejack(self, interface="hci0"):
        """btlejack Bluetooth Low Energy sniffing"""
        os.system(f"btlejack -i {interface}")
    
    # ==========================================
    # STEGANOGRAPHY & CRYPTOGRAPHY
    # ==========================================
    
    def steghide(self, file, passphrase=""):
        """steghide steganography in image/audio"""
        if passphrase:
            os.system(f"steghide extract -sf {file} -p {passphrase}")
        else:
            os.system(f"steghide extract -sf {file}")
    
    def stegosuite(self):
        """stegosuite GUI steganography"""
        os.system("stegosuite")
    
    def outguess(self, image, output="output.jpg", passphrase=""):
        """outguess steganography in JPEG"""
        if passphrase:
            os.system(f"outguess -k {passphrase} -r {image} {output}")
        else:
            os.system(f"outguess -r {image} {output}")
    
    def xortool(self, file):
        """xortool XOR brute-force"""
        os.system(f"xortool {file}")
    
    def hashpump(self, hash_value, original_data, append_data, key_length):
        """hashpump hash length extension attack"""
        os.system(f"hashpump -s {hash_value} -d '{original_data}' -a '{append_data}' -k {key_length}")
    
    # ==========================================
    # FORENSICS
    # ==========================================
    
    def autopsy(self):
        """autopsy digital forensics platform"""
        os.system("autopsy")
    
    def sleuthkit(self, img_file, command="mmls"):
        """sleuthkit file system forensics"""
        os.system(f"{command} {img_file}")
    
    def foremost(self, file):
        """foremost file recovery"""
        os.system(f"foremost {file}")
    
    def binwalk(self, file):
        """binwalk firmware analysis"""
        os.system(f"binwalk {file}")
    
    def strings(self, file, min_len=4):
        """strings extract text from binaries"""
        os.system(f"strings -n {min_len} {file}")
    
    def exiftool(self, file):
        """exiftool read/edit metadata"""
        os.system(f"exiftool {file}")
    
    def volatility(self, memory_dump, profile="Win7SP1x64", command="pslist"):
        """volatility memory forensics"""
        os.system(f"volatility -f {memory_dump} --profile={profile} {command}")
    
    # ==========================================
    # REVERSE ENGINEERING
    # ==========================================
    
    def ghidra(self):
        """ghidra reverse engineering framework"""
        os.system("ghidraRun")
    
    def radare2(self, file):
        """radare2 reverse engineering framework"""
        os.system(f"radare2 -A {file}")
    
    def cutter(self, file=""):
        """cutter GUI for radare2"""
        if file:
            os.system(f"cutter {file}")
        else:
            os.system("cutter")
    
    def jadx(self, apk_file):
        """jadx Android APK decompiler"""
        os.system(f"jadx {apk_file}")
    
    def apktool(self, apk_file, command="d"):
        """apktool APK reverse engineering"""
        if command == "d":
            os.system(f"apktool d {apk_file}")
        elif command == "b":
            os.system(f"apktool b {apk_file}")
        else:
            print("[!] Use 'd' for decode, 'b' for build")
    
    def dex2jar(self, dex_file):
        """dex2jar DEX to JAR converter"""
        os.system(f"d2j-dex2jar {dex_file}")
    
    def androbugs(self, apk_file):
        """androbugs Android vulnerability scanner"""
        os.system(f"androbugs -f {apk_file}")
    
    # ==========================================
    # CUSTOM / CURATED
    # ==========================================
    
    def pwntools(self):
        """pwntools CTF exploit development"""
        os.system("python3 -c 'from pwn import *; print(\"Pwntools loaded\")'")
    
    def angr(self, binary):
        """angr binary analysis"""
        os.system(f"python3 -c 'import angr; proj = angr.Project(\"{binary}\"); print(proj)'")
    
    def ghostx(self):
        """ghost-x custom terminal toolkit"""
        os.system("python3 ghostx.py")

# ============================================
# MAIN EXECUTION - COMMAND LINE INTERFACE
# ============================================

if __name__ == "__main__":
    tools = HackingTools()
    
    if len(sys.argv) < 2:
        print("""
=== HACKING TOOLS SHORTCUT - DARK AI VIP ===
Usage: python3 hacking_tools.py <tool> [args]

NETWORK RECON:
  nmap <target> [flags]
  masscan <target> [ports] [rate]
  netdiscover [interface] [range]
  bettercap [interface]

WEB TESTING:
  sqlmap <url> [data]
  nikto <target>
  dirb <target> [wordlist]
  gobuster <target> [wordlist]
  ffuf <target> [wordlist]
  wpscan <target> [token]
  dalfox <target>
  nuclei <target> [templates]

PASSWORD CRACKING:
  hashcat <hashfile> [wordlist] [hashtype]
  john <hashfile> [wordlist]
  hydra <target> <service> <userlist> <passlist>
  aircrack <capfile> [wordlist]

EXPLOITATION:
  msfconsole
  searchsploit <keyword>
  setoolkit
  beef

POST-EXPLOIT:
  responder [interface]
  impacket <tool> <target> <user> <pass> <cmd>
  bloodhound

OSINT:
  theharvester <domain> [sources]
  sherlock <username>
  holehe <email>
  gitleaks <repo_path>

WIRELESS:
  wifite [interface]
  reaver <bssid> [interface]
  mdk4 [interface]

FORENSICS:
  foremost <file>
  binwalk <file>
  volatility <memory_dump> [profile] [command]

REVERSE:
  radare2 <file>
  jadx <apk_file>
  apktool <apk_file> [d/b]
  ghidra

STEGANOGRAPHY:
  steghide <file> [passphrase]
  xortool <file>

OTHERS:
  ghostx
  pwntools
  angr <binary>
""")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    args = sys.argv[2:]
    
    # Mapping tool name to function
    tool_funcs = {
        # Network
        "nmap": tools.nmap,
        "masscan": tools.masscan,
        "zmap": tools.zmap,
        "unicornscan": tools.unicornscan,
        "rustscan": tools.rustscan,
        "netdiscover": tools.netdiscover,
        "bettercap": tools.bettercap,
        "arp-scan": tools.arp_scan,
        "netsniff-ng": tools.netsniff_ng,
        
        # Web
        "sqlmap": tools.sqlmap,
        "nikto": tools.nikto,
        "dirb": tools.dirb,
        "gobuster": tools.gobuster,
        "ffuf": tools.ffuf,
        "wpscan": tools.wpscan,
        "dalfox": tools.dalfox,
        "kiterunner": tools.kiterunner,
        "arjun": tools.arjun,
        "waybackurls": tools.waybackurls,
        "httpx": tools.httpx,
        "nuclei": tools.nuclei,
        
        # Cracking
        "hashcat": tools.hashcat,
        "john": tools.john,
        "hash-identifier": tools.hash_identifier,
        "findmyhash": tools.findmyhash,
        "crackle": tools.crackle,
        "aircrack": tools.aircrack,
        "hydra": tools.hydra,
        "medusa": tools.medusa,
        "ncrack": tools.ncrack,
        
        # Exploit
        "msfconsole": tools.msfconsole,
        "searchsploit": tools.searchsploit,
        "beef": tools.beef,
        "veil": tools.veil,
        "setoolkit": tools.setoolkit,
        "shellter": tools.shellter,
        "thefatrat": tools.thefatrat,
        
        # Post
        "bloodhound": tools.bloodhound,
        "responder": tools.responder,
        "impacket": tools.impacket,
        "empire": tools.empire,
        "covenant": tools.covenant,
        
        # OSINT
        "theharvester": tools.theharvester,
        "recon-ng": tools.recon_ng,
        "spiderfoot": tools.spiderfoot,
        "sherlock": tools.sherlock,
        "holehe": tools.holehe,
        "gitleaks": tools.gitleaks,
        "trufflehog": tools.trufflehog,
        
        # Wireless
        "wifite": tools.wifite,
        "kismet": tools.kismet,
        "reaver": tools.reaver,
        "bully": tools.bully,
        "mdk4": tools.mdk4,
        
        # Bluetooth
        "bluez": tools.bluez,
        "spooftooph": tools.spooftooph,
        "btlejack": tools.btlejack,
        
        # Stegano
        "steghide": tools.steghide,
        "stegosuite": tools.stegosuite,
        "outguess": tools.outguess,
        "xortool": tools.xortool,
        "hashpump": tools.hashpump,
        
        # Forensics
        "autopsy": tools.autopsy,
        "sleuthkit": tools.sleuthkit,
        "foremost": tools.foremost,
        "binwalk": tools.binwalk,
        "strings": tools.strings,
        "exiftool": tools.exiftool,
        "volatility": tools.volatility,
        
        # Reverse
        "ghidra": tools.ghidra,
        "radare2": tools.radare2,
        "cutter": tools.cutter,
        "jadx": tools.jadx,
        "apktool": tools.apktool,
        "dex2jar": tools.dex2jar,
        "androbugs": tools.androbugs,
        
        # Custom
        "ghostx": tools.ghostx,
        "pwntools": tools.pwntools,
        "angr": tools.angr,
    }
    
    if tool_name in tool_funcs:
        try:
            tool_funcs[tool_name](*args)
        except Exception as e:
            print(f"[!] Error: {e}")
            print(f"[!] Usage: python3 hacking_tools.py {tool_name} [args]")
    else:
        print(f"[!] Tool '{tool_name}' tidak ditemukan atau belum di-shortcut")
        print("[!] Ketik 'python3 hacking_tools.py' untuk lihat daftar")
