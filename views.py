import os
import requests
import csv
from datetime import datetime

# GitHub organization name
organization = "analyticsinmotion"

# Personal access token with repo and read:org scopes
#token = $TOKEN
#token = os.environ.get('TOKEN')
token = os.getenv("TOKEN")

# Base URL for GitHub REST API
base_url = "https://api.github.com"

# GitHub API endpoint for organization repositories
repos_url = f"{base_url}/orgs/{organization}/repos"

# Request headers with the access token
headers = {
    "Authorization": f"Token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Fetch organization repositories
response = requests.get(repos_url, headers=headers)

if response.status_code == 200:
    output = response.json()
else:
    print(f"Failed to fetch traffic stats for repository. Error: {response.status_code}")


data = []

# Public Repositories to exclude
exclude_repos = ["discussions", ".github"]

# Iterate over the repositories
for repo in output:
    repo_name = repo["name"]
    repo_url = repo["url"]
    repo_private = repo["private"]
    
    # Exclude specified repositories
    if repo_name in exclude_repos:
        continue

    # Exclude private repositories
    if repo_private:
        continue    
    
    # Get the traffic stats for the repository
    traffic_url = f"{repo_url}/traffic/views"
    response = requests.get(traffic_url, headers=headers)
    traffic_stats = response.json()

    # Extract the relevant traffic information
    views_summary = traffic_stats['views']
    
    # Get the most recent viewing stats for the repo.
    latest_views = views_summary[-1:]
    
    # Should the latest record be blank (i.e. the list is empty []) add the current date stamp with a 0 view 0 unique data set
    if not latest_views:
        current_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        latest_views = [{'timestamp': current_date, 'count': 0, 'uniques': 0}]
    
    datetime_object = datetime.strptime(latest_views[0]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    date_only = datetime_object.date()
    views = latest_views[0]['count']
    unique_visitors = latest_views[0]['uniques']
    result = str(date_only) + "," + repo_name + "," + str(views) + "," + str(unique_visitors)
    
    # Add the result to the list variable data 
    data.append(result)

# Open the CSV file in append mode
with open(".github/assets/data/views.csv", "a", newline="") as csv_file:
    writer = csv.writer(csv_file)

    # Write each list item as a separate row in the CSV file
    for item in data:
        values = item.split(",")
        writer.writerow(values)

print("Data appended to the CSV file successfully.")


