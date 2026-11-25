
import os
import subprocess

seven_zip = r"C:\Program Files\7-Zip\7z.exe"

archive = r"C:\Users\omech\ycbv\ycbv_train_real.zip"

output_dir = r"C:\Users\omech\ycbv\real_subset"

list_file = os.path.join(output_dir, "image_list.txt")

# Read the 1,200 selected image paths
with open(list_file, "r", encoding="utf-8") as f:
    image_paths = [
        line.strip()
        for line in f
        if line.strip()
    ]

print("Images requested:", len(image_paths))

# Extract only the selected images
command = [
    seven_zip,
    "x",
    archive,
    f"-o{output_dir}",
    f"-i@{list_file}",
    "-y"
]

print("\nStarting extraction...")

result = subprocess.run(
    command,
    capture_output=True,
    text=True
)

print("\n7-Zip output:")
print(result.stdout[-4000:])

if result.stderr:
    print("\nWarnings/errors:")
    print(result.stderr[-2000:])

# Verify that the requested images were extracted
extracted = []

for archive_path in image_paths:
    relative_path = archive_path.replace("\\", os.sep)
    full_path = os.path.join(output_dir, relative_path)

    if os.path.isfile(full_path) and os.path.getsize(full_path) > 0:
        extracted.append(full_path)

print("\nEXTRACTION SUMMARY")
print("Requested images:", len(image_paths))
print("Successfully extracted:", len(extracted))
print("Missing or empty:", len(image_paths) - len(extracted))
print("7-Zip return code:", result.returncode)

if len(extracted) == len(image_paths):
    print("\nSUCCESS: All selected images were extracted.")
else:
    print("\nWARNING: Some images are missing or empty.")
