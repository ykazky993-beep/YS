#!/bin/bash
# ============================================
# DARK AI VIP - AUTO INSTALLER
# Install semua tools dari requirements.txt
# ============================================

set -e

# Warna
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Auto Install for YourShellGhost                             ║${NC}"
echo -e "${BLUE}║  ~30min | warning some packages maybe are not found          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Cek root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[!] Root Requied!${NC}"
   echo -e "${YELLOW}use: sudo bash install_all.sh${NC}"
   exit 1
fi

# Update system
echo -e "${GREEN}[+] Updating system packages...${NC}"
apt update && apt upgrade -y

# Install core dependencies
echo -e "${GREEN}[+] Installing core dependencies...${NC}"
apt install -y python3 python3-pip python3-venv git curl wget \
    build-essential python3-dev libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev \
    libpq-dev libpcap-dev libsqlite3-dev libbz2-dev \
    libreadline-dev libncurses5-dev libgdbm-dev \
    liblzma-dev tk-dev uuid-dev libnss3-dev \
    libdbus-1-dev libnl-3-dev libnl-genl-3-dev \
    vim nano tmux screen htop tree \
    jq yq bat ripgrep fzf

# Install network tools
echo -e "${GREEN}[+] Installing network tools...${NC}"
apt install -y nmap masscan zmap unicornscan netdiscover \
    bettercap arp-scan netsniff-ng tcpdump wireshark \
    tshark traceroute netcat socat ncat hping3 fping \
    mtr iperf3 speedtest-cli ifconfig iproute2 \
    bridge-utils ethtool iwconfig wireless-tools

# Install web tools
echo -e "${GREEN}[+] Installing web application tools...${NC}"
apt install -y sqlmap nikto dirb wpscan ffuf gobuster \
    httpx nuclei arjun dalfox

# Install password cracking
echo -e "${GREEN}[+] Installing password cracking tools...${NC}"
apt install -y hashcat john hydra medusa ncrack aircrack-ng \
    hash-identifier findmyhash crackle hashpump xortool

# Install exploitation
echo -e "${GREEN}[+] Installing exploitation frameworks...${NC}"
apt install -y metasploit-framework exploitdb setoolkit \
    beef-xss veil shellter

# Install post-exploitation
echo -e "${GREEN}[+] Installing post-exploitation tools...${NC}"
apt install -y bloodhound responder powershell-empire \
    impacket-scripts

# Install wireless
echo -e "${GREEN}[+] Installing wireless tools...${NC}"
apt install -y wifite kismet reaver bully mdk4 \
    bluez-tools spooftooph

# Install forensics
echo -e "${GREEN}[+] Installing forensics tools...${NC}"
apt install -y autopsy sleuthkit foremost binwalk \
    scalpel magicrescue photorec testdisk ddrescue \
    guymager afflib ewf-tools libewf

# Install steganography
echo -e "${GREEN}[+] Installing steganography tools...${NC}"
apt install -y steghide stegosuite outguess exiftool

# Install reverse engineering
echo -e "${GREEN}[+] Installing reverse engineering tools...${NC}"
apt install -y radare2 cutter jadx apktool dex2jar \
    androbugs ghidra

# Install OSINT
echo -e "${GREEN}[+] Installing OSINT tools...${NC}"
apt install -y theharvester recon-ng spiderfoot

# Install Rust tools
echo -e "${GREEN}[+] Installing Rust tools...${NC}"
if ! command -v cargo &> /dev/null; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi
cargo install rustscan

# Install Python packages
echo -e "${GREEN}[+] Installing Python packages...${NC}"
pip3 install --upgrade pip setuptools wheel virtualenv

# Python packages yang perlu diinstall via pip
echo -e "${GREEN}[+] Installing Python libraries...${NC}"
pip3 install -r requirements.txt 2>/dev/null || pip3 install \
    colorama requests beautifulsoup4 lxml paramiko scapy \
    netaddr dnspython pyOpenSSL cryptography pycryptodome \
    termcolor tabulate psutil pyyaml python-nmap \
    python-dotenv click prompt_toolkit rich typer pydantic \
    httpx aiohttp asyncio websockets urllib3 certifi \
    chardet idna six sqlalchemy pymysql psycopg2-binary \
    redis pymongo shodan censys whois phonenumbers \
    holehe sherlock-project pwntools capstone keystone-engine \
    unicorn angr binjitsu z3-solver numpy scipy matplotlib \
    jupyter ipython ctfcli ropgadget one_gadget frida \
    frida-tools objection androguard zipfile

