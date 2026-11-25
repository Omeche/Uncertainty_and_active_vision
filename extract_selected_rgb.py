
import os
import subprocess

# Original multi-volume archive
archive = r"C:\Users\omech\ycbv\ycbv_train_real.zip"

# Downloaded image list
list_file = r"C:\Users\omech\Downloads\image_list_both_objects.txt"

# Destination for the selected images
output_dir = r"C:\Users\omech\ycbv\selected_rgb"

# 7-Zip executable
seven_zip = r"C:\Program Files\7-Zip\7z.exe"

os.makedirs(output_dir, exist_ok=True)

# Verify inputs
for path in [archive, list_file, seven_zip]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not found: {path}")

with open(list_file, "r") as f:
    image_paths = [
        line.strip().replace("/", "\\")
        for line in f
        if line.strip()
    ]

print("Images requested:", len(image_paths))

# Extract only the listed files
command = [
    seven_zip,
    "x",
    archive,
    f"-o{output_dir}",
    "-y",
    f"-i@{list_file}"
]

result = subprocess.run(
    command,
    capture_output=True,
    text=True
)

print("\n7-Zip return code:", result.returncode)
print("\nLast part of output:")
print(result.stdout[-3000:])

if result.stderr:
    print("\nWarnings/errors:")
    print(result.stderr[-2000:])

# Verify extraction
found = []

for relative_path in image_paths:
    expected_path = os.path.join(
        output_dir,
        relative_path
    )

    if os.path.isfile(expected_path):
        found.append(expected_path)

print("\nImages successfully extracted:", len(found))
print("Images missing:", len(image_paths) - len(found))
