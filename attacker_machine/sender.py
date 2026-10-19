import requests,time,random,os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INBOX_PATH = os.path.join(SCRIPT_DIR, "inbox_a.txt")
TOKEN = os.environ["GITHUB_TOKEN"]
GIST_ID = "7ab519d3252a1e4f1ed713fff9f3987f"
FILENAME = "channel.txt"
MESSAGE_TO_SEND = "run"

def load_key(file_path="conv.key"):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
SECRET_KEY = load_key()  


cipher = Fernet(SECRET_KEY.encode())

def get_headers():
    return {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

def read_channel():
    url = f"https://api.github.com/gists/{GIST_ID}"
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        if r.status_code == 200:
            return r.json()["files"][FILENAME]["content"].strip()
        return None
    except requests.RequestException:
        return None

def write_channel(text):
    url = f"https://api.github.com/gists/{GIST_ID}"
    data = {"files": {FILENAME: {"content": text}}}
    try:
        r = requests.patch(url, headers=get_headers(), json=data, timeout=15)
        return r.status_code == 200
    except requests.RequestException:
        return False

def main():
    initial_delay = random.randint(5, 20)
    print(f"[A] Script started. Waiting {initial_delay}s before initializing...")
    time.sleep(initial_delay)

    print(f"[A] Encrypting and sending: {MESSAGE_TO_SEND}")
    
    encrypted_bytes = cipher.encrypt(MESSAGE_TO_SEND.encode())
    encrypted_str = encrypted_bytes.decode('utf-8')
    
    time.sleep(random.uniform(0.5, 3.5))
    
    if not write_channel(f"B:{encrypted_str}"):
        print("[A] Failed to send message.")
        return
        
    print("[A] Sent. Listening for encrypted reply...")

    while True:
        content = read_channel()
        if content and content.startswith("A:"):
            encrypted_reply = content[2:].strip()
            try:
                decrypted_bytes = cipher.decrypt(encrypted_reply.encode())
                message = decrypted_bytes.decode('utf-8')
                print(f"\n[A] 🔓 Decrypted reply: {message}")
                
                with open(INBOX_PATH, "w") as f:
                    f.write(message + "\n")
                print("[A] Saved to inbox_a.txt.")
                
                time.sleep(random.uniform(1.0, 5.0))
                
                print("[A] Sending final __EMPTY__ message to reset channel...")
                if write_channel("__EMPTY__"):
                    print("[A] Channel successfully reset to Point 1.")
                else:
                    print("[A] Failed to reset channel.")
                break
                
            except Exception as e:
                print(f"[A] Decryption failed: {e}")
                break
        
        base_delay = 60
        jitter = random.randint(-30, 45)
        delay = base_delay + jitter
        print(f"[A] No reply yet. Sleeping for {delay} seconds...")
        time.sleep(delay)

if __name__ == "__main__":
    main()