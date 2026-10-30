import pandas as pd
from pathlib import Path

def main():
    """This function is responsible for condensing individual CSV activity files into one super file for aggregation"""

    # Create relative paths to input and output directories
    parent_dir = Path("output")
    input_dir = parent_dir  / "fit"
    output_dir = parent_dir / "csv"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect csv data files
    csv_files = list(input_dir.glob("*_data.csv"))

    # Initialise empty list and dataframe for downstream collection and concatenation
    df_list = []
    out = pd.DataFrame()

    # Declare path on concatenated CSV files
    output_file = output_dir / 'output.csv'

    print("Collecting individual CSV files...")
    # Collect csv files in a list
    for file in csv_files:
        df = pd.read_csv(file, low_memory=False)
        df_list.append(df)

    print("Concatenating collected data...")
    # Concatenate list of dataframes into one dataframe
    out = pd.concat(df_list)

    # Drop irrelevant columns
    out = out[['record.timestamp[s]', 'record.distance[m]', 'record.heart_rate[bpm]', 'record.power[watts]', 'record.enhanced_speed[m/s]', 'GUID']]

    # Rename columns for readability
    out.rename(columns={'record.timestamp[s]': 'timestamp[s]', 'record.distance[m]': 'distance[m]', 'record.heart_rate[bpm]': 'heart_rate[bpm]', 'record.power[watts]': 'power[watts]', 'record.enhanced_speed[m/s]': 'speed[m/s]'}, errors="raise", inplace=True)

    # Save dataframe as CSV
    out.to_csv(output_file, index=False)
    print("Successfully concatenated and pre-processed data")

if __name__ == '__main__':
   main()