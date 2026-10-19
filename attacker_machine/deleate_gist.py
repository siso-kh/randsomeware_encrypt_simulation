import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["GITHUB_TOKEN"]
GIST_ID = "7ab519d3252a1e4f1ed713fff9f3987f"

def delete_gist():
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"[*] Attempting to delete Gist: {GIST_ID}")
    response = requests.delete(url, headers=headers, timeout=15)
    
    if response.status_code == 204:
        print("[✅] Gist deleted successfully. All history is gone.")
    elif response.status_code == 404:
        print("[!] Gist not found (it may already be deleted).")
    elif response.status_code == 403:
        print("[❌] Forbidden. Check if your Token has 'gist' permission.")
    else:
        print(f"[❌] Failed. Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    confirm = input("This will PERMANENTLY delete the Gist and ALL history. Type 'YES' to confirm: ")
    if confirm == "YES":
        delete_gist()
    else:
        print("Cancelled.")