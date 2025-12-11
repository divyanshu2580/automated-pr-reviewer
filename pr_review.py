import os
import subprocess
import hashlib
import pickle
import base64
import json

# Hard-coded secret / credentials — often flagged by static-analysis rules
API_KEY = "MY_SUPER_SECRET_API_KEY_123456"
PASSWORD = "Pa$$w0rd!"

def insecure_hash(data: bytes) -> str:
    # insecure / weak hash usage — MD5
    m = hashlib.md5(data).hexdigest()
    return m

def secure_hash(data: bytes) -> str:
    # safer usage — SHA-256
    return hashlib.sha256(data).hexdigest()

def run_shell_untrusted(user_input: str):
    # Unsafe: using shell command with direct concatenation of untrusted input
    os.system("ls " + user_input)

    # Another unsafe variant: subprocess with shell=True (if used)
    subprocess.call("echo " + user_input, shell=True)

def safe_list_dir(path: str):
    # Safe usage: using Python API, not shell
    if os.path.isdir(path):
        for name in os.listdir(path):
            print(name)
    else:
        print("Not a dir:", path)

def do_exec(user_code: str):
    # Dangerous: executing arbitrary code from user input
    exec(user_code)

def insecure_deserialize(pickled_data: bytes):
    # Dangerous: untrusted pickle.loads — insecure deserialization
    obj = pickle.loads(pickled_data)
    return obj

def main():
    print("Hardcoded secrets:", API_KEY, PASSWORD)

    data = b"hello world"
    print("Insecure MD5:", insecure_hash(data))
    print("Secure SHA256:", secure_hash(data))

    user_input = input("Enter something (shell path): ")
    run_shell_untrusted(user_input)
    safe_list_dir(user_input)

    print("Now exec user code...")
    code = input("Enter python code to exec: ")
    do_exec(code)

    print("Demonstrating unsafe deserialization (pretend this came from network):")
    dummy = pickle.dumps({"foo": "bar"})
    result = insecure_deserialize(dummy)
    print("Deserialized result:", result)

    # Also include some benign code to test false-positives
    cfg = {"user": "alice", "role": "admin"}
    print(json.dumps(cfg))

if __name__ == "__main__":
    main()
