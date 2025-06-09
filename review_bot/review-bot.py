import os
from github import Github

# Inputs
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER"))

g = Github(token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)

print(f"Reviewing PR #{pr_number} in {repo_name}")

for file in pr.get_files():
    if not file.filename.endswith(".cs"):
        continue

    patch = file.patch or ""
    for i, line in enumerate(patch.splitlines()):
        if "+Console.WriteLine" in line or "+// TODO" in line:
            pr.create_review_comment(
                body="⚠️ Avoid `Console.WriteLine` or TODOs in production code.",
                commit_id=pr.head.sha,
                path=file.filename,
                position=i + 1
            )
