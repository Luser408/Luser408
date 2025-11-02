import requests
from datetime import datetime

USERNAME = "Luser408"
URL = f"https://api.github.com/users/{USERNAME}"

response = requests.get(URL)
data = response.json()

followers = data.get("followers", "N/A")
public_repos = data.get("public_repos", "N/A")
date_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

readme_path = "README.md"

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!--STATS_START-->"
end_marker = "<!--STATS_END-->"

new_stats = (
    f"{start_marker}\n"
    f"🗓️ Updated on: **{date_str}**\n\n"
    f"👥 Followers: **{followers}**\n"
    f"📦 Public Repos: **{public_repos}**\n"
    f"{end_marker}"
)

if start_marker in content and end_marker in content:
    updated_content = content.split(start_marker)[0] + new_stats + content.split(end_marker)[1]
else:
    updated_content = content + "\n\n" + new_stats

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("✅ README updated successfully!")
