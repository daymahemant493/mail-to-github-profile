# 🕵️ GitHub Email OSINT Tool

This project demonstrates an **OSINT-based technique** to check whether an email address is linked to a GitHub account by leveraging commit metadata.

It automates:
- Temporary repository creation
- Commit injection using a target email
- Commit author extraction
- Profile enrichment (repos, activity, metadata)
- Cleanup (repo deletion)

---

## ⚠️ Ethical Use Disclaimer

This tool is strictly for:
- Educational purposes  
- OSINT research  
- Authorized investigations  

Do **NOT** use this tool for:
- Harassment  
- Privacy invasion  
- Unauthorized tracking  

Always ensure proper authorization before testing.

---

## 🚀 How It Works

1. Creates a **temporary private repository**
2. Commits a file using a **custom email address**
3. Fetches commit metadata from GitHub API
4. Checks if the email is linked to a GitHub account
5. If linked → extracts:
   - Username
   - Profile details
   - Repositories
   - Recent activity
6. Deletes the repository (cleanup)

---

## 📦 Requirements

- Python 3.x
- `requests` library

Install dependencies:



🔑 Generate GitHub Token (Classic)

You need a Personal Access Token (Classic) with repo permissions.

Step-by-step:
Go to GitHub → Settings

Navigate to:

Developer Settings → Personal Access Tokens → Tokens (Classic)

Click:

Generate new token (classic)
Configure:
Note: OSINT Tool Token
Expiration: 7 or 30 days (recommended)
Scopes:
✅ repo (Full control of private repositories)
Click Generate token
⚠️ Copy the token immediately (you won’t be able to see it again)
⚙️ Configuration

Edit the script and add your credentials:

GITHUB_TOKEN = "your_token_here"
GITHUB_USERNAME = "your_username"
REPO_NAME = "temp-repo-name"
▶️ Usage

Run the script:

python script.py

You will be prompted:

Enter email:
Example:
Enter email: target@example.com

```bash
pip install requests
