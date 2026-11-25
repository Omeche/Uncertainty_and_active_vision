
import os
import subprocess

seven_zip = r"C:\Program Files\7-Zip\7z.exe"

archive = r"C:\Users\omech\ycbv\ycbv_train_real.zip"

output_dir = r"C:\Users\omech\ycbv\real_subset"

list_file = os.path.join(output_dir, "test_image_list.txt")

# Use one image from the training subset
image_path = (
    r"train_real\000087\rgb\000001.png"
)

with open(list_file, "w", encoding="utf-8") as f:
    f.write(image_path + "\n")

command = [
    seven_zip,
    "x",
    archive,
    f"-o{output_dir}",
    f"-i@{list_file}",
    "-y"
]

print("Testing extraction...")
print("Image:", image_path)

result = subprocess.run(
    command,
    capture_output=True,
    text=True
)

print("\n7-Zip output:")
print(result.stdout[-3000:])

if result.stderr:
    print("\nErrors/warnings:")
    print(result.stderr[-1500:])

extracted_file = os.path.join(
    output_dir,
    "train_real",
    "000087",
    "rgb",
    "000001.png"
)

print("\nReturn code:", result.returncode)
print("File exists:", os.path.exists(extracted_file))

if os.path.exists(extracted_file):
    print("File size:", os.path.getsize(extracted_file), "bytes")
