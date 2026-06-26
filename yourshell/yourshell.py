import os
import sys
import time
import shutil

if sys.prefix != sys.base_prefix:
    print("Status: venv is ACTIVE")
else:
    print("Status: venv is NOT active")

def loading(duration=3, width=30):
    cols = shutil.get_terminal_size().columns

    for i in range(width + 1):
        filled = "█" * i
        empty = "░" * (width - i)
        bar = f"[{filled}{empty}]"

        # Tengah horizontal
        padding = max((cols - len(bar)) // 2, 0)

        sys.stdout.write("\r" + " " * padding + bar)
        sys.stdout.flush()

        time.sleep(duration / width)

    print()

loading()

os.system("cls" if os.name == "nt" else "clear")

import subprocess
from pathlib import Path
import platform
import socket
import getpass

password = "root"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
WHITE = "\033[37m"

try:
    import readline
    # This automatically enables standard arrow-key history for input()
    readline.parse_and_bind("tab: complete")
except ImportError:
    # On Windows, basic arrow key history is usually supported natively, 
    # but if you are on a unique terminal, you might need 'pip install pyreadline3'
    pass

# 1. Print the logo ONCE at startup, not inside the loop
logo = rf"""

$$\     $$\                             $$$$$$\  $$\                 $$\ $$\ ©
\$$\   $$  |                           $$  __$$\ $$ |                $$ |$$ |
 \$$\ $$  /$$$$$$\  $$\   $$\  $$$$$$\ $$ /  \__|$$$$$$$\   $$$$$$\  $$ |$$ |
  \$$$$  /$$  __$$\ $$ |  $$ |$$  __$$\\$$$$$$\  $$  __$$\ $$  __$$\ $$ |$$ |
   \$$  / $$ /  $$ |$$ |  $$ |$$ |  \__|\____$$\ $$ |  $$ |$$$$$$$$ |$$ |$$ |
    $$ |  $$ |  $$ |$$ |  $$ |$$ |     $$\   $$ |$$ |  $$ |$$   ____|$$ |$$ |
    $$ |  \$$$$$$  |\$$$$$$  |$$ |     \$$$$$$  |$$ |  $$ |\$$$$$$$\ $$ |$$ |
    \__|   \______/  \______/ \__|      \______/ \__|  \__| \_______|\__|\__|
"""
print(logo)

w = """
YourShell 1.0v

A lightweight custom shell written in Python.

Features:
- Custom prompt
- Virtual environment detection
- Command history
- Tab completion
- FDEL integration
- Package manager wrapper

"""

q = """
YourShell Help

Built-in Commands:
  cd <path>         Change directory
  clear             Clear terminal
  infodevice        Show system information
  logoys            Show YourShell logo
  help              Show this help
  about             About YourShell
  history           Show command history
  venvcheck         Check virtual environment
  exit              Exit YourShell

FDEL:
  fdel explore <path>
  fdel stats <path>
  fdel find <path> <pattern>
  fdel pkg install <package>
  fdel pkg update
  fdel pkg upgrade
"""

def is_root():
    try:
        # Works on Linux and macOS
        return os.getuid() == 0
    except AttributeError:
        # Fallback for Windows
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

def check_venv():
    if sys.prefix != sys.base_prefix:
        print("Status: venv is ACTIVE")
    else:
        print("Status: venv is NOT active")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

import sys
import tty
import termios

def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)

    password = ""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)

        while True:
            ch = sys.stdin.read(1)

            if ch in ("\n", "\r"):
                break

            elif ch == "\x7f":  # Backspace
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)

            else:
                password += ch
                print("*", end="", flush=True)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    print()
    return password

def info():
    print("user      :", getpass.getuser())
    print("Shell     : YourShell")
    print("OS        :", platform.system())      # Windows/Linux
    print("OS version:", platform.release())     # versi
    print("OS detail :", platform.version())     # detail
    print("Host      :", socket.gethostname())
    print("Kernel    :", platform.release())
    print("YS Version: 1.0v")
    print("Logo      : YourShell Logo")
    print("CPU       :", get_cpu_info()["brand_raw"])
    ram = psutil.virtual_memory()
    print("Memory    :", f"{ram.total / (1024**3):.2f} GB")
    for gpu in GPUtil.getGPUs():
        print("GPU       :", gpu.name)
    print("Terminal  :", os.environ.get("TERM"))
    print("Packages  :",
        subprocess.check_output(
            ["dpkg", "--get-selections"],
            text=True
        ).count("\n")
    )
    print("WM        :", os.environ.get("XDG_CURRENT_DESKTOP"))

HISTORY_FILE = ".ys_history"

try:
    if Path(HISTORY_FILE).exists():
        readline.read_history_file(HISTORY_FILE)
except:
    pass

