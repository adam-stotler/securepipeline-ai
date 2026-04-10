"""
CodeQL verification target — intentional CWE-78 (Command Injection).
DELETE THIS FILE before any production milestone.
This exists solely to verify the SAST gate catches shell injection.
"""
import subprocess
import os

def scan_target(target_host: str) -> str:
    """
    INTENTIONALLY VULNERABLE: user input flows directly into shell command.
    CodeQL should flag this as a command injection (CWE-78).
    """
    # BAD: shell=True + unsanitized input = injection sink
    result = subprocess.run(
        f"ping -c 1 {target_host}",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout


def read_report(report_name: str) -> str:
    """
    INTENTIONALLY VULNERABLE: path traversal (CWE-22).
    CodeQL should flag user-controlled input reaching open().
    """
    # BAD: no path sanitization — attacker passes "../../etc/passwd"
    with open(os.path.join("reports", report_name), "r") as f:
        return f.read()