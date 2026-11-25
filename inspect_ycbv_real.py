
import zipfile
import os
import subprocess

archive_path = r"C:\users\Omech\ycbv\ycbv_train_real.zip"


seven_zip = r"C:\Program Files\7-Zip\7z.exe"

print("Archive exists:", os.path.exists(archive_path))
print("Archive size:", round(os.path.getsize(archive_path) / (1024**3), 2), "GB")

print("\nInspecting archive...\n")

result = subprocess.run(
    [seven_zip, "l", archive_path],
    capture_output=True,
    text=True,
    errors="replace"
)

print("Return code:", result.returncode)

if result.returncode == 0:
    lines = result.stdout.splitlines()

    print("\nFirst 70 archive entries:\n")

    for line in lines[:70]:
        print(line)

    print("\nArchive listing summary:\n")

    for line in lines[-15:]:
        print(line)

else:
    print("7-Zip reported an error:")
    print(result.stderr[-3000:])
