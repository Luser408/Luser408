name: Daily Commit

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  daily-commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Git
        run: |
          git config --global user.name "GitHub Action Bot"
          git config --global user.email "action@github.com"
      
      - name: Update timestamp
        run: echo "Bot update: $(date)" > timestamp.txt
      
      - name: Update README Stats
        run: |
          # Get current date
          current_date=$(date +"%Y-%m-%d %H:%M UTC")
          
          # Get GitHub stats
          stats=$(curl -s "https://api.github.com/users/Luser408")
          followers=$(echo "$stats" | grep -o '"followers":[0-9]*' | cut -d: -f2)
          public_repos=$(echo "$stats" | grep -o '"public_repos":[0-9]*' | cut -d: -f2)
          
          echo "Date: $current_date"
          echo "Followers: $followers"
          echo "Public Repos: $public_repos"
          
          # Create new stats block
          new_stats="<!--STATS_START-->
🕒 Last Updated: **$current_date**

👥 Followers: **$followers**

📦 Public Repos: **$public_repos**

✨ Recently Starred Repositories:
⭐ [Luser408/Luser408](https://github.com/Luser408/Luser408)
⭐ [shahradelahi/zod-request](https://github.com/shahradelahi/zod-request)
⭐ [shahradelahi/sha256](https://github.com/shahradelahi/sha256)
<!--STATS_END-->"
          
          # Replace entire stats block
          awk -v new_stats="$new_stats" '
            BEGIN {replacing=0}
            /<!--STATS_START-->/ {
              print new_stats
              replacing=1
              next
            }
            /<!--STATS_END-->/ {
              replacing=0
              next
            }
            replacing==0 {print}
          ' README.md > README_temp.md && mv README_temp.md README.md
      
      - name: Commit changes
        run: |
          git add timestamp.txt README.md
          git commit -m "📊 Daily stats update [$(date +'%Y-%m-%d')]" || echo "No changes"
          git push
