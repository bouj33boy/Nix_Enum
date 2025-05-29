import subprocess
import os
import pwd
import grp

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        return "[ERROR] Command failed or permission denied."

def is_root():
    return os.geteuid() == 0

def user_info():
    print("\n[+] Current User Info")
    print("======================")
    user = pwd.getpwuid(os.getuid()).pw_name
    groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
    print(f"User: {user}")
    print(f"Groups: {', '.join(groups) if groups else '[None listed]'}")

enum_steps = {
    "OS Version": "cat /etc/os-release",
    "PATH Variable": "echo $PATH",
    "Environment Variables": "env",
    "Kernel Version": "uname -a",
    "CPU Info": "lscpu",
    "Root Processes": "ps aux | grep root",
    "All Processes": "ps au",
    "Login Shells": "cat /etc/shells",
    "Routing Table": "route -n || netstat -rn",
    "DNS Resolver Config": "cat /etc/resolv.conf",
    "Home Directory Listing": "ls -la /home",
    "All Groups": "cat /etc/group",
    "Sudo Group Members": "getent group sudo",
    "SSH Directory": "ls -l ~/.ssh",
    "Bash History": "history",
    "Sudo Privileges": "sudo -l",
    "Groups": "groups",
    "Readable Shadow File": "ls -l /etc/shadow",
    "User Info (/etc/passwd)": "cat /etc/passwd",
    "Login Shell Users": "grep '/bin/bash' /etc/passwd",
    "Cron Jobs (Daily)": "ls -la /etc/cron.daily/",
    "Block Devices": "lsblk",
    "Printers": "lpstat -p",
    "fstab (mount info)": "cat /etc/fstab",
    "Mounted Drives": "df -h",
    "Writable Directories": "find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null",
    "Writable Files": "find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null",
    "Hidden Files": "find / -type f -name '.*' -exec ls -l {} \\; 2>/dev/null",
    "Hidden Directories": "find / -type d -name '.*' -ls 2>/dev/null",
    "Temp Directory Contents": "ls -l /tmp /var/tmp /dev/shm"
}

def enumerate_system():
    user_info()
    print("\n[!] Privilege Check")
    print("====================")
    print("Running as root." if is_root() else "Running as non-root user. Some commands may be restricted.")

    for title, cmd in enum_steps.items():
        print(f"\n[+] {title}")
        print("=" * (len(title) + 5))
        output = run_cmd(cmd)
        print(output)

if __name__ == "__main__":
    enumerate_system()
