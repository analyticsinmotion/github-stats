# CHANGELOG
This changelog file outlines a chronologically ordered list of the changes made on this project. 
It is organized by version and release date followed by a list of Enhancements, New Features, Bug Fixes, and/or Breaking Changes.
<br /><br />

## Version 0.0.3 (Latest) 
**Released:** July 20, 2023<br />
**Tag:** v0.0.3

### Breaking Changes

- views.py has been replaced by traffic.py in the main directory
- views.yml has been replaced by traffic.yml in the .github/workflows directory
- views.csv has been replaced by traffic.csv in the data directory
- traffic.csv adds two extra columns to the table schema ("clones" and "unique_cloners") compared to the old views.csv file
- traffic.csv renames two of the columns from the old views.csv file:
  - "repo" renamed to "repository"
  - "visitor" renamed to "unique_visitor"

### Enhancements

- Daily capture process now includes data for clones and unique cloners for each repository. 

<br /><br />

## Version 0.0.2 
**Released:** July 13, 2023<br />
**Tag:** v0.0.2

### Enhancements

- Enhanced the process for extracting views and unique visitors. In version 0.0.1 the views.py script was scheduled to run at 11:45pm to capture the data for that day. However, sometimes GitHub would update the metrics between 11:45pm and midnight, essentially making the views.py data extraction outdated. Having the scheduling so close to midnight also introduced a risk that if the CRON job (in GitHub actions) was delayed it would also potentially lead to inaccurate results. The new views.py script is run at 12:25am and captures the stats from the previous day, essentially removing the issues faced in version 0.0.1.

<br /><br />
## Version 0.0.1 (Initial Release)
**Released:** June 20, 2023<br />
**Tag:** v0.0.1

This is the initial release
