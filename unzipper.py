import gzip
import shutil
from pathlib import Path
from zipfile import ZipFile


def main():
    """This function is responsible for unziping the parent file containing individual, zipped, activity files and creating required directories"""

    # parent zip file containing all zipped data files
    parent_filename = "activities.zip"

    # paths for output file directories
    output_path = Path("output")
    # path to zipped data files (.fit.gz)
    activities_path = output_path / "activities"
    # path to unzipped data files (.fit)
    fit_path = output_path / "fit"

    # loading the parent zip file and unzip it to the activities folder
    with ZipFile(parent_filename, "r") as zObject:
        # Extracts files to output directory, which is created if it does not exist
        zObject.extractall(path=output_path)
        print("Unzipping parent file: " + parent_filename)

    # create subdirectories
    activities_path.mkdir(parents=True, exist_ok=True)
    fit_path.mkdir(parents=True, exist_ok=True)


    # track number of files
    count = 0
    print("Unzipping individual data files...")
    for filepath in activities_path.iterdir():
        count += 1
        # ensure file is of format (.fit.gz)
        if filepath.is_file() and filepath.suffix == ".gz":
            # Construct output file path with .gz removed
            output_file = fit_path / filepath.stem

            # open zipped file
            with gzip.open(filepath) as f_in:
                # copy zipped file to fit directory as an unzipped file
                with open(output_file, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

    print(f"Completed unzipping of {count} files from {parent_filename}")

if __name__ == '__main__':
   main()