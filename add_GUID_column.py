import os
import csv
from pathlib import Path

def main():
    """This function is responsible for adding a GUID associated with each activity to all rows from said activity"""

    # Location of CSV files
    parent_path = Path("output")
    folder_path = parent_path / "fit"

    count = 0
    
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('_data.csv'):  # Check if the file is a CSV file
            count +=1

            csv_file_path = os.path.join(folder_path, filename)

            # Use the filename (without extension) as the GUID
            file_guid = os.path.splitext(filename)[0]

            # Read the CSV file and add the same GUID to all rows
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames

                if fieldnames is None:
                    print(f"Skipping {filename} due to missing headers.")
                    continue  # Skip files without headers

                if 'GUID' not in fieldnames:
                    fieldnames.append('GUID')  # Add the new 'GUID' column

                rows = []
                for row in reader:
                    # Ensure all keys exist in the row to prevent missing field errors
                    row = {key: row.get(key, '') for key in fieldnames}
                    row['GUID'] = file_guid  # Assign the same GUID to every row
                    rows.append(row)

            # Write the updated data back to the CSV file
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()  # Write the header
                writer.writerows(rows)  # Write the rows with GUIDs

            print(f"GUID added to {filename} (GUID: {file_guid})")

    print(f"{count} CSV files have been updated with GUIDs.")

if __name__ == '__main__':
   main()