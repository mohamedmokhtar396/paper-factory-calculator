import os
import subprocess
import re

def run_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Error executing command:")
        print(e.stderr)
        return None

def get_pages_link(remote_url):
    # Extract username and repository name to generate the link
    match = re.search(r'github\.com[:/](.+)/(.+?)(?:\.git)?$', remote_url)
    if match:
        username = match.group(1)
        repo = match.group(2)
        return f"https://{username}.github.io/{repo}/"
    return None

def main():
    print("="*50)
    print("      Website Deployment & Update Tool      ")
    print("="*50)
    
    is_initialized = os.path.exists(".git")
    
    if not is_initialized:
        print("\n[INFO] New project detected. Initializing repository...")
        run_command(["git", "init"])
        run_command(["git", "branch", "-M", "main"])
        repo_url = input("Enter repository URL (e.g., https://github.com/user/repo.git): ")
        run_command(["git", "remote", "add", "origin", repo_url])
    else:
        print("\n[INFO] Existing repository found. Preparing to upload updates...")

    print("\n[PROCESS] Adding files...")
    run_command(["git", "add", "."])

    commit_msg = input("\nEnter commit message (or press Enter for 'Site Update'): ")
    if not commit_msg:
        commit_msg = "Site Update"
    
    print("\n[PROCESS] Committing changes...")
    run_command(["git", "commit", "-m", commit_msg])

    print("\n[PROCESS] Pushing to GitHub...")
    push_result = run_command(["git", "push", "-u", "origin", "main"])
    
    if push_result is not None:
        print("\n[SUCCESS] Files successfully pushed!")
        
        remote_url = run_command(["git", "remote", "get-url", "origin"])
        if remote_url:
            pages_link = get_pages_link(remote_url)
            if pages_link:
                print("\nYour website link is:")
                print(pages_link)
                print("(Note: The link may take a few minutes to work the first time)")
            else:
                print("\n[WARNING] Could not extract automatic link.")
    else:
        print("\n[ERROR] Push failed. Please check your access permissions.")

if __name__ == "__main__":
    main()