# Install Go tools
echo -e "${GREEN}[+] Installing Go tools...${NC}"
if ! command -v go &> /dev/null; then
    wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
fi

go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/waybackurls/cmd/waybackurls@latest
go install -v github.com/hahwul/dalfox/v2@latest
go install -v github.com/assetnote/kiterunner@latest
go install -v github.com/tomnomnom/gitleaks@latest
go install -v github.com/trufflesecurity/trufflehog/v3@latest
go install -v github.com/ffuf/ffuf@latest
go install -v github.com/OJ/gobuster/v3@latest

# Install wordlists
echo -e "${GREEN}[+] Downloading wordlists...${NC}"
if [ ! -f /usr/share/wordlists/rockyou.txt ]; then
    wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O /usr/share/wordlists/rockyou.txt
fi
if [ ! -f /usr/share/wordlists/dirb/common.txt ]; then
    wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web_Content/common.txt -O /usr/share/wordlists/dirb/common.txt
fi

# Clone custom tools
echo -e "${GREEN}[+] Cloning custom tools...${NC}"
if [ ! -d /opt/TheFatRat ]; then
    git clone https://github.com/Screetsec/TheFatRat /opt/TheFatRat
    chmod +x /opt/TheFatRat/TheFatRat.py
fi

if [ ! -d /opt/Covenant ]; then
    git clone https://github.com/cobbr/Covenant /opt/Covenant
fi

# Set permissions
echo -e "${GREEN}[+] Setting permissions...${NC}"
chmod +x /opt/TheFatRat/TheFatRat.py

# Install additional Python tools
echo -e "${GREEN}[+] Installing additional Python tools...${NC}"
pip3 install git+https://github.com/sherlock-project/sherlock.git
pip3 install git+https://github.com/laramies/theHarvester.git
pip3 install git+https://github.com/aboul3la/Sublist3r.git

# Add ghost-x if available
echo -e "${GREEN}[+] Setting up ghost-x...${NC}"
if [ -f "ghostx.py" ]; then
    chmod +x ghostx.py
    ln -sf $(pwd)/ghostx.py /usr/local/bin/ghostx
fi

# Link hacking_tools.py dan wizard.py
echo -e "${GREEN}[+] Linking shortcuts...${NC}"
if [ -f "hacking_tools.py" ]; then
    chmod +x hacking_tools.py
    ln -sf $(pwd)/hacking_tools.py /usr/local/bin/ht
fi

if [ -f "wizard.py" ]; then
    chmod +x wizard.py
    ln -sf $(pwd)/wizard.py /usr/local/bin/wizard
fi

# Create bash aliases
echo -e "${GREEN}[+] Adding aliases to .bashrc...${NC}"
echo "
# DARK AI VIP ALIASES
alias ht='python3 /usr/local/bin/ht'
alias wizard='python3 /usr/local/bin/wizard'
alias msf='msfconsole'
alias msfvenom='msfvenom'
alias searchsploit='searchsploit'
alias sqlmap='sqlmap'
alias nmap='nmap'
alias masscan='masscan'
alias gobuster='gobuster'
alias ffuf='ffuf'
alias wpscan='wpscan'
alias hashcat='hashcat'
alias john='john'
alias hydra='hydra'
alias aircrack='aircrack-ng'
alias responder='responder'
alias impacket='impacket'
alias bloodhound='bloodhound'
alias sherlock='sherlock'
alias theharvester='theharvester'
" >> ~/.bashrc

source ~/.bashrc

# Done
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ INSTALLASI SELESAI!                                     ║${NC}"
echo -e "${GREEN}║  ${YELLOW}Semua tools telah terinstall${GREEN}                         ║${NC}"
echo -e "${GREEN}║  ${BLUE}Gunakan:${GREEN}                                        ║${NC}"
echo -e "${GREEN}║    - ht [tool] [args]  → Jalankan tool langsung${NC}"
echo -e "${GREEN}║    - wizard            → Menu interaktif${NC}"
echo -e "${GREEN}║    - ghostx            → Ghost-X terminal toolkit${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
