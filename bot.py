import requests
import datetime

USERNAME = "Luser408"
README_FILE = "README.md"

def fetch_github_data(username):
    user_data = requests.get(f"https://api.github.com/users/{username}").json()
    repos_data = requests.get(f"https://api.github.com/users/{username}/repos?sort=updated").json()

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    latest_repo = repos_data[0]["name"] if repos_data else "N/A"
    latest_commit_msg = "N/A"

    if repos_data:
        repo_name = repos_data[0]["name"]
        commits = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/commits").json()
        if isinstance(commits, list) and commits:
            latest_commit_msg = commits[0]["commit"]["message"]

    return {
        "followers": user_data.get("followers", 0),
        "public_repos": user_data.get("public_repos", 0),
        "total_stars": total_stars,
        "latest_repo": latest_repo,
        "latest_commit_msg": latest_commit_msg,
    }

def update_readme(stats):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!--STATS_START-->"
    end_marker = "<!--STATS_END-->"

    stats_md = f"""
📊 **Live GitHub Stats (Auto Updated Daily)**

🗓️ Last Updated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
⭐ Total Stars: {stats['total_stars']}
👥 Followers: {stats['followers']}
🍴 Public Repos: {stats['public_repos']}
📁 Latest Repo: {stats['latest_repo']}
💬 Last Commit: "{stats['latest_commit_msg']}"
"""

    new_content = (
        content.split(start_marker)[0]
        + start_marker
        + "\n"
        + stats_md
        + "\n"
        + end_marker
        + content.split(end_marker)[1]
    )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    stats = fetch_github_data(USERNAME)
    update_readme(stats)
