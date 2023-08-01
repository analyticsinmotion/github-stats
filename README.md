
<h1 align="center">:chart_with_upwards_trend: GitHub Stats</h1>

<!-- badges: start -->
<div align="center">
  
[![Python Version](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=ffdd54)](https://www.python.org/downloads/)&nbsp;&nbsp;
![Experimental](https://img.shields.io/badge/experimental-yes-brightgreen.svg)&nbsp;&nbsp;
[![MIT license](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/analyticsinmotion/github-stats/blob/main/LICENSE)&nbsp;&nbsp;
[![GitHub Metrics](https://github.com/analyticsinmotion/github-stats/actions/workflows/traffic.yml/badge.svg)](https://github.com/analyticsinmotion/github-stats/actions/workflows/traffic.yml)&nbsp;&nbsp;
[![GitHub Activity Metrics](https://github.com/analyticsinmotion/github-stats/actions/workflows/activity.yml/badge.svg)](https://github.com/analyticsinmotion/github-stats/actions/workflows/activity.yml)&nbsp;&nbsp;
[![Analytics in Motion](https://raw.githubusercontent.com/analyticsinmotion/.github/main/assets/images/analytics-in-motion-github-badge-rounded.svg)](https://www.analyticsinmotion.com)
  
</div>
<!-- badges: end -->

<!-- DESCRIPTION -->
## Description
This project is designed to capture and store data related to user activity (views, unique visitors, clones, forks, stars, etc.) for Analytics in Motion's public repositories on GitHub. The primary purpose of this project is for us to collect more data on user interactions on our Github repositories beyond the current limitations (such as the ability to only see 14 days worth of traffic data). 
<br /><br />


## Data Overview
The following table provides an overview of the data that will be extracted and stored.

| Metric  | Description | 
| ------------- | ------------- |
| views  | A view refers to the number of times a specific page or resource within the repository has been accessed or loaded. It represents the number of times the repository's main page or any of its subpages (such as code files, issues, or pull requests) have been viewed. |
| unique visitors  | Unique visitors represent the number of distinct individuals who have visited the repository during a specific time period. If the same user visits your repository multiple times within a specified period (typically 24 hours), they are counted as a single unique visitor. |
| clones  | Clones refer to the number of times the repository has been copied. When someone clones your repository, they make an exact replica of the repository, including all its files, branches, commit history, and other associated data. |
| unique cloners  | Unique cloners represent the number of distinct users who have performed at least one clone of the repository during a specific time period. Similar to unique visitors, unique cloners are counted only once, regardless of the number of clones they perform. |
| watch  | Watching a repository means you opt to receive notifications about its activity. This includes new issues, pull requests, and other updates. Watching is more proactive than starring, as it means you want to stay up-to-date with what's happening in the repository. This is particularly useful when you want to keep track of developments or participate in discussions related to the project. |
| fork  | Forking a repository creates a copy of the original repository under your GitHub account. This action allows you to freely experiment with the code without affecting the original project. Forking is often the first step in contributing to an open-source project. After forking, you can make changes to the code in your forked repository, commit those changes, and then submit a "Pull Request" to the original repository, suggesting the changes you made. The maintainers of the original repository can then review your changes and decide whether to merge them into the main project. |
| star  | When you Star a repository, you are essentially bookmarking it. This action indicates that you have an interest in the repository and want to keep track of it. Starred repositories can be easily accessed from your profile, allowing you to find them quickly. It's a way of showing appreciation or support for a project without necessarily contributing to it directly. |

<br /><br />

<!-- DATA DICTIONARY -->
## Data Dictionary

<details>
  <summary><h3>&nbsp;User Traffic</h3></summary>

The <a href="https://github.com/analyticsinmotion/github-stats/blob/main/data/traffic.csv">traffic.csv</a> file contains time series information relating to views, unique visitors, clones and unique cloners to each repository.

**File Details**
<br />
*Filename:* traffic
<br />
*Extension:* .csv
<br />
*Delimiter:* Comma (,)
<br />
*Header:* True


**Structure**

| Column Name  | Data Type | Description |
| ------------- | ------------- | ------------- |
| date  | Date (yyyy-mm-dd) | The date when the data was recorded |
| repository  | Text | The name of the repository |
| views  | Numeric | The number of repository views |
| unique_visitors  | Numeric | The number of unique visitors to the repository |
| clones  | Numeric | The number of times a repository is cloned |
| unique_cloners  | Numeric | The number of unique cloners of the repository |

</details>

<details>
  <summary><h3>&nbsp;User Activity</h3></summary>

The <a href="https://github.com/analyticsinmotion/github-stats/blob/main/data/activity.csv">traffic.csv</a> file contains cumulative time series information relating to stars, watchers and forks for each repository.

**File Details**
<br />
*Filename:* activity
<br />
*Extension:* .csv
<br />
*Delimiter:* Comma (,)
<br />
*Header:* True


**Structure**

| Column Name  | Data Type | Description |
| ------------- | ------------- | ------------- |
| date  | Date (yyyy-mm-dd) | The date when the data was recorded |
| repository  | Text | The name of the repository |
| stars  | Numeric | The number of times a repository has been starred |
| watchers  | Numeric | The number of users watching a repository |
| forks  | Numeric | The number of times a repository has been forked |


</details>

<br /><br />

<!-- DIRECTORY STRUCTURE -->
## Directory Structure

    github-stats
    ├── .github           
    │   ├── workflows
    │   │   └── activity.yml
    │   │   └── traffic.yml
    │   └── assets
    │       └── images 
    ├── data
    │   ├── activity.csv 
    │   └── traffic.csv
    ├── src
    │   ├── activity.py 
    │   └── traffic.py 
    ├── .gitignore
    ├── CHANGELOG.md
    ├── LICENSE  
    ├── README.md              
    └── requirements.txt                    

                       
<br /><br />


