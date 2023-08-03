# This python script accesses the CSV data in the
# analyticsinmotion/github-stats repo to extract the data,
# transform it, and plot the number of views by day of the
# week. This file is scheduled to run once a day at 12:25am
# using cron. The scheduling code is located in
# .github/workflows/plot-views-by-day.yml file.

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from github import Github


def fetch_csv_data(github_username, repository_name, csv_file_path):
    data_source_url = f'https://raw.githubusercontent.com/{github_username}/{repository_name}/main/{csv_file_path}'
    df = pd.read_csv(data_source_url)

    # Subset dataframe to the last 365 days
    # Step 1: - Convert the "date" column to a pandas datetime object
    df['date'] = pd.to_datetime(df['date'])

    # Step 2: - Calculate the current date
    current_date = datetime.today()

    # Step 3: - Calculate the date 365 days ago from the current date
    last_year_date = current_date - timedelta(days=365)

    # Step 4: - Filter the DataFrame to include only dates from the last 365 days
    df = df[df['date'] >= last_year_date]

    return df


def transform_df_for_plot(dataframe_name):
    # Step 1: - Add a new column that converts the date column to a datetime format
    dataframe_name['datetime'] = pd.to_datetime(dataframe_name['date'])
    # Step 2: - Create a new column 'day_of_week' containing the day of the week as a string
    dataframe_name['day_of_week'] = dataframe_name['datetime'].dt.day_name()
    # Step 3: - Create a new column 'day' containing integers representing the day of the week, where Monday is 0 and Sunday is 6.
    dataframe_name['day'] = dataframe_name['datetime'].dt.dayofweek
    # Step 4: - Group the data by day of the week and average the views. Sort by the numeric day variable so the coming x axis in plot is ordered correctly
    dataframe_name = dataframe_name.groupby(['day_of_week','day'])['views'].mean().reset_index().sort_values(by='day')
    return dataframe_name


def plot_views_by_day(dataframe_name):
    fig, ax = plt.subplots()

    bars = ax.bar(
        x=dataframe_name['day_of_week'],
        height=dataframe_name['views'],
        width=0.55
        )

    # Remove the top, right and left spines (figure borders)
    # Also, make the bottom spine gray instead of black.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')

    # Remove the ticks as well.
    ax.tick_params(bottom=False, left=False)

    # Add a horizontal grid (but keep the vertical grid hidden)
    # Color the lines a light gray as well.
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    # Grab the color of the bars so we can make the text the same color.
    bar_color = bars[0].get_facecolor()

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            round(bar.get_height(), 1),
            horizontalalignment='center',
            color=bar_color,
            weight='bold'
            )

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    formatted_date = yesterday.strftime("%B %d, %Y")

    # Add labels and a title. Note the use of `labelpad` and `pad` to add some
    # extra space between the text and the tick labels.
    ax.set_xlabel('Day of the Week', labelpad=15, color='#333333')
    ax.set_ylabel('Views', labelpad=15, color='#333333')
    title = 'Average Views by Day of the Week\n\nas at ' + formatted_date
    ax.set_title(title, pad=25, color='#333333', weight='bold')

    # Make the chart fill out the figure better.
    fig.tight_layout()



    # Set the dpi to a higher value for a high-resolution image
    high_resolution_dpi = 300

    file_name = f"plot-views-by-day.png"

    try:
        plt.savefig(file_name, dpi=high_resolution_dpi)
        print(f"Plot successfully saved as '{file_name}'")
        file_path = os.path.abspath(file_name)
        print(f"Plot successfully saved at: '{file_path}'")
    except Exception as e:
        print(f"Error occurred while saving the plot: {e}")

    # Close the plot to avoid displaying it
    plt.close()


def main():
    # Step 1: - Instantiate some global variables
    github_username = 'analyticsinmotion'
    repository_name = 'github-stats'
    csv_file_path = 'data/traffic.csv'

    # Step 2: - Fetch the last 12 months worth of CSV data from github
    df = fetch_csv_data(github_username, repository_name, csv_file_path)

    # Step 3: - Transform the data so it is ready for plotting
    df = transform_df_for_plot(df)

    # Step 4: - Create the plot, and save it
    plot_views_by_day(df)


if __name__ == "__main__":
    main()
