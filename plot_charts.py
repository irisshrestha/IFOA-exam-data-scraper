import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import math

# Import relevant csv
clean_data = pd.read_csv("Outputs/clean_data.csv")
subjects_csv = pd.read_csv("Inputs/subjects.csv", header=0)
dates_csv = pd.read_csv("Inputs/dates.csv", header=0)
mapping_csv = pd.read_csv("Inputs/chart_mapping.csv", header=0)

# Convert to date time format
clean_data['Date'] = pd.to_datetime(clean_data['Date'])

# Add in mapping columns to create chart groupings
clean_data = clean_data.merge(mapping_csv, on="Subject",how="left")
grouped_df = clean_data.groupby("Mapping")

# Loop over groups to create a new figure for each group
for group, df in grouped_df:

    # Break up each group into subgroups by subjects
    groups_in_sub = df['Subject'].unique()

    ncols = 2
    nrows = math.ceil(len(groups_in_sub) / ncols)

    # Create one figure per group, with one axis per subgroup
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(8, 4 * nrows),
        sharex=False
    )
    # If there is only one item in the subgroup
    if nrows == 1 and ncols == 1:
        axes = [axes]
    # Flatten to change from multi dimension object to one dimension so allow iterations
    else:
        axes = axes.flatten()

    # Loop over each subgroup and plot a new axis
    for ax, (subgroup, subgroup_df) in zip(axes, df.groupby('Subject')):

        # Plot Pass mark
        ax.plot(subgroup_df['Date'], subgroup_df['Pass Mark'], "-o", color="Blue", label="Pass Mark")

        ax.set_title(f"{subgroup.upper()}")
        ax.set_ylim(20,80)

        #Format so dates are shown correctly
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[4,9]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
        ax.tick_params(axis='x', rotation=90)

        # Plot pass rate on the same axis
        ax2 = ax.twinx()
        ax2.plot(subgroup_df['Date'], subgroup_df['Pass Rate'] * 100, "-o", color="red", label="Pass Rate (%)")

        ax2.set_ylim(20, 80)
        ax2.set_axis_off()

    # Get handles and labels for the two plots of the last iteration
    # This is then used for the legend
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles = handles1 + handles2
    labels = labels1 + labels2
    total_axes = len(axes)
    fig.legend(handles, labels, loc='upper center', ncol=2)

    # Remove any blank axes
    for i in range(len(groups_in_sub), total_axes):
        fig.delaxes(axes[i])

    # Format the chart
    plt.tight_layout()

    #Save as png
    plt.savefig(f"Charts/{group}.png")
