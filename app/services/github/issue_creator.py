# app/services/github/issue_creator.py

import requests

def create_issue(repo, task):
    url = f"https://api.github.com/repos/{repo}/issues"
    
    payload = {
        "title": task["task"],
        "body": task["description"],
    }
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    
    requests.post(url, json=payload, headers=headers)