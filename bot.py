import requests
import datetime
import os

USERNAME = "Luser408"
README_FILE = "README.md"

# Fetch GitHub user stats
def get_github_stats():
    url = f"https://api.github.com/users/{USERNAME}"
    response = requests.get(url).json()
    followers = response.get("followers", 0)
    public_repos = response.get("public_repos", 0)
    return followers, public_repos

# Fetch last 3 recently starred repos
def get_recent_stars(limit=3):
    url = f"https://api.github.com/users/{USERNAME}/starred?per_page={limit}"
    response = requests.get(url).json()
    if isinstance(response, list) and len(response) > 0:
        stars = []
        for repo in response[:limit]:
            name = repo.get("full_name", "Unknown")
            html_url = repo.get("html_url", "#")
            stars.append(f"⭐ [{name}]({html_url})")
        return "\n".join(stars)
    return "No recent stars"

# Update README content
def update_readme():
    followers, public_repos = get_github_stats()
    recent_stars = get_recent_stars()
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!--STATS_START-->"
    end_tag = "<!--STATS_END-->"
    new_section = (
        f"{start_tag}\n"
        f"🕒 Last Updated: **{date}**\n\n"
        f"👥 Followers: **{followers}**\n\n"
        f"📦 Public Repos: **{public_repos}**\n\n"
        f"✨ Recently Starred Repositories:\n{recent_stars}\n"
        f"{end_tag}"
    )

    if start_tag in content and end_tag in content:
        start_idx = content.index(start_tag)
        end_idx = content.index(end_tag) + len(end_tag)
        updated_content = content[:start_idx] + new_section + content[end_idx:]
    else:
        updated_content = content + "\n\n" + new_section

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()
