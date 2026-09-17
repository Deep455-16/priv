import os
import random
import subprocess
from datetime import datetime, timedelta

def get_positive_int(prompt, default=20):
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_repo_path(prompt, default="."):
    while True:
        user_input = input(f"{prompt} (default current directory): ")
        if not user_input.strip():
            user_input = default
        if os.path.isdir(user_input):
            git_dir = os.path.join(user_input, ".git")
            if not os.path.exists(git_dir):
                print(f"\nInitializing new git repository in {user_input}...")
                subprocess.run(["git", "init"], cwd=user_input)
            return user_input
        else:
            print("Directory does not exist. Please enter a valid path.")

def get_remote_url(prompt):
    user_input = input(f"{prompt} (leave blank to skip): ")
    return user_input.strip()

def get_filename(prompt, default="data.txt"):
    user_input = input(f"{prompt} (default {default}): ")
    if not user_input.strip():
        return default
    return user_input

def random_date_in_last_year():
    today = datetime.now()
    start_date = today - timedelta(days=365)
    random_days = random.randint(0, 364)
    random_seconds = random.randint(0, 23 * 3600 + 3599)
    commit_date = start_date + timedelta(days=random_days, seconds=random_seconds)
    return commit_date

def make_commit(date, repo_path, filename, message="graph-greener!"):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")
    
    subprocess.run(["git", "add", filename], cwd=repo_path)
    
    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def main():
    print("=" * 60)
    print("Welcome to graph-greener - GitHub Contribution Graph Commit Generator")
    print("=" * 60)
    print("This tool will help you fill your GitHub contribution graph with custom commits.\n")

    num_commits = get_positive_int("How many commits do you want to make", 20)
    repo_path = get_repo_path("Enter the path to your local git repository", ".")
    remote_url = get_remote_url("Enter the GitHub repository URL to push to")
    filename = get_filename("Enter the filename to modify for commits", "data.txt")

    print(f"\nMaking {num_commits} commits in repo: {repo_path}\nModifying file: {filename}\n")

    for i in range(num_commits):
        commit_date = random_date_in_last_year()
        print(f"[{i+1}/{num_commits}] Committing at {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
        make_commit(commit_date, repo_path, filename)

    print("\nPushing commits to your remote repository...")
    if remote_url:
        res = subprocess.run(["git", "remote"], cwd=repo_path, capture_output=True, text=True)
        if "origin" in res.stdout:
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=repo_path)
        else:
            subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=repo_path)
        
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path)
    else:
        subprocess.run(["git", "push"], cwd=repo_path)
        
    print("✅ All done! Check your GitHub contribution graph in a few minutes.\n")
    print("Tip: Use a dedicated repository for best results. Happy coding!")

if __name__ == "__main__":
    main()
