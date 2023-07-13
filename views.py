# This python script accesses the GitHub API to extract the 
# number of views and unique visitors for all public repos.
# Any public repo can be excluded by adding its name to the
# exclude_repos list in the script. Once the data has been 
# extracted it will append to the views.csv file that is
# located in the data directory of the main branch. This file
# is scheduled to run once a day at 12:30am using cron. The
# scheduling code is located in .github/workflows/views.yml

import os
import requests
import csv
from datetime import datetime, timedelta
from github import Github

def fetch_traffic_stats(repo_url, headers):
    traffic_url = f"{repo_url}/traffic/views"
    response = requests.get(traffic_url, headers=headers)
    if response.status_code == 200:
        traffic_stats = response.json()
        return traffic_stats['views']
    else:
        raise Exception(f"Failed to fetch traffic stats for repository. Error: {response.status_code}")

def update_csv_file(repo, file_path, data):
    file_contents = repo.get_contents(file_path)
    existing_data = file_contents.decoded_content.decode().splitlines()
    updated_data = existing_data + data

    updated_file_contents = '\n'.join(updated_data).encode()

    repo.update_file(file_path, "Appending data to CSV", updated_file_contents, file_contents.sha)

def main():
    organization = "analyticsinmotion"
    token = os.environ.get('TOKEN')
    base_url = "https://api.github.com"
    repos_url = f"{base_url}/orgs/{organization}/repos"

    headers = {
        "Authorization": f"Token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(repos_url, headers=headers)
    if response.status_code == 200:
        output = response.json()
    else:
        print(f"Failed to fetch organization repositories. Error: {response.status_code}")
        return

    data = []
    exclude_repos = ["discussions", ".github"]

    for repo in output:
        repo_name = repo["name"]
        repo_url = repo["url"]
        repo_private = repo["private"]

        if repo_name in exclude_repos or repo_private:
            continue

        try:
            traffic_stats = fetch_traffic_stats(repo_url, headers)

            check_dates_list = []
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)

            for views_stats in traffic_stats:
                date_object = datetime.strptime(views_stats['timestamp'], '%Y-%m-%dT%H:%M:%SZ').date()
                check_dates_list.append(date_object)
                if date_object == yesterday:
                    date_only = yesterday
                    views = views_stats['count']
                    unique_visitors = views_stats['uniques']

            if yesterday not in check_dates_list:
                date_only = yesterday
                views = 0
                unique_visitors = 0

            result = f"{date_only},{repo_name},{views},{unique_visitors}"
            data.append(result)
        except Exception as e:
            print(f"Failed to fetch traffic stats for repository '{repo_name}': {str(e)}")

    print(data)
    
    g = Github(os.getenv('TOKEN'))
    repo = g.get_repo('analyticsinmotion/github-stats')
    file_path = 'data/views.csv'

    try:
        update_csv_file(repo, file_path, data)
        print("Data appended to CSV file successfully.")
    except Exception as e:
        print(f"Failed to update CSV file: {str(e)}")

if __name__ == "__main__":
    main()
