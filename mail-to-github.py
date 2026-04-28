import requests
import json
import time
import base64

# ================= CONFIG (HARDCODED) =================
GITHUB_TOKEN = ""
GITHUB_USERNAME = ""
REPO_NAME = "temp-repo-name"

# ================= HELPERS =================
def handle_rate_limit(response):
    if response.status_code == 403:
        print("[!] Rate limited. Sleeping for 60 seconds...")
        time.sleep(60)
        return True
    return False


# ================= STEP 1: CREATE REPO =================
def create_github_repo(repo_name, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "name": repo_name,
        "private": True,
        "auto_init": True
    }

    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json=data
    )

    if response.status_code == 201:
        print("[+] Repo created")
    elif response.status_code == 422:
        print("[!] Repo already exists")
    else:
        print("[-] Repo creation failed:", response.text)


# ================= STEP 2: COMMIT WITH EMAIL =================
def commit_to_github(repo_name, email, token, username):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    content = base64.b64encode(b"OSINT TEST").decode()

    data = {
        "message": "OSINT email test commit",
        "committer": {
            "name": "osint-probe",
            "email": email
        },
        "content": content
    }

    response = requests.put(
        f"https://api.github.com/repos/{username}/{repo_name}/contents/test.txt",
        headers=headers,
        json=data
    )

    if response.status_code == 201:
        print("[+] Commit created")
    else:
        print("[-] Commit failed:", response.text)


# ================= STEP 3: EXTRACT AUTHOR =================
def get_commit_author(repo_name, token, username):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(
        f"https://api.github.com/repos/{username}/{repo_name}/commits",
        headers=headers
    )

    if handle_rate_limit(response):
        return get_commit_author(repo_name, token, username)

    if response.status_code != 200:
        print("[-] Failed to fetch commits:", response.text)
        return None

    commits = response.json()

    if not commits:
        print("[!] No commits found")
        return None

    commit = commits[0]
    author = commit.get("author")
    raw_author = commit.get("commit", {}).get("author")

    if not author:
        print("[!] Email not linked to GitHub account")
        print("[i] Raw commit author:")
        print(json.dumps(raw_author, indent=4))
        return None

    print("\n[+] FULL AUTHOR OBJECT:\n")
    print(json.dumps(author, indent=4))

    return author.get("login")


# ================= STEP 4: PROFILE ENRICHMENT =================
def get_full_github_profile(username, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    # USER PROFILE
    user_res = requests.get(
        f"https://api.github.com/users/{username}",
        headers=headers
    )

    if handle_rate_limit(user_res):
        return get_full_github_profile(username, token)

    if user_res.status_code != 200:
        print("[-] Failed to fetch user profile")
        return None

    user_data = user_res.json()

    # REPOS
    repo_res = requests.get(
        f"https://api.github.com/users/{username}/repos",
        headers=headers
    )

    repos = []
    if repo_res.status_code == 200:
        for repo in repo_res.json():
            repos.append({
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"],
                "updated_at": repo["updated_at"]
            })

    # EVENTS
    events_res = requests.get(
        f"https://api.github.com/users/{username}/events",
        headers=headers
    )

    events = []
    if events_res.status_code == 200:
        for event in events_res.json()[:10]:
            events.append({
                "type": event["type"],
                "repo": event["repo"]["name"],
                "created_at": event["created_at"]
            })

    profile = {
        "username": user_data["login"],
        "name": user_data.get("name"),
        "bio": user_data.get("bio"),
        "company": user_data.get("company"),
        "location": user_data.get("location"),
        "blog": user_data.get("blog"),
        "public_repos": user_data.get("public_repos"),
        "followers": user_data.get("followers"),
        "following": user_data.get("following"),
        "created_at": user_data.get("created_at"),
        "repos": repos,
        "recent_activity": events
    }

    return profile


# ================= STEP 5: CLEANUP =================
def delete_github_repo(repo_name, token, username):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.delete(
        f"https://api.github.com/repos/{username}/{repo_name}",
        headers=headers
    )

    if response.status_code == 204:
        print("[+] Repo deleted")
    else:
        print("[-] Repo deletion failed:", response.text)


# ================= MAIN =================
if __name__ == "__main__":
    email = input("Enter email: ").strip()

    create_github_repo(REPO_NAME, GITHUB_TOKEN)
    commit_to_github(REPO_NAME, email, GITHUB_TOKEN, GITHUB_USERNAME)

    username = get_commit_author(REPO_NAME, GITHUB_TOKEN, GITHUB_USERNAME)

    if username:
        print("\n[+] Fetching full profile...\n")
        profile = get_full_github_profile(username, GITHUB_TOKEN)
        print(json.dumps(profile, indent=4))

    delete_github_repo(REPO_NAME, GITHUB_TOKEN, GITHUB_USERNAME)
