import argparse
import time
from git_clone_push import clone_repo, commit_changes, push_changes
from change_yml import main as modify_yaml
from auth import github_credentials, update_input_data_filepaths

def run_all(scale_type, retries=5):
    attempt = 0
    while attempt < retries:
        try:
            # Get GitHub credentials and repo details from auth module
            github_token, github_url, repo_path = github_credentials()

            # Re-clone the repository
            print(f"Cloning the repository... Attempt {attempt + 1}/{retries}", flush=True)
            clone_repo(github_token)

            # Update file paths in input_data
            update_input_data_filepaths(repo_path)

            # Running the change_yml file with the scale type from our end
            print(f"Modifying YAML files with scale type: {scale_type}", flush=True)
            modify_yaml(scale_type)

            print("Committing and pushing changes...", flush=True)
            # Commit and push changes
            commit_changes(repo_path, scale_type)
            time.sleep(10)

            # Push changes
            push_changes(repo_path, github_token, github_url)

            # Exit outer loop if everything succeeded
            break

        except Exception as outer_e:
            print(f"Outer error detected: {outer_e}. Retrying outer block...", flush=True)
            attempt += 1
            if attempt < retries:
                print(f"Retrying outer loop... Outer attempt {attempt}/{retries}", flush=True)
                time.sleep(5)  # Optional delay before retrying outer
            else:
                print("Max outer retries reached. Exiting.", flush=True)
                raise RuntimeError("Failed to push changes after maximum outer retry attempts.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all scripts sequentially with a specified scale type.")
    parser.add_argument("--scale-type", choices=["scale_up", "scale_down"], required=True,
                        help="Specify whether to scale up or scale down replicas.")
    args = parser.parse_args()

    run_all(args.scale_type)
