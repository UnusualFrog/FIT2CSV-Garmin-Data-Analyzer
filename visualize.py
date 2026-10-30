import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone


def main():
    """This function is responsible for visualizing the data in aggregate into graphs for analysis"""

    # Set relative filepaths
    data_path = Path("output")
    csv_path = data_path / "csv"
    filename = csv_path / "output.csv"

    # Load CSV file into a DataFrame
    df = pd.read_csv(filename)
    # print(df.head())

    df_sample = df.sample(frac=0.1)

    # Add UTC timestamp
    df_utc = df_sample.copy()
    df_utc["timestamp[UTC]"] = df_utc["timestamp[s]"].apply(
        lambda x: datetime(1989, 12, 31, tzinfo=timezone.utc) + timedelta(seconds=x)
    )
    # print(df_utc.head())

    df_monthly = df_utc.copy()
    df_monthly = df_monthly.drop(columns=["timestamp[s]", "GUID"])
    print(df_monthly.head())

    monthly_distance = (
        df_monthly.set_index("timestamp[UTC]")
        .resample("M")["distance[m]"]
        .mean()
    )


    colors = [
    "red", "orange", "yellow", "lime",
    "green", "springgreen", "cyan", "azure",
    "blue", "violet", "magenta", "deeppink"
]

    monthly_distance.plot(
        kind="bar",
        figsize=(12,6),
        title="Monthly Average Distance",
        color=colors[:len(monthly_distance)]
    )

    plt.xticks(
        ticks=range(len(monthly_distance)),
        labels=monthly_distance.index.strftime("%b %Y"),
        rotation=45
    )

    plt.ylabel = "Avg. Distance"
    plt.xlabel = "Months"
    plt.title = "Avg. Distance by Month"

    plt.show()




if __name__ == "__main__":
    main()
