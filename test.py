#!/usr/bin/env python3
# test.py — sample file to test Semgrep behavior

import os
import subprocess
import hashlib
import json

def safe_hash(data: bytes) -> str:
    # This is okay: using SHA-256, not MD5
    h = hashlib.sha256(data).hexdigest()
    return h

def insecure_hash(data: bytes) -> str:
    # Example of insecure usage — MD5
    m = hashlib.md5(data).hexdigest()  # maybe a rule to flag MD5 usage
    return m

def run_user_command(user_input: str):
    # This is insecure: builds a shell command with user input
    os.system("ls " + user_input)  # command injection risk: expected to be flagged by Semgrep

    # Another variant using subprocess — still risky if not sanitized
    subprocess.call(["ls", user_input])

def process_data(obj: dict):
    # Nested complexity: safe path
    if "username" in obj and isinstance(obj["username"], str):
        name = obj["username"].strip()
        print(f"Hello, {name}")
    else:
        print("No valid username provided")

def serialize_secret(secret: str):
    # Hardcoded secret — maybe a rule to catch hardcoded credentials/keys
    cfg = {
        "secret_key": "my_secret_value_12345",
        "user": "admin"
    }
    return json.dumps(cfg)

def main():
    user_input = input("Enter directory name: ")
    run_user_command(user_input)

    data = b"some important data"
    print("SHA256:", safe_hash(data))
    print("MD5:", insecure_hash(data))

    config = {"username": "  alice "}
    process_data(config)

    # Dump a hardcoded secret — maybe insecure depending on rule
    print("Config:", serialize_secret("top_secret"))

if __name__ == "__main__":
    main()
