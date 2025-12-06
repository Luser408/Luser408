name: Daily Commit

on:
  schedule:
    # Runs every day at 00:00 UTC (midnight)
    - cron: '0 0 * * *'
  workflow_dispatch:  # Allows manual run

jobs:
  daily-commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      # Step 1: Get the code
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      # Step 2: Setup git
      - name: Setup Git
        run: |
          git config --global user.name "GitHub Action Bot"
          git config --global user.email "action@github.com"
      
      # Step 3: Update timestamp only
      - name: Update timestamp
        run: |
          echo "Last updated: $(date)" > timestamp.txt
      
      # Step 4: SIMPLER README update (just update date)
      - name: Update README Date
        run: |
          # Get current date
          current_date=$(date +"%Y-%m-%d %H:%M UTC")
          
          # Simple sed command to update date
          sed -i "s|🕒 Last Updated: \*\*.*\*\*|🕒 Last Updated: **$current_date**|" README.md
      
      # Step 5: Commit and push
      - name: Commit and push
        run: |
          git add timestamp.txt README.md
          git commit -m "🤖 Daily update [$(date +'%Y-%m-%d')]" || echo "No changes to commit"
          git push
