# This python script accesses the GitHub API to extract the 
# number of stars, watchers and forks for all public repos.
# Any public repo can be excluded by adding its name to the
# exclude_repos list in the script. Once the data has been 
# extracted it will append to the activity.csv file that is
# located in the data directory of the main branch. This file
# is scheduled to run once a day at midnight using cron. The
# scheduling code is located in .github/workflows/activity.yml

import os
import requests
import csv
from datetime import datetime, timedelta
from github import Github


def fetch_activity_stats(organization, token):
    base_url = 'https://api.github.com/orgs'
    headers = {'Authorization': f'token {token}'}

    url = f'{base_url}/{organization}/repos'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        output = response.json()

        data = []
        exclude_repos = ["discussions", ".github"]

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        for repo_data in output:
            repo_name = repo_data['name']
            repo_stars = repo_data['stargazers_count']
            repo_forks = repo_data['forks_count']
            repo_private = repo_data["private"]

            if repo_name in exclude_repos or repo_private:
                continue

            org_url = repo_data['url']
            org_response = requests.get(org_url, headers=headers)
            org_data = org_response.json()
            repo_watchers = org_data['subscribers_count']

            result = f"{yesterday},{repo_name},{repo_stars},{repo_watchers},{repo_forks}"
            data.append(result)

        return data

    else:
        print(f"Error: Unable to get data for {organization}. Status code: {response.status_code}")


def update_csv_file(repo, file_path, data):
    file_contents = repo.get_contents(file_path)
    existing_data = file_contents.decoded_content.decode().splitlines()
    updated_data = existing_data + data

    updated_file_contents = '\n'.join(updated_data).encode()

    repo.update_file(file_path, "Appending Activity Data to CSV", updated_file_contents, file_contents.sha)

def main():
    organization = "analyticsinmotion"
    token = os.environ.get('TOKEN')

    data = fetch_activity_stats(organization, token)
    print(data)
    
    g = Github(os.getenv('TOKEN'))
    repo = g.get_repo('analyticsinmotion/github-stats')
    file_path = 'data/activity.csv'

    try:
        update_csv_file(repo, file_path, data)
        print("Data appended to CSV file successfully.")
    except Exception as e:
        print(f"Failed to update CSV file: {str(e)}")

if __name__ == "__main__":
    main()
