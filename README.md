
<h1 align="center">:chart_with_upwards_trend: GitHub Stats</h1>

<!-- badges: start -->
<div align="center">
  
[![Python Version](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=ffdd54)](https://www.python.org/downloads/)&nbsp;&nbsp;
![Experimental](https://img.shields.io/badge/experimental-yes-brightgreen.svg)&nbsp;&nbsp;
[![MIT license](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/analyticsinmotion/github-stats/blob/main/LICENSE)&nbsp;&nbsp;
[![GitHub Metrics](https://github.com/analyticsinmotion/github-stats/actions/workflows/views.yml/badge.svg)](https://github.com/analyticsinmotion/github-stats/actions/workflows/views.yml)&nbsp;&nbsp;
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
| views  | The number of views per day for each repository. |
| unique users  | The number of unique visitors to each repository per day. |
| clones  | TBD |
| unique cloners  | TBD |
| watch  | TBD |
| fork  | TBD |
| star  | TBD |

<br /><br />

<!-- DATA DICTIONARY -->
## Data Dictionary

<details>
  <summary><h3>&nbsp;Views and Unique Users</h3></summary>
  

The <a href="https://github.com/analyticsinmotion/github-stats/blob/main/data/views.csv">views.csv</a> file contains time series information relating to views and unique visitors to each repository for each day.

**File Details**
<br />
*Filename:* views
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
| repo  | Text | The name of the repository |
| views  | Numeric | The number of repository views |
| visitors  | Numeric | The number of unique visitors to the repository |

</details>

<br /><br />

<!-- DIRECTORY STRUCTURE -->
## Directory Structure

    github-stats
    ├── .github           
    │   └── workflows
    │       └── views.yml  
    ├── data
    │   └── views.csv 
    ├── .gitignore
    ├── CHANGELOG.md 
    ├── README.md              
    ├── requirements.txt                    
    ├── LICENSE                      
    └── views.py                       
<br /><br />


