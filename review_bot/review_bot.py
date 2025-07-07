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
    if not file.patch:
        continue

    prompt = f"""You are a senior developer reviewing code,review the code based on the defined Security Design principles :
    1.Least priveledge 2.Fail-Safe 3. Privacy by default 4. Removing legacy and unsused components 5.Buffer Overflows 6.Injection Flaws
    7.Cross-Site Scripting 8.DOS Attack 9.Broken Authentication
    
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
    label_name = "Reviewbot-Changes-required"

    # Add label to PR
    existing_labels = [label.name for label in pr.get_labels()]
    if label_name not in existing_labels:
        repo_label = None
        try:
            repo_label = repo.get_label(label_name)
        except:
            repo_label = repo.create_label(name=label_name, color="f29513", description="Review bot: review changes needed")
        
        pr.add_to_labels(repo_label)

    print("Comments posted.")
else:
    print("No comments to post.")

