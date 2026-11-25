import os
import shutil

possible_paths = [
    r"C:\Program Files\7-Zip\7z.exe",
    r"C:\Program Files (x86)\7-Zip\7z.exe"
]

seven_zip = shutil.which("7z")

if not seven_zip:
    for path in possible_paths:
        if os.path.exists(path):
            seven_zip = path
            break

if seven_zip:
    print("7-Zip found:", seven_zip)
else:
    print("7-Zip still not found.")