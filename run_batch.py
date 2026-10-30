import subprocess
from pathlib import Path

def main():
    """This function is responsible for running the JAR files required to convert FIT files to CSV data files"""

    # specify directory containing files to be converted
    parent_directory = Path("output")
    directory_in = parent_directory / 'fit'

    # path to JAR file for converting from .fit to .csv
    jar_path = Path("SDK") / "FitSDKRelease_21.158.00" / "java" / "FitCSVTool.jar"

    # loop through each .fit file and run the JAR file to convert it to CSV.
    for file in directory_in.glob("*.fit"):
        output_prefix = file.with_suffix("")
        # run JAR file to perform conversion from FIT activity to data CSV with formatted column headers
        subprocess.run(
            [   
                "java",
                "-jar", str(jar_path),
                "-b", str(file),
                str(output_prefix),
                "--defn",
                "none",
                "--data",
                "record",
                ],
            check=True
        )
    print("Successfully converted all .fit files to .csv")

if __name__ == '__main__':
   main()




