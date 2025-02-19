from git import Repo,GitCommandError
import os
import shutil
import stat
import pygit2
import subprocess

def handle_remove_readonly(func, path, exc_info):
    """
    Handle the read-only file removal.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(github_token):
    """
    Clones the repository using the provided GitHub token and URL from the environment variable.
    """
    repo_url = os.getenv("GITHUB_URL")
    if not repo_url:
        raise ValueError("GITHUB_URL environment variable is not set.")

    current_directory = os.path.dirname(os.path.abspath(__file__))
    repo_name = os.path.basename(repo_url).replace('.git', '')
    clone_directory = os.path.join(current_directory, repo_name)

    if os.path.exists(clone_directory):
        print(f"Directory {clone_directory} already exists. Deleting it.")
        shutil.rmtree(clone_directory, onerror=handle_remove_readonly)
        print(f"Deleted {clone_directory}")
    # Use pygit2 credentials for cloning
    credentials = pygit2.UserPass(github_token, "x-oauth-basic")
    pygit2.clone_repository(repo_url, clone_directory, callbacks=pygit2.RemoteCallbacks(credentials=credentials))
    print(f"Repository cloned into {clone_directory}")

def commit_changes(repo_directory, scale_type):
    commit_message = f"watchman: {scale_type}"
    repo = Repo(repo_directory)
    git_committer_name = os.getenv('GIT_COMMITTER_NAME')
    git_committer_email = os.getenv('GIT_COMMITTER_EMAIL')

    if not git_committer_name or not git_committer_email:
        raise ValueError("Git committer name and email must be set via environment variables.")

    with repo.config_writer() as config:
        config.set_value("user", "name", git_committer_name)
        config.set_value("user", "email", git_committer_email)

    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)
        repo.index.commit(commit_message)
        print("Changes committed locally")
    else:
        print("No changes to commit.")

def push_changes(repo_directory, github_token, github_url):
    github_url_cleaned = github_url.replace("https://", "").replace("http://", "")
    os.environ['GIT_ASKPASS'] = 'echo'
    os.environ['GIT_USERNAME'] = 'x-access-token'
    os.environ['GIT_PASSWORD'] = github_token

    repo = Repo(repo_directory)
    origin = repo.remote(name='origin')
    remote_url = f'https://{github_token}@{github_url_cleaned}'
    origin.set_url(remote_url)

    try:
        origin.push().raise_if_error()
        print("Changes successfully pushed to the repository.", flush=True)
    except Exception as e:
        error_message = str(e).lower()
        if "failed to push some refs" in error_message or "merge conflict" in error_message:
            print("Merge conflict or push failure detected. Attempting to pull and rebase.", flush=True)

            # Pull the latest changes with rebase to avoid merge commits
            try:
                print("Pulling latest changes with rebase before pushing...", flush=True)
                pull_info = origin.pull(rebase=True)
                for info in pull_info:
                    if info.flags & info.ERROR:
                        raise GitCommandError(f"Error during pull: {info.summary}")
            except GitCommandError as e:
                print(f"Failed to pull changes with rebase: {e}. Trying without rebase...", flush=True)
                try:
                    repo.git.rebase('--abort')  # Abort the failed rebase
                    pull_info = origin.pull()  # Retry without rebase
                    for info in pull_info:
                        if info.flags & info.ERROR:
                            raise GitCommandError(f"Error during pull without rebase: {info.summary}")
                except GitCommandError as e:
                    print(f"Failed to pull changes without rebase: {e}", flush=True)
                    raise e

            # Retry push after rebase
            print("Retrying push after rebase...", flush=True)
            origin.push().raise_if_error()
            print("Push successful after rebase.", flush=True)
        else:
            print(f"Unhandled exception in push operation: {error_message}", flush=True)
            raise e
