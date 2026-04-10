"""
CodeQL verification target — FastAPI entry points create real dataflow sources.
DELETE before any production milestone.
"""
import subprocess
import os
from fastapi import FastAPI

app = FastAPI()


@app.get("/scan")
def scan_target(host: str) -> dict:
    """
    CWE-78: HTTP query param flows directly into shell command.
    CodeQL can now trace: HTTP input → subprocess.run(shell=True)
    """
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True
    )
    return {"output": result.stdout}


@app.get("/report")
def read_report(filename: str) -> dict:
    """
    CWE-22: HTTP query param flows into open() without sanitization.
    CodeQL can now trace: HTTP input → open(path)
    """
    with open(os.path.join("reports", filename), "r") as f:
        return {"content": f.read()}