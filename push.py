import requests
import json
import base64


repo_owner = ""
repo_name = ""
branch_name = "main"  # Or whatever branch you want to push to
file_paths = ['BZU.json', 'date.json']

token = ""# GitHub API token with repo access







headers = {
    'Authorization': 'token ' + token,
    'Content-Type': 'application/json'
}


for file_path in file_paths:
    with open(file_path, 'rb') as file_content:
        content = base64.b64encode(file_content.read()).decode("utf-8")
    data = {
        "message": f"Add {file_path}",
        "content": content,
        "branch": branch_name
    }
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print(f"File {file_path} pushed to GitHub successfully.")
    else:
        print(f"Failed to push {file_path} to GitHub. Status code: {response.status_code}, Response: {response.text}")
