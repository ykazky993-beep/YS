#!/usr/bin/env python3

import os
import sys
import time
import shutil
import subprocess
import platform
import socket
import getpass
import shlex
import signal
import threading
import queue
import pty
import termios
import fcntl
import struct
import select
import re
import glob
import fnmatch
import tempfile
import tty
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
import itertools

# ============================================================
# GLOBAL CONFIG
# ============================================================
HISTORY_FILE = ".ys_history"
LOG_FILE = ".ys_log"
ALIAS_FILE = ".ys_aliases"
ENV_FILE = ".ys_env"
password = "root" #deffault password
# ys logo info device
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

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
BG = "\033[49m"

# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def is_root() -> bool:
    try:
        return os.geteuid() == 0
    except AttributeError:
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

def info_general():
    print("User      :", getpass.getuser())
    print("Shell     : YourShell")
    print("Host      :", socket.gethostname())

    print("OS        :", platform.system())
    print("OS Version:", platform.release())
    print("OS Detail :", platform.version())
    print("Machine   :", platform.machine())
    print("Processor :", platform.processor())

    print("Kernel    :", platform.release())
    print("Python    :", platform.python_version())
    print("Terminal  :", os.environ.get("TERM", "Unknown"))
    print("YS Version: 1.0v")

    total, used, free = shutil.disk_usage("/")
    print("Storage   :", f"{used//(1024**3)} GB / {total//(1024**3)} GB")

    try:
        pkg = subprocess.check_output(
            ["dpkg", "--get-selections"],
            text=True
        ).count("\n")
        print("Packages  :", pkg)
    except:
        pass

    try:
        print("WM        :", os.environ.get("XDG_CURRENT_DESKTOP", "Unknown"))
    except:
        pass

def info_droid():

    def prop(name):
        try:
            return subprocess.check_output(
                ["getprop", name],
                text=True
            ).strip()
        except:
            return "Unknown"

    print("Brand     :", prop("ro.product.brand"))
    print("Model     :", prop("ro.product.model"))
    print("Device    :", prop("ro.product.device"))
    print("Android   :", prop("ro.build.version.release"))
    print("SDK       :", prop("ro.build.version.sdk"))
    print("ABI       :", prop("ro.product.cpu.abi"))

    try:
        with open("/proc/meminfo") as f:
            mem = int(f.readline().split()[1]) // 1024
            print("Memory    :", f"{mem} MB")
    except:
        pass

    total, used, free = shutil.disk_usage("/")
    print("Storage   :", f"{used//(1024**3)} GB / {total//(1024**3)} GB")

    try:
        uptime = subprocess.check_output(
            ["uptime"],
            text=True
        ).strip()
        print("Uptime    :", uptime)
    except:
        pass

    try:
        cpu = subprocess.check_output(
            ["uname", "-m"],
            text=True
        ).strip()
        print("CPU Arch  :", cpu)
    except:
        pass

def loading(duration=1.5, width=30):
    cols = shutil.get_terminal_size().columns
    for i in range(width + 1):
        filled = "█" * i
        empty = "░" * (width - i)
        bar = f"[{filled}{empty}]"
        padding = max((cols - len(bar)) // 2, 0)
        sys.stdout.write("\r" + " " * padding + bar)
        sys.stdout.flush()
        time.sleep(duration / width)
    print()

def clear():
    os.system("cls" if os.name == "nt" else "clear")
clear()

def input_password(prompt="Password: ") -> str:
    print(prompt, end="", flush=True)
    password = ""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)  # cbreak
        while True:
            ch = sys.stdin.read(1)
            if ch in ("\n", "\r"):
                break
            elif ch == "\x7f" or ch == "\b":  # Backspace
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

def get_cpu_info():
    try:
        from cpuinfo import get_cpu_info
        return get_cpu_info()
    except Exception:
        return {"brand_raw": platform.processor() or "Unknown"}