# Main CLI Loop
while True:
    cwd = Path.cwd()
    
    # --- COMPACT PATH FORMATTING ---
    # Grab the last two parts of the path (e.g., 'project' and 'a') if they exist
    if len(cwd.parts) > 1:
        display_path = f"{cwd.parts[-2]}/{cwd.parts[-1]}"
    else:
        display_path = cwd.name if cwd.name else str(cwd)
    
    symbol = "/>"
    pin = f"{GREEN}(root){RESET}" if is_root() else ""
    color = RED if is_root() else GREEN

    # Dynamically build prompt based on venv status
    if sys.prefix != sys.base_prefix:
        prompt = f"{color}{pin}{WHITE}(venv){RESET}{color}{display_path}{symbol}{RESET}"
    else:
        prompt = f"{color}{pin}{color}{display_path}{symbol}{RESET}"
    # -------------------------------

    # Catching Ctrl+C or Ctrl+D cleanly so it doesn't throw a messy traceback
    try:
        cmd = input(prompt).strip()
        try:
            readline.write_history_file(HISTORY_FILE)
        except:
            pass

    except (KeyboardInterrupt, EOFError):
        print("\nExiting shell.")
        sys.exit()

    # Skip empty inputs
    if not cmd:
        continue

    # 3. Handle built-in commands properly
    if cmd == "yscd" or cmd.startswith("yscd "):
        # Split into ['cd', 'target_path'] limiting to 1 split for paths with spaces
        parts = cmd.split(maxsplit=1)
        
        # If user just types 'cd' without arguments, default to their User Home directory
        target_dir = parts[1] if len(parts) > 1 else str(Path.home())
        
        try:
            os.chdir(target_dir)
        except FileNotFoundError:
            print(f"Error: The system cannot find the path specified: '{target_dir}'")
        except Exception as e:
            print(f"Error: {e}")
        continue  # Skips subprocess execution and restarts the loop at the new path

    if cmd == "ysvenvcheck":
        check_venv()

    elif cmd == "ysunvenv":
        if sys.prefix != sys.base_prefix:
            print("System: To deactivate this venv, type 'exit' to leave this custom shell, then type 'deactivate'.")
        else:
            print("Status: venv is not active anyway.")

    elif cmd in ["ysexit", "ysbash"]:  # Fixed the logical 'or' evaluation bug
        print("Exiting custom shell.")
        sys.exit()

    elif cmd == "ysinfodevice":
        tes = rf"""
$$\     $$\  $$$$$$\  
\$$\   $$  |$$  __$$\ 
 \$$\ $$  / $$ /  \__|
  \$$$$  /  \$$$$$$\  
   \$$  /    \____$$\ 
    $$ |    $$\   $$ |
    $$ |    \$$$$$$  |
    \__|     \______/ 
Your             Shell
"""
        if sys.prefix != sys.base_prefix:
            from cpuinfo import get_cpu_info
            import psutil
            import GPUtil
            print(tes)
            info()
        else:
            print("venv required")

    elif cmd == "ysdfp":
        if Path("dfp").is_dir():
            subprocess.run(["python3", "dfp/main.py"])
        else:
            print("dfp not found")

    elif cmd == "yslogo":
        print(logo)

    elif cmd.startswith("fdel"):
        args = cmd.split()[1:]

        subprocess.run(
            ["python", "-m", "fdel.cli", *args],
            cwd="fdel"
        )

    elif cmd == "ysclear":
        clear()

    elif cmd == "yshelp":
        print(q)

    elif cmd == "ysabout":
        print(w)

    elif cmd == "yshistory":
        for i in range(
            1,
            readline.get_current_history_length() + 1
        ):
            print(
                f"{i}: {readline.get_history_item(i)}"
            )

    elif cmd == "ysver":
        print("YourShell 1.0v")

    elif cmd == "yswhoami":
        print(getpass.getuser())

    elif cmd == "yspwd":
        print(Path.cwd())

    elif cmd == "ysGhost-x":
        e = input_password()
        if e == password:
            clear()
            loading()
            subprocess.run(["python3", "lock/ghostx.py"])
        else:
            print("Access Denied")

    elif cmd == "ysGhost-m":
        if is_root():
            e = input_password()
            if e == password:
                clear()
                loading()
                subprocess.run(["python3", "lock/ghostm.py"])
            else:
                print("Access Denied")
        else:
            print("ROOT REQUIED")

    elif cmd == "ysGhost-v":
        r = input_password()
        if r == password:
            clear()
            loading()
            subprocess.run(["python3", "lock/wizard.py"])
        else:
            print("Access Denied")

    elif cmd == "ysGhost-v-install":
        if is_root():
            t = input_password()
            if t == password:
                subprocess.run(["bash", "lock/install_all.sh"])
        else:
            print("Root Requied")

    elif cmd == "ysGhost":
        gtw = """
1. ysGhost     show secret command
2. ysGhost-x   not for mobile
3. ysGhost-m   for mobile and everyone
4. ysGhost-v   all in one
"""
        print(gtw)

    elif cmd == "exit":
        print("you mean ysexit?")

    elif cmd == "ysGhost-how":
        subprocess.run(["python3", "lock/how.py"])

    elif cmd.startswith("fdel"):
        subprocess.run(cmd, shell=True)

    else:
        try:
            subprocess.run(cmd, shell=True)
        except KeyboardInterrupt:
            print("\nCommand interrupted.")
