import os

archive_path = r"C:\Users\omech\ycbv\ycbv_train_real.zip"

folder = os.path.dirname(archive_path)
base = os.path.splitext(os.path.basename(archive_path))[0]

expected_files = [
    base + ".z01",
    base + ".zip"
]

for filename in expected_files:
    path = os.path.join(folder, filename)

    if os.path.exists(path):
        size = os.path.getsize(path) / (1024**3)
        print(f"FOUND: {filename} ({size:.2f} GB)")
    else:
        print(f"MISSING: {filename}")