
import subprocess
import os

seven_zip = r"C:\Program Files\7-Zip\7z.exe"

archive_path = r"C:\Users\omech\ycbv\ycbv_train_real.zip"

output_dir = r"C:\Users\omech\ycbv\real_annotations"

os.makedirs(output_dir, exist_ok=True)

# Extract only the three annotation files from every scene.
patterns = [
    "train_real\\*\\scene_gt.json",
    "train_real\\*\\scene_gt_info.json",
    "train_real\\*\\scene_camera.json"
]

command = [
    seven_zip,
    "x",
    archive_path,
    *patterns,
    f"-o{output_dir}",
    "-y"
]

print("Extracting annotation files...")
print("Destination:", output_dir)

result = subprocess.run(command)

print("\n7-Zip return code:", result.returncode)

if result.returncode == 0:
    print("Extraction completed.")
else:
    print("Extraction reported an issue. Send me the output.")
