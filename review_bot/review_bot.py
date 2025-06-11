import os
from github import Github
from mistralai import Mistral

# Inputs
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER"))

#Connect to github
g = Github(token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)

comments = []
print(f"Reviewing PR #{pr_number} in {repo_name}")

for file in pr.get_files():
    if not file.filename.endswith(".cs") or not file.patch:
        continue

    prompt = f"""You are a senior .NET developer reviewing code. 
    Provide a code review for the following diff (GitHub pull request format). Be constructive and concise.\n\n
    ```diff\n{file.patch}\n```"""

    try:
        mistralClient = Mistral(api_key="oJiXyrl6BwYbWLzMyqcECc46wjlsWWP8")
        response = mistralClient.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": "You are a helpful code reviewer."},
                {"role": "user", "content": prompt}
            ]
        )
        suggestion = response.choices[0].message.content
        comments.append(f"### Review for `{file.filename}`\n{suggestion}")
    except Exception as e:
        comments.append(f"Error analyzing {file.filename}: {str(e)}")

# Post summary as PR comment
if comments:
    pr.create_issue_comment("\n\n---\n".join(comments))
    print("Comments posted.")
else:
    print("No comments to post.")
