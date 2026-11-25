import os
import urllib.request
import json

repo_id = "bop-benchmark/ycbv"
local_dir = "./ycbv"
os.makedirs(local_dir, exist_ok=True)

print(f"Fetching file list for {repo_id}...")
api_url = f"https://huggingface.co/api/datasets/{repo_id}/tree/main"

# Fetch file tree recursively or list root files using HF Hub API
req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print(f"Failed to fetch file list: {e}")
    exit(1)

# Function to download files recursively from the tree API
def download_tree(path=""):
    url = f"https://huggingface.co/api/datasets/{repo_id}/tree/main/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            items = json.loads(response.read().decode())
    except Exception:
        items = []

    for item in items:
        item_path = f"{path}/{item['path']}" if path else item['path']
        if item['type'] == 'directory':
            os.makedirs(os.path.join(local_dir, item_path), exist_ok=True)
            download_tree(item_path)
        elif item['type'] == 'file':
            file_url = f"https://huggingface.co/datasets/{repo_id}/raw/main/{item_path}"
            # For large binary files
            file_url_resolve = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{item_path}"
            dest_path = os.path.join(local_dir, item_path)
            
            if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
                print(f"Skipping (already exists): {item_path}")
                continue

            print(f"Downloading: {item_path}...")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            try:
                urllib.request.urlretrieve(file_url_resolve, dest_path)
            except Exception as err:
                print(f"Error downloading {item_path}: {err}")

download_tree()
print("Download script finished!")