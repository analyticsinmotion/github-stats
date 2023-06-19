import os
import requests
import csv
from datetime import datetime
from github import Github

# GitHub organization name
organization = "analyticsinmotion"

# Personal access token with repo and read:org scopes
token = os.environ.get('TOKEN')

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
    #print(latest_views)
    
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

print(data)

# Open the CSV file in append mode
#with open(".github/assets/data/views.csv", "a", newline="") as csv_file:
with open("data/views.csv", "a", newline="") as csv_file:
    writer = csv.writer(csv_file)

    # Write each list item as a separate row in the CSV file
    for item in data:
        values = item.split(",")
        writer.writerow(values)

print("Data appended to the CSV file successfully.")






# Access the GitHub repository using the access token
g = Github(os.getenv('TOKEN'))
repo = g.get_repo('analyticsinmotion/github-stats')  

# Specify the file path within the repository
file_path = 'data/views.csv'

# Read the existing content of the file
file_contents = repo.get_contents(file_path)
existing_data = file_contents.decoded_content.decode().splitlines()

# Append new data to the existing content
# new_data = [['new', 'row', 'of', 'data'], ['another', 'row', 'of', 'data']]
new_data = data
updated_data = existing_data + [','.join(row) for row in new_data]

# Encode the updated content
updated_file_contents = '\n'.join(updated_data).encode()

# Commit the changes to the file in the repository
repo.update_file(file_path, "Appending data to CSV", updated_file_contents, file_contents.sha)
