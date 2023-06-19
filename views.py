import os
import requests
import csv
from datetime import datetime
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
            if traffic_stats:
                latest_views = traffic_stats[-1:]
                if not latest_views:
                    current_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                    latest_views = [{'timestamp': current_date, 'count': 0, 'uniques': 0}]

                datetime_object = datetime.strptime(latest_views[0]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                date_only = datetime_object.date()
                views = latest_views[0]['count']
                unique_visitors = latest_views[0]['uniques']
                result = f"{date_only},{repo_name},{views},{unique_visitors}"
                data.append(result)
        except Exception as e:
            print(f"Failed to fetch traffic stats for repository '{repo_name}': {str(e)}")

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
