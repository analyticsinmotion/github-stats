# This python script accesses the GitHub API to extract the 
# number of views and unique visitors for all public repos.
# Any public repo can be excluded by adding its name to the
# exclude_repos list in the script. Once the data has been 
# extracted it will append to the traffic.csv file that is
# located in the data directory of the main branch. This file
# is scheduled to run once a day at 12:45am using cron. The
# scheduling code is located in .github/workflows/traffic.yml

import os
import requests
import csv
from datetime import datetime, timedelta
from github import Github

def fetch_visitor_stats(repo_url, headers):
    visitors_url = f"{repo_url}/traffic/views"
    visitors_response = requests.get(visitors_url, headers=headers)
    if visitors_response.status_code == 200:
        visitor_stats = visitors_response.json()
        return visitor_stats['views']
    else:
        raise Exception(f"Failed to fetch Visitor stats for repository. Error: {visitors_response.status_code}")

def fetch_git_clones_stats(repo_url, headers):
    clones_url = f"{repo_url}/traffic/clones"
    clones_response = requests.get(clones_url, headers=headers)
    if clones_response.status_code == 200:
        clone_stats = clones_response.json()
        return clone_stats['clones']
    else:
        raise Exception(f"Failed to fetch Git Clones stats for repository. Error: {clones_response.status_code}")

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
            visitor_stats = fetch_visitor_stats(repo_url, headers)
            git_clones_stats = fetch_git_clones_stats(repo_url, headers)

            check_visitor_dates_list = []
            check_git_clones_dates_list = []

            today = datetime.now().date()
            yesterday = today - timedelta(days=1)

            for views_stats in visitor_stats:
                views_date_object = datetime.strptime(views_stats['timestamp'], '%Y-%m-%dT%H:%M:%SZ').date()
                check_visitor_dates_list.append(views_date_object)
                if views_date_object == yesterday:
                    date_only = yesterday
                    views = views_stats['count']
                    unique_visitors = views_stats['uniques']

            if yesterday not in check_visitor_dates_list:
                date_only = yesterday
                views = 0
                unique_visitors = 0


            for clones_stats in git_clones_stats:
                clones_date_object = datetime.strptime(clones_stats['timestamp'], '%Y-%m-%dT%H:%M:%SZ').date()
                check_git_clones_dates_list.append(clones_date_object)

                if clones_date_object == yesterday:
                    date_only = yesterday
                    clones = clones_stats['count']
                    unique_cloners = clones_stats['uniques']

            if yesterday not in check_git_clones_dates_list:
                date_only = yesterday
                clones = 0
                unique_cloners = 0


            result = f"{date_only},{repo_name},{views},{unique_visitors},{clones},{unique_cloners}"
            data.append(result)
        except Exception as e:
            print(f"Failed to fetch traffic stats for repository '{repo_name}': {str(e)}")

    print(data)
    
    g = Github(os.getenv('TOKEN'))
    repo = g.get_repo('analyticsinmotion/github-stats')
    file_path = 'data/traffic.csv'

    try:
        update_csv_file(repo, file_path, data)
        print("Data appended to CSV file successfully.")
    except Exception as e:
        print(f"Failed to update CSV file: {str(e)}")

if __name__ == "__main__":
    main()
