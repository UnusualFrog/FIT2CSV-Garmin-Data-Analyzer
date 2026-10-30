import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Color schema for bar chart
colors = [
    "red",
    "orange",
    "yellow",
    "lime",
    "green",
    "springgreen",
    "cyan",
    "cornflowerblue",
    "blue",
    "violet",
    "magenta",
    "deeppink",
]


def get_hr_zone(hr):
    if hr < 119 or pd.isna(hr):
        return "Zone 0 (0-118)"
    elif hr < 132:
        return "Zone 1 (119-131)"
    elif hr < 144:
        return "Zone 2 (132-143)"
    elif hr < 155:
        return "Zone 3 (133-154)"
    elif hr < 167:
        return "Zone 4 (155-166)"
    else:
        return "Zone 5 (167+)"


def generate_monthly_distance(dataframe, path):
    df_monthly = dataframe.copy()
    df_monthly = df_monthly.drop(columns=["timestamp[s]", "GUID"])
    # print(df_monthly.head())

    # Group by monthly average distance
    monthly_distance = (
        df_monthly.set_index("timestamp[UTC]").resample("M")["distance[m]"].mean()
    )

    # Plot avergae distance per month on a bar chart
    monthly_distance.plot(
        kind="bar",
        figsize=(12, 6),
        title="Monthly Average Distance",
        color=colors[: len(monthly_distance)],
        xlabel="Months",
        ylabel="Avg. Distance (m)"
    )

    plt.xticks(
        ticks=range(len(monthly_distance)),
        labels=monthly_distance.index.strftime("%b %Y"),
        rotation=45,
    )

    plt.title = "Avg. Distance by Month"

    plt.savefig(path / "avg_distance_month.png")


def generate_max_hr(dataframe, path):
    df = dataframe.copy()
    df = df.drop(
        columns=["timestamp[s]", "GUID", "distance[m]", "power[watts]", "speed[m/s]"]
    )
    df = df.set_index("timestamp[UTC]")

    # Group by monthly max heartrate
    max_hr = df.resample("M")["heart_rate[bpm]"].max()
    # print(max_hr.head())

    # Initialise figure
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot line graph
    ax.plot(
        max_hr.index,
        max_hr.values,
        marker="o",
    )

    # Add grid for readability
    ax.grid(True, linestyle="--", alpha=0.4)

    # Set labels
    ax.set_ylabel("Max Heartrate [bpm]")
    ax.set_xlabel("Month")
    ax.set_title("Max Heartrate by Month")
    plt.savefig(path / "max_hr_quarterly.png")


def generate_hr_zone_pie(dataframe, path):
    df = dataframe.copy()
    df = df.drop(
        columns=["timestamp[s]", "GUID", "distance[m]", "power[watts]", "speed[m/s]"]
    )

    # Add heart rate zone column
    df["hr_zone"] = df["heart_rate[bpm]"].apply(lambda x: get_hr_zone(x))
    
    # drop heart rate
    df = df.drop(columns=["heart_rate[bpm]"])

    # Group by heart rate zone
    df = df.groupby("hr_zone").size().to_frame("count")

    # Get total row count
    total_rows = df["count"].sum()

    # Calculate zone percentages
    df["hr_percent"] = round((df["count"] / total_rows) * 100)
    print(df.head(10))

    df.plot.pie(
        y='hr_percent',
        labels=df.index,
        autopct='%1.1f%%',
        figsize=(7,7),
        ylabel="",
        legend=False,
    )

    plt.suptitle("Heart Rate Zone Percentages")
    plt.savefig(path / "hr_zone_percent.png")


def main():
    """This function is responsible for visualizing the data in aggregate into graphs for analysis"""

    # Set relative filepaths
    data_path = Path("output")
    csv_path = data_path / "csv"
    filename = csv_path / "output.csv"
    graph_path = data_path / "graph"

    # Generate directory to save graphs
    graph_path.mkdir(parents=True, exist_ok=True)

    # Load CSV file into a DataFrame
    df = pd.read_csv(filename)
    # print(df.head())

    df_sample = df.sample(frac=0.1)

    # Add UTC timestamp
    df_utc = df_sample.copy()
    df_utc["timestamp[UTC]"] = df_utc["timestamp[s]"].apply(
        lambda x: datetime(1989, 12, 31, tzinfo=timezone.utc) + timedelta(seconds=x)
    )
    print(df_utc.head())

    # Generate graphs
    generate_monthly_distance(df_utc, graph_path)
    generate_max_hr(df_utc, graph_path)
    generate_hr_zone_pie(df_utc, graph_path)


if __name__ == "__main__":
    main()
