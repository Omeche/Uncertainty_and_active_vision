
import os
import zipfile

source_dir = r"C:\Users\omech\ycbv\real_subset"

zip_path = r"C:\Users\omech\ycbv\real_subset.zip"

print("Preparing ZIP archive...")

total_files = 0

with zipfile.ZipFile(
    zip_path,
    "w",
    compression=zipfile.ZIP_STORED
) as archive:

    for root, dirs, files in os.walk(source_dir):
        for filename in files:

            # Do not include temporary test list
            if filename == "test_image_list.txt":
                continue

            full_path = os.path.join(root, filename)

            relative_path = os.path.relpath(
                full_path,
                os.path.dirname(source_dir)
            )

            archive.write(full_path, relative_path)

            total_files += 1

print("\nZIP creation completed.")
print("Files:", total_files)
print("ZIP size:", round(os.path.getsize(zip_path) / (1024**2), 2), "MB")
print("Location:", zip_path)
