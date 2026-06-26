a = """
# ============================================
# Ghost-X - Terminal Hacking Toolkit
# Requirements File
# ============================================
#
# Install with: pip install -r requirements.txt
# Run with: python3 ghostx.py
#
# Note: Most tools (nmap, sqlmap, hydra, etc.)
# need to be installed via your package manager:
#   apt install nmap sqlmap hydra john nikto dirb
# ============================================

# DNS resolution for DNS Lookup tool
dnspython>=2.0.0

# Optional - uncomment if you want better colors
# colorama>=0.4.0

# Optional - uncomment for better terminal handling
# prompt-toolkit>=3.0.0

# ============================================
# For Termux users:
#   pkg install python nmap sqlmap hydra john nikto dirb
#   pip install -r requirements.txt
# ============================================
"""
print(a)