# ============================================================
# MAIN SHELL CLASS
# ============================================================
class YourShell:
    def __init__(self):
        self.history = []
        self.history_file = Path(HISTORY_FILE)
        self.log_file = Path(LOG_FILE)
        self.alias_file = Path(ALIAS_FILE)
        self.env_file = Path(ENV_FILE)
        self.aliases = {}
        self.env = os.environ.copy()
        self.jobs = {}   # job_id -> (process, command)
        self.job_counter = 0
        self.running = True
        self.prompt_color = GREEN

        # Load history, aliases, env
        self.load_history()
        self.load_aliases()
        self.load_env()

        # Setup readline
        try:
            import readline
            readline.set_completer(self.completer)
            readline.parse_and_bind("tab: complete")
            readline.set_history_length(1000)
        except ImportError:
            pass

        # BANNER
        self.show_banner()

    # ------------------------------
    # LOAD / SAVE PERSISTENCE
    # ------------------------------
    def load_history(self):
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    for line in f:
                        self.history.append(line.strip())
        except Exception:
            pass

    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                for cmd in self.history[-500:]:
                    f.write(cmd + "\n")
        except Exception:
            pass

    def load_aliases(self):
        try:
            if self.alias_file.exists():
                with open(self.alias_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, val = line.strip().split('=', 1)
                            self.aliases[key] = val
        except Exception:
            pass

    def save_aliases(self):
        try:
            with open(self.alias_file, 'w') as f:
                for k, v in self.aliases.items():
                    f.write(f"{k}={v}\n")
        except Exception:
            pass

    def load_env(self):
        try:
            if self.env_file.exists():
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            k, v = line.strip().split('=', 1)
                            self.env[k] = v
        except Exception:
            pass

    def save_env(self):
        try:
            with open(self.env_file, 'w') as f:
                for k, v in self.env.items():
                    f.write(f"{k}={v}\n")
        except Exception:
            pass

    # ------------------------------
    # BANNER
    # ------------------------------
    def show_banner(self):
        logo = rf"""
{RED}
$$\     $$\                             $$$$$$\  $$\                 $$\ $$\  $$$$$$\  $$\                             $$     
\$$\   $$  |                           $$  __$$\ $$ |                $$ |$$ |$$  __$$\ $$ |                            $$ |    
 \$$\ $$  /$$$$$$\  $$\   $$\  $$$$$$\ $$ /  \__|$$$$$$$\   $$$$$$\  $$ |$$ |$$ /  \__|$$$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$\   
  \$$$$  /$$  __$$\ $$ |  $$ |$$  __\\$$$$$$$$\  $$  __$$\ $$  __$$\ $$ |$$ |$$ |$$$$\ $$  __$$\ $$  __$$\ $$  _____|\_$$  _|  
   \$$  / $$ /  $$ |$$ |  $$ |$$ |  \__|\____$$\ $$ |  $$ |$$$$$$$$ |$$ |$$ |$$ |\_$$ |$$ |  $$ |$$ /  $$ |\$$$$$$\    $$ |    
    $$ |  $$ |  $$ |$$ |  $$ |$$ |     $$\   $$ |$$ |  $$ |$$   ____|$$ |$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ | \____$$\   $$ |$$\ 
    $$ |  \$$$$$$  |\$$$$$$  |$$ |     \$$$$$$  |$$ |  $$ |\$$$$$$$\ $$ |$$ |\$$$$$$  |$$ |  $$ |\$$$$$$  |$$$$$$$  |  \$$$$  |
    \__|   \______/  \______/ \__|      \______/ \__|  \__| \_______|\__|\__| \______/ \__|  \__| \______/ \_______/    \____/ 
{RESET}
"""
        print(logo)
        print(f"{GREEN}{BOLD}YourShell 2.0 – By ykazky993-beep{RESET}")
        print(f"{CYAN}Type 'yshelp' for commands, 'ysabout' for info.{RESET}\n")

    # ------------------------------
    # PROMPT
    # ------------------------------
    def get_prompt(self):
        cwd = Path.cwd()
        # compact path
        if len(cwd.parts) > 2:
            display = f"{cwd.parts[-2]}/{cwd.parts[-1]}"
        else:
            display = cwd.name if cwd.name else str(cwd)
        color = RED if is_root() else GREEN
        root_tag = f"{RED}(root){RESET}" if is_root() else ""
        venv_tag = f"{WHITE}(venv){RESET}" if sys.prefix != sys.base_prefix else ""
        prompt = f"{color}{root_tag}{venv_tag}{color}{display}{RESET} {CYAN}/>{RESET} "
        return prompt

    # ------------------------------
    # COMPLETER
    # ------------------------------
    def completer(self, text, state):
        # Command completion
        builtins = [cmd for cmd in dir(self) if cmd.startswith('cmd_')]
        builtins = [c[4:] for c in builtins]  # remove 'cmd_'
        builtins += ['ys' + c for c in builtins]  # with ys prefix
        builtins += ['fdel', 'exit', 'help', 'about']
        options = [c for c in builtins if c.startswith(text)]
        # Also file/dir completion
        if not options and text:
            files = glob.glob(text + '*')
            options = files
        # Also environment variables
        if text.startswith('$'):
            env_vars = [f"${k}" for k in self.env.keys() if k.startswith(text[1:])]
            options = env_vars
        try:
            return options[state]
        except IndexError:
            return None

    # ------------------------------
    # PARSING (PIPE, REDIR, BG, EXPAND)
    # ------------------------------
    def parse_command(self, raw: str) -> Dict:
        """Parsing command with pipes, redirection, background, env expansion."""
        raw = raw.strip()
        if not raw:
            return None

        # Expand aliases
        parts = shlex.split(raw)
        if parts and parts[0] in self.aliases:
            alias_cmd = self.aliases[parts[0]]
            if len(parts) > 1:
                raw = alias_cmd + " " + " ".join(parts[1:])
            else:
                raw = alias_cmd

        # Expand environment variables $VAR and $(cmd)
        def expand_env(match):
            var = match.group(1)
            if var.startswith('('):
                # $(command)
                cmd = var[1:-1]
                try:
                    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True).strip()
                    return result
                except Exception:
                    return ''
            else:
                return self.env.get(var, '')
        raw = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*|\([^)]+\))', expand_env, raw)

        # Split on pipes
        pipe_segments = raw.split('|')
        commands = []
        for seg in pipe_segments:
            seg = seg.strip()
            # Check for redirection and background
            bg = False
            if seg.endswith('&'):
                bg = True
                seg = seg[:-1].strip()
            # Redirection: >, >>, <
            stdout_redir = None
            stderr_redir = None
            stdin_redir = None
            append = False

            # Parse >>
            if '>>' in seg:
                seg, stdout_redir = seg.split('>>', 1)
                stdout_redir = stdout_redir.strip()
                append = True
            # Parse >
            elif '>' in seg:
                seg, stdout_redir = seg.split('>', 1)
                stdout_redir = stdout_redir.strip()
            # Parse <
            if '<' in seg:
                seg, stdin_redir = seg.split('<', 1)
                stdin_redir = stdin_redir.strip()

            # Tokenize command
            args = shlex.split(seg)
            if not args:
                continue
            cmd = args[0]
            cmd_args = args[1:]

            commands.append({
                'cmd': cmd,
                'args': cmd_args,
                'stdin': stdin_redir,
                'stdout': stdout_redir,
                'stderr': stderr_redir,
                'append': append,
                'bg': bg
            })

        return {
            'pipeline': commands,
            'bg': any(c['bg'] for c in commands) if commands else False
        }

    # ------------------------------
    # EXECUTION ENGINE
    # ------------------------------
    def execute_pipeline(self, parsed: Dict, raw_cmd: str = ""):
        if not parsed:
            return
        pipeline = parsed['pipeline']
        bg = parsed['bg']

        procs = []
        opened_files = []
        prev_stdout_pipe = None

        for i, cmd_info in enumerate(pipeline):
            cmd = cmd_info['cmd']
            args = cmd_info['args']
            stdin_redir = cmd_info['stdin']
            stdout_redir = cmd_info['stdout']
            append = cmd_info['append']

            if cmd.startswith('ys'):
                builtin = cmd[2:]
                builtin = builtin.replace('-', '_')
                if hasattr(self, f'cmd_{builtin}'):
                    if len(pipeline) > 1:
                        print(f"{RED}Error: Built-in '{cmd}' tidak bisa dipipe{RESET}")
                        return
                    func = getattr(self, f'cmd_{builtin}')
                    func(*args)
                    return
            elif cmd == 'fdel':
                if len(pipeline) > 1:
                    print(f"{RED}Error: fdel tidak bisa dipipe{RESET}")
                    return
                subprocess.run(["python", "-m", "fdel.cli"] + args, cwd="fdel")
                return

            # External command
            try:
                if stdin_redir:
                    stdin_fd = open(stdin_redir, 'r')
                    opened_files.append(stdin_fd)
                elif prev_stdout_pipe is not None:
                    stdin_fd = prev_stdout_pipe
                elif i == 0:
                    stdin_fd = sys.stdin
                else:
                    stdin_fd = None

                is_last = (i == len(pipeline) - 1)
                if stdout_redir:
                    mode = 'a' if append else 'w'
                    stdout_fd = open(stdout_redir, mode)
                    opened_files.append(stdout_fd)
                elif not is_last:
                    stdout_fd = subprocess.PIPE
                else:
                    stdout_fd = sys.stdout

                use_setsid = bg and os.name != 'nt'

                proc = subprocess.Popen(
                    [cmd] + args,
                    stdin=stdin_fd,
                    stdout=stdout_fd,
                    stderr=subprocess.PIPE,
                    text=True,
                    preexec_fn=os.setsid if use_setsid else None
                )
                procs.append(proc)

                if prev_stdout_pipe is not None:
                    prev_stdout_pipe.close()

                prev_stdout_pipe = proc.stdout if stdout_fd == subprocess.PIPE else None

            except FileNotFoundError:
                print(f"{RED}Command not found: {cmd}{RESET}")
                for f in opened_files:
                    f.close()
                return
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
                for f in opened_files:
                    f.close()
                return

        # If background, detach
        if bg:
            self.job_counter += 1
            job_id = self.job_counter
            self.jobs[job_id] = (procs, raw_cmd)
            print(f"{YELLOW}[{job_id}] Background job started: {raw_cmd}{RESET}")
            for f in opened_files:
                try:
                    f.close()
                except Exception:
                    pass
            return

        # Wait for all processes
        for p in procs:
            try:
                p.wait()
            except Exception:
                pass

        # Show stderr if any
        for p in procs:
            if p.stderr:
                err = p.stderr.read()
                if err:
                    print(f"{RED}{err}{RESET}")

    # ------------------------------
    # BUILT-IN COMMANDS
    # ------------------------------

    # --- Core ---
    def cmd_cd(self, path: str = ""):
        target = path or str(Path.home())
        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"cd: no such file or directory: {target}")
        except Exception as e:
            print(f"cd: {e}")

    def cmd_clear(self):
        clear()

    def cmd_exit(self):
        self.running = False
        print("Exiting shell.")

    def cmd_help(self):
        help_text = f"""
Built-in Commands (prefix 'ys'):
Ghost features
piping, redirection, background jobs, environment variables,
aliases, auto-completion, history, multi-line input, colored prompt

type 'yshelp-full' for full command list.
"""
        print(help_text)

    def cmd_help_full(self):
        help_text = rf"""
{YELLOW}YourShell Help – Overpower Edition{RESET}

{BOLD}Built-in Commands (prefix 'ys'):{RESET}
  {GREEN}cd{RESET}          Change directory
  {GREEN}clear{RESET}       Clear terminal
  {GREEN}exit{RESET}        Exit shell
  {GREEN}help{RESET}        Show this help
  {GREEN}about{RESET}       About YourShell
  {GREEN}history{RESET}     Show command history
  {GREEN}alias{RESET}       List/set aliases
  {GREEN}unalias{RESET}     Remove alias
  {GREEN}env{RESET}         Show environment variables
  {GREEN}setenv{RESET}      Set environment variable
  {GREEN}unsetenv{RESET}    Unset environment variable
  {GREEN}echo{RESET}        Print arguments
  {GREEN}date{RESET}        Show date/time
  {GREEN}whoami{RESET}      Show current user
  {GREEN}pwd{RESET}         Print working directory
  {GREEN}ls{RESET}          List files (with -l, -a)
  {GREEN}cat{RESET}         Display file content
  {GREEN}head{RESET}        First lines of file
  {GREEN}tail{RESET}        Last lines of file
  {GREEN}grep{RESET}        Search text in files
  {GREEN}find{RESET}        Find files
  {GREEN}ps{RESET}          List processes
  {GREEN}kill{RESET}        Kill process
  {GREEN}ping{RESET}        Ping host
  {GREEN}curl{RESET}        HTTP client
  {GREEN}wget{RESET}        Download file
  {GREEN}zip{RESET}         Zip files
  {GREEN}unzip{RESET}       Unzip files
  {GREEN}chmod{RESET}       Change file permissions
  {GREEN}chown{RESET}       Change file owner
  {GREEN}mkdir{RESET}       Create directory
  {GREEN}rm{RESET}          Remove file/dir
  {GREEN}mv{RESET}          Move/rename file
  {GREEN}cp{RESET}          Copy file
  {GREEN}df{RESET}          Disk free
  {GREEN}du{RESET}          Disk usage
  {GREEN}free{RESET}        Memory usage
  {GREEN}uptime{RESET}      System uptime
  {GREEN}who{RESET}         Logged-in users
  {GREEN}last{RESET}        Last logins
  {GREEN}jobs{RESET}        List background jobs
  {GREEN}fg{RESET}          Bring job to foreground
  {GREEN}bg{RESET}          Resume job in background

{BLUE}Ghost commands:{RESET}
  {PURPLE}ysGhost{RESET}
  {PURPLE}ysGhost-x{RESET}
  {PURPLE}ysGhost-m{RESET}
  {PURPLE}ysGhost-v{RESET}
  {PURPLE}ysGhost-install{RESET}
  {PURPLE}ysGhost-how{RESET}

{CYAN}Features:{RESET}
  - Piping (|), redirection (>, >>, <)
  - Background jobs (&)
  - Environment variables ($VAR, $(cmd))
  - Aliases
  - Auto-completion (TAB)
  - History (↑↓)
  - Multi-line input (ending with \)
  - Colored prompt
""".format(RED=RED, GREEN=GREEN, YELLOW=YELLOW, BLUE=BLUE, PURPLE=PURPLE, CYAN=CYAN, WHITE=WHITE, BOLD=BOLD, RESET=RESET)
        print(help_text)

    def cmd_about(self):
        about = """
{YELLOW}YourShell 2.0 – Overpower Edition{RESET}
{CYAN}Lightweight custom shell written in Python{RESET}
{BOLD}Features:{RESET}
  - Banyak built-in command (file, proses, network, kompresi, dll)
  - Piping, redirection, background jobs
  - Aliases, environment variables
  - Auto-completion, history
  - Multi-line input
{GREEN}Version: 2.0{RESET}
""".format(RED=RED, GREEN=GREEN, YELLOW=YELLOW, BLUE=BLUE, PURPLE=PURPLE, CYAN=CYAN, WHITE=WHITE, BOLD=BOLD, RESET=RESET)
        print(about)

    # --- History ---
    def cmd_history(self):
        for i, cmd in enumerate(self.history[-50:], 1):
            print(f"{i}: {cmd}")

    # --- Aliases ---
    def cmd_alias(self, *args):
        if not args:
            for k, v in self.aliases.items():
                print(f"{k}='{v}'")
        else:
            name = args[0]
            if len(args) > 1:
                value = " ".join(args[1:])
                self.aliases[name] = value
                self.save_aliases()
            else:
                if name in self.aliases:
                    print(f"{name}='{self.aliases[name]}'")
                else:
                    print(f"Alias '{name}' not found")

    def cmd_unalias(self, name: str):
        if name in self.aliases:
            del self.aliases[name]
            self.save_aliases()

    # --- Environment ---
    def cmd_env(self):
        for k, v in self.env.items():
            print(f"{k}={v}")

    def cmd_setenv(self, key: str, value: str):
        self.env[key] = value
        self.save_env()

    def cmd_unsetenv(self, key: str):
        if key in self.env:
            del self.env[key]
            self.save_env()

    # --- Echo ---
    def cmd_echo(self, *args):
        print(" ".join(args))

    # --- Date ---
    def cmd_date(self):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # --- User ---
    def cmd_whoami(self):
        print(getpass.getuser())

    def cmd_pwd(self):
        print(Path.cwd())

    # --- File Operations ---
    def cmd_ls(self, *args):
        path = "."
        flags = []
        for a in args:
            if a.startswith('-'):
                flags.append(a)
            else:
                path = a
        try:
            files = sorted(os.listdir(path))
            if '-l' in flags:
                for f in files:
                    st = os.stat(os.path.join(path, f))
                    print(f"{st.st_mode:o} {st.st_size:8d} {datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M')} {f}")
            else:
                if '-a' in flags:
                    print(" ".join(files))
                else:
                    print(" ".join([f for f in files if not f.startswith('.')]))
        except Exception as e:
            print(f"ls: {e}")

    def cmd_cat(self, *files):
        for f in files:
            try:
                with open(f, 'r') as fp:
                    print(fp.read(), end='')
            except Exception as e:
                print(f"cat: {e}")

    def cmd_head(self, file: str, n: str = "10"):
        try:
            with open(file, 'r') as fp:
                for i, line in enumerate(fp):
                    if i >= int(n):
                        break
                    print(line, end='')
        except Exception as e:
            print(f"head: {e}")

    def cmd_tail(self, file: str, n: str = "10"):
        try:
            with open(file, 'r') as fp:
                lines = fp.readlines()
                for line in lines[-int(n):]:
                    print(line, end='')
        except Exception as e:
            print(f"tail: {e}")

    def cmd_grep(self, pattern: str, *files):
        try:
            for f in files:
                with open(f, 'r') as fp:
                    for line in fp:
                        if re.search(pattern, line):
                            print(f"{f}: {line}", end='')
        except Exception as e:
            print(f"grep: {e}")

    def cmd_find(self, path: str, pattern: str = "*"):
        try:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if glob.fnmatch.fnmatch(f, pattern):
                        print(os.path.join(root, f))
        except Exception as e:
            print(f"find: {e}")

    def cmd_mkdir(self, *dirs):
        for d in dirs:
            try:
                os.makedirs(d, exist_ok=True)
            except Exception as e:
                print(f"mkdir: {e}")

    def cmd_rm(self, *files):
        for f in files:
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
            except Exception as e:
                print(f"rm: {e}")

    def cmd_mv(self, src: str, dst: str):
        try:
            shutil.move(src, dst)
        except Exception as e:
            print(f"mv: {e}")

    def cmd_cp(self, src: str, dst: str):
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            print(f"cp: {e}")

    def cmd_chmod(self, mode: str, *files):
        for f in files:
            try:
                os.chmod(f, int(mode, 8))
            except Exception as e:
                print(f"chmod: {e}")

    def cmd_chown(self, owner: str, *files):
        # Only for Unix
        try:
            import pwd
            uid = pwd.getpwnam(owner).pw_uid
            for f in files:
                os.chown(f, uid, -1)
        except Exception as e:
            print(f"chown: {e}")

    def cmd_ln(self, src: str, dst: str):
        try:
            os.symlink(src, dst)
        except Exception as e:
            print(f"ln: {e}")

    # --- System Info ---
    def cmd_df(self):
        try:
            for part in Path('/').iterdir():
                if part.is_mount():
                    usage = shutil.disk_usage(part)
                    print(f"{str(part):10} {usage.total >> 30:4}G  {usage.used >> 30:4}G  {usage.free >> 30:4}G")
        except Exception:
            print("df not available on this system")

    def cmd_du(self, path: str = "."):
        try:
            total = 0
            for root, dirs, files in os.walk(path):
                for f in files:
                    total += os.path.getsize(os.path.join(root, f))
            print(f"{total >> 20} MB")
        except Exception as e:
            print(f"du: {e}")

    def cmd_free(self):
        try:
            import psutil
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            print(f"Memory: {mem.used >> 30}G / {mem.total >> 30}G")
            print(f"Swap  : {swap.used >> 30}G / {swap.total >> 30}G")
        except Exception:
            print("Install psutil for memory info")

    def cmd_uptime(self):
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_sec = float(f.read().split()[0])
                days = int(uptime_sec // 86400)
                hours = int((uptime_sec % 86400) // 3600)
                mins = int((uptime_sec % 3600) // 60)
                print(f"{days}d {hours}h {mins}m")
        except Exception:
            print("uptime not available")

    def cmd_who(self):
        try:
            for user in os.listdir('/var/run/user'):
                print(f"{user} logged in")
        except Exception:
            print("who not available")

    def cmd_last(self):
        try:
            with open('/var/log/wtmp', 'rb') as f:
                print("Last logins: (use 'last' command if installed)")
        except Exception:
            print("last not available")

    # --- Process ---
    def cmd_ps(self):
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                print(f"{proc.info['pid']:8} {proc.info['name']}")
        except Exception:
            print("Install psutil for process info")

    def cmd_kill(self, pid: str):
        try:
            os.kill(int(pid), signal.SIGTERM)
        except Exception as e:
            print(f"kill: {e}")

    # --- Network ---
    def cmd_ping(self, host: str, count: str = "4"):
        try:
            subprocess.run(["ping", "-c", count, host])
        except Exception:
            print("ping not available")

    def cmd_curl(self, url: str):
        try:
            import requests
        except ImportError:
            print("Install requests for curl (pip install requests)")
            return
        try:
            r = requests.get(url, timeout=15)
            print(r.text)
        except requests.RequestException as e:
            print(f"curl: {e}")

    def cmd_wget(self, url: str, output: str = ""):
        try:
            import requests
        except ImportError:
            print("Install requests for wget (pip install requests)")
            return
        try:
            r = requests.get(url, timeout=15)
            filename = output or url.split('/')[-1] or "downloaded_file"
            with open(filename, 'wb') as f:
                f.write(r.content)
            print(f"Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"wget: {e}")
        except OSError as e:
            print(f"wget: cannot write file: {e}")

    # --- Compression ---
    def cmd_zip(self, archive_name: str, *files):
        try:
            import zipfile as zipfile_mod
        except ImportError:
            print("zip requires the zipfile module (built-in, should not be missing)")
            return
        if not files:
            print("Usage: yszip <archive.zip> <file1> [file2 ...]")
            return
        try:
            with zipfile_mod.ZipFile(archive_name, 'w') as zf:
                for f in files:
                    zf.write(f)
            print(f"Zipped to {archive_name}")
        except Exception as e:
            print(f"zip: {e}")

    def cmd_unzip(self, archive_name: str, extract_to: str = "."):
        try:
            import zipfile as zipfile_mod
        except ImportError:
            print("unzip requires the zipfile module (built-in, should not be missing)")
            return
        try:
            with zipfile_mod.ZipFile(archive_name, 'r') as zf:
                zf.extractall(extract_to)
            print(f"Extracted to {extract_to}")
        except Exception as e:
            print(f"unzip: {e}")

    # --- Jobs ---
    def cmd_jobs(self):
        for jid, (procs, cmd) in self.jobs.items():
            status = "running" if any(p.poll() is None for p in procs) else "done"
            print(f"[{jid}] {status}  {cmd}")

    def cmd_fg(self, job_id: str = None):
        if not job_id:
            # bring last job
            if self.jobs:
                jid = max(self.jobs.keys())
            else:
                print("No jobs")
                return
        else:
            try:
                jid = int(job_id)
            except ValueError:
                print(f"fg: invalid job id: {job_id}")
                return
        if jid not in self.jobs:
            print(f"No such job: {jid}")
            return
        procs, cmd = self.jobs.pop(jid)
        for p in procs:
            try:
                p.wait()
            except Exception:
                pass
        # cleanup

    def cmd_bg(self, job_id: str):
        # resume stopped job (not implemented fully)
        print("bg command not fully implemented, use fg")

    # --- Venv ---
    def cmd_venvcheck(self):
        if sys.prefix != sys.base_prefix:
            print("venv is ACTIVE")
        else:
            print("venv is NOT active")

    def cmd_unvenv(self):
        if sys.prefix != sys.base_prefix:
            print("Type 'exit' to leave shell, then deactivate venv.")
        else:
            print("No venv active")

    # --- Infodevice ---
    def cmd_infodevice(self):
        print(tes)
        if sys.prefix != sys.base_prefix:
            try:
                from cpuinfo import get_cpu_info
                import psutil
                import GPUtil
                print("User      :", getpass.getuser())
                print("Shell     : YourShell 2.0")
                print("OS        :", platform.system())
                print("OS version:", platform.release())
                print("Host      :", socket.gethostname())
                print("Kernel    :", platform.release())
                print("CPU       :", get_cpu_info().get("brand_raw", "Unknown"))
                ram = psutil.virtual_memory()
                print("Memory    :", f"{ram.total / (1024**3):.2f} GB")
                try:
                    for gpu in GPUtil.getGPUs():
                        print("GPU       :", gpu.name)
                except Exception:
                    pass
                print("Terminal  :", os.environ.get("TERM", "unknown"))
            except Exception:
                print("Install cpuinfo, psutil, GPUtil for full info")
        else:
            print("venv required for full info")

    def cmd_infodevice_droid(self):
        print(tes)
        info_droid()
    
    def cmd_infodevice_gen(self):
        print(tes)
        info_general()
    
    def cmd_infodevice_help(self):
        print(tes)
        helep = """
ysinfodevice          #info device (for pc)
ysinfodevice-droid    #info device (for android)
ysinfodevice-gen      #info device (general)
ysinfodevice-help     #show this help
"""
        print(helep)

    # --- DFP ---
    def cmd_dfp(self):
        if Path("dfp").is_dir():
            subprocess.run(["python3", "dfp/main.py"])
        else:
            print("dfp not found")

    # --- Logo ---
    def cmd_logo(self):
        self.show_banner()

    # --- FDEL ---
    def cmd_fdel(self, *args):
        if Path("fdel").is_dir():
            subprocess.run(["python", "-m", "fdel.cli"] + list(args), cwd="fdel")
        else:
            print("fdel not found")

    def cmd_Ghost(self):
        listysg = """
1. ysGhost-x         #Desktop only
2. ysGhost-m         #All device
3. ysGhost-v         #All device
4. ysGhost-install   #Install all dependencies
5. ysGhost-m-noroot  #Run yGhost-m with non root
6. ysGhost-how       #Explaining
7. ysdfp             #Desktop only (in progress update)
"""
        print(listysg)

    def cmd_Ghost_x(self):
        q = input_password()
        if q == password:
            clear()
            loading()
            try:
                subprocess.run(["python3", "lock/ghostx.py"])
            except ModuleNotFoundError:
                print("[!]Some module not found.")
                print("[!]Activate virtual enviroment or use ysGhost-v for all device usage")
        else:
            print("Access denied")

    def cmd_Ghost_m(self):
        if is_root():
            w = input_password()
            if w == password:
                clear()
                loading()
                try:
                    subprocess.run(["python3", "lock/ghostm.py"])
                except ModuleNotFoundError:
                    print("[!]Some module not found")
                    print("[!]Activate virtual enviroment or use ysGhost all device")
            else:
                print("Access denied")
        else:
            print("Root Requied")

    def cmd_Ghost_m_noroot(self):
        w = input_password()
        if w == password:
            clear()
            loading()
            try:
                subprocess.run(["python3", "lock/ghostm.py"])
            except ModuleNotFoundError:
                    print("[!]Some module not found")
                    print("[!]Activate virtual enviroment or use ysGhost all device")
        else:
            print("Access denied")

    def cmd_Ghost_v(self):
        e = input_password()
        if e == password:
            clear()
            loading()
            try:
                subprocess.run(["python3", "lock/wizard.py"])
            except ModuleNotFoundError:
                    print("[!]Some module not found")
                    print("[!]Activate virtual enviroment or use ysGhost all device")
        else:
            print("Access denied")

    def cmd_Ghost_install(self):
        r = input_password()
        if r == password:
            clear()
            loading()
            try:
                subprocess.run(["bash", "lock/install_all.sh"])
            except ModuleNotFoundError:
                    print("[!]Some module not found")
                    print("[!]Activate virtual enviroment or edit the bash file; lock/install_all.sh")
        else:
            print("Access denied")

    def cmd_Ghost_how(self):
        print("some feature can't run in termux because there is a module that is not supported on the cellphone")

    def cmd_cover(self):
        print("Wait For Next Update!")

    # --- Version ---
    def cmd_ver(self):
        print("YourShell 2.0")

    # --- Exit alias ---
    def cmd_bash(self):
        self.running = False
        print("Exiting shell.")

    # ============================================================
    # MAIN LOOP
    # ============================================================
    def run(self):
        while self.running:
            try:
                raw = input(self.get_prompt()).strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break

            if not raw:
                continue

            # Multi-line support (if ends with \)
            while raw.endswith('\\'):
                raw = raw[:-1] + ' ' + input("... ").strip()

            # Save history
            self.history.append(raw)
            self.save_history()

            # Parse and execute
            parsed = self.parse_command(raw)
            if parsed:
                self.execute_pipeline(parsed, raw)

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    # Check root warning
    if not is_root():
        print(f"{YELLOW}Warning: Not running as root. Some commands may fail.{RESET}")

    if sys.prefix == sys.base_prefix:
        print(f"{YELLOW}Warning: Not running in a virtual environment. Some features may be limited.{RESET}")

    shell = YourShell()
    shell.run()
