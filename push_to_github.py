"""
push_to_github.py — Pushes all project files to GitHub via REST API.
Usage: python push_to_github.py <YOUR_GITHUB_TOKEN>
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error
import time

GITHUB_USERNAME = "ajaynarwal1495-droid"
REPO_NAME       = "IBMprojectsmratAI"
BRANCH          = "main"
COMMIT_MESSAGE  = "feat: SmartStudy AI - complete project foundation"
PROJECT_ROOT    = os.path.dirname(os.path.abspath(__file__))

# Files/folders to skip
SKIP_DIRS  = {".venv", "node_modules", "__pycache__", ".git", "dist", ".pytest_cache", "uploads"}
SKIP_FILES = {".env", "push_to_github.py", "smartstudy.db", "uvicorn.log", "vite.log"}
SKIP_EXTS  = {".pyc", ".pyo", ".db", ".sqlite", ".log"}


def api_request(url, token, method="GET", data=None):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "SmartStudy-Pusher"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req  = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")), resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return json.loads(body) if body else {}, e.code


def collect_files():
    files = []
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        # Remove skip dirs in-place so os.walk doesn't descend into them
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in filenames:
            if filename in SKIP_FILES:
                continue
            if os.path.splitext(filename)[1] in SKIP_EXTS:
                continue
            full_path = os.path.join(root, filename)
            rel_path  = os.path.relpath(full_path, PROJECT_ROOT).replace("\\", "/")
            files.append((rel_path, full_path))
    return files


def get_file_sha(path, token):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{path}"
    resp, status = api_request(url, token)
    if status == 200:
        return resp.get("sha")
    return None


def push_file(rel_path, full_path, token, index, total):
    try:
        with open(full_path, "rb") as f:
            raw = f.read()
    except Exception as e:
        print(f"  [SKIP] Cannot read {rel_path}: {e}")
        return False

    content_b64 = base64.b64encode(raw).decode("utf-8")
    url         = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{rel_path}"
    existing_sha = get_file_sha(rel_path, token)

    payload = {
        "message": COMMIT_MESSAGE,
        "content": content_b64,
        "branch":  BRANCH,
    }
    if existing_sha:
        payload["sha"] = existing_sha

    resp, status = api_request(url, token, method="PUT", data=payload)

    if status in (200, 201):
        print(f"  [{index}/{total}] ✓  {rel_path}")
        return True
    else:
        print(f"  [{index}/{total}] ✗  {rel_path} — HTTP {status}: {resp.get('message','')}")
        return False


def main():
    if len(sys.argv) < 2:
        print("\nUsage: python push_to_github.py <YOUR_GITHUB_TOKEN>")
        print("Get token at: https://github.com/settings/tokens/new  (scope: repo)\n")
        sys.exit(1)

    token = sys.argv[1].strip()

    # Verify token works
    print(f"\n🔍 Verifying token for user: {GITHUB_USERNAME}")
    resp, status = api_request("https://api.github.com/user", token)
    if status != 200:
        print(f"❌ Token invalid or expired. Status: {status}")
        sys.exit(1)
    print(f"✅ Authenticated as: {resp.get('login')}")

    # Verify repo exists
    print(f"\n🔍 Checking repository: {REPO_NAME}")
    resp, status = api_request(
        f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}", token
    )
    if status != 200:
        print(f"❌ Repo not found. Create it at https://github.com/new first.")
        sys.exit(1)
    print(f"✅ Repository found: {resp.get('full_name')}")

    # Collect files
    files = collect_files()
    total = len(files)
    print(f"\n📁 Found {total} files to push\n")

    # Push each file
    success = 0
    failed  = 0
    for i, (rel_path, full_path) in enumerate(files, 1):
        ok = push_file(rel_path, full_path, token, i, total)
        if ok:
            success += 1
        else:
            failed += 1
        # Small delay to avoid GitHub secondary rate limits
        time.sleep(0.3)

    print(f"\n{'='*50}")
    print(f"✅ Pushed:  {success} files")
    print(f"❌ Failed:  {failed} files")
    print(f"\n🔗 Repository: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
