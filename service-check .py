#!/usr/bin/env python3
import os
import socket
import stat
import subprocess
import sys
import time
from pathlib import Path

BASE = Path("/home/labex/project")
SERVICE = BASE / "secret_service.py"
SECRET = BASE / "secret.txt"
LOG = BASE / "access.log"

def check_token():
    proc = subprocess.Popen(
        [sys.executable, str(SERVICE), "--host", "127.0.0.1", "--port", "8081"],
        cwd=BASE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1)
        no_token = subprocess.run(
            ["curl", "-s", "-o", "/tmp/no-token.txt", "-w", "%{http_code}", "http://127.0.0.1:8081/secret"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        with_token = subprocess.run(
            ["curl", "-s", "-H", "X-Access-Token: lab-token-2026", "http://127.0.0.1:8081/secret"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        if no_token != "403":
            print(f"token: expected 403 without token, got {no_token}")
            return 1
        if "ORBIT-742" not in with_token:
            print("token: correct token did not return the secret")
            return 1
        print("token: complete")
        return 0
    finally:
        proc.terminate()
        proc.wait(timeout=5)

def check_localhost():
    text = SERVICE.read_text()
    if '--host", default="127.0.0.1"' not in text:
        print("localhost: service default host is not 127.0.0.1")
        return 1
    print("localhost: complete")
    return 0

def check_permissions():
    mode = stat.S_IMODE(SECRET.stat().st_mode)
    if mode != 0o600:
        print(f"permissions: expected 600, got {oct(mode)[2:]}")
        return 1
    print("permissions: complete")
    return 0

def check_logging():
    LOG.unlink(missing_ok=True)
    proc = subprocess.Popen(
        [sys.executable, str(SERVICE), "--host", "127.0.0.1", "--port", "8081"],
        cwd=BASE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1)
        subprocess.run(["curl", "-s", "http://127.0.0.1:8081/secret"], stdout=subprocess.DEVNULL, check=True)
        if not LOG.exists() or "missing_or_bad_token" not in LOG.read_text():
            print("logging: rejected request was not written to access.log")
            return 1
        print("logging: complete")
        return 0
    finally:
        proc.terminate()
        proc.wait(timeout=5)

def main():
    checks = {
        "token": check_token,
        "localhost": check_localhost,
        "permissions": check_permissions,
        "logging": check_logging,
    }
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target == "all":
        return max(func() for func in checks.values())
    if target not in checks:
        print("usage: service-check.py [token|localhost|permissions|logging|all]")
        return 1
    return checks[target]()

if __name__ == "__main__":
    raise SystemExit(main())