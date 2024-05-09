
import requests
import json
import base64

repo_owner = ""
repo_name = ""
branch_name = "main"  # branch you want to push into
file_paths = ['BZU.json', 'date.json']

token = ""  # GitHub API token with repo access

headers = {
    'Authorization': 'token ' + token,
    'Content-Type': 'application/json'
}

# directory_path within the repository
directory_path = "BZU" # use the folder you want to update the files in

for file_path in file_paths:
    with open(file_path, 'rb') as file_content:
        content = base64.b64encode(file_content.read()).decode("utf-8")

    # check if the file exists
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}/{file_path}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # file exists then get the SHA hash
        existing_file_data = response.json()
        sha = existing_file_data['sha']

        # update the file content
        data = {
            "message": f"Update {file_path}",
            "content": content,
            "branch": branch_name,
            "sha": sha
        }

        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}/{file_path}"
        response = requests.put(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print(f"File {file_path} updated on GitHub successfully.")
        else:
            print(
                f"Failed to update {file_path} on GitHub. Status code: {response.status_code}, Response: {response.text}")
    else:
        #  create a new file if the file doesnt exist before
        data = {
            "message": f"Add {file_path}",
            "content": content,
            "branch": branch_name
        }

        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}/{file_path}"
        response = requests.put(url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            print(f"File {file_path} pushed to GitHub successfully.")
        else:
            print(
                f"Failed to push {file_path} to GitHub. Status code: {response.status_code}, Response: {response.text}")
