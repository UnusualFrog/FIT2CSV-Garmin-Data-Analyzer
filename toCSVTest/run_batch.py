import subprocess
from pathlib import Path

# Specify directory containing files to be converted
parent_directory = Path("output")
directory_in = parent_directory / 'fit'

# Path to JAR file for converting from .fit to .csv
jar_path = Path("toCSVTest") / "FitSDKRelease_21.158.00" / "java" / "FitCSVTool.jar"

# Loop through each .fit file and run the JAR file to convert it to CSV.
for file in directory_in.glob("*.fit"):
    output_prefix = file.with_suffix("")
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





