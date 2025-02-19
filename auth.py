import os
import input_data

def github_credentials():
    # Fetch GitHub token and URL from environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    github_url = os.getenv("GITHUB_URL")

    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set.")
    
    if not github_url:
        raise ValueError("GITHUB_URL environment variable is not set.")

    # Extract repository name from GitHub URL
    repo_name = github_url.replace('.git', '').split('/')[-1]
    repo_path = os.path.join("/app", repo_name)

    return github_token, github_url, repo_path

def update_input_data_filepaths(repo_path):
    # Update file paths in input_data with the full path
    for input_item in input_data.list_of_inputs:
        input_item['filepath'] = os.path.join(repo_path, input_item['filepath'])