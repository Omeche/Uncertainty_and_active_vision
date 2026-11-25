
import os
import json

root = r"C:\Users\omech\ycbv\real_annotations\train_real"

train_scenes = [
    "000087", "000038", "000040",
    "000011", "000014", "000035"
]

val_scenes = [
    "000028", "000033", "000070",
    "000086", "000026", "000027"
]

output_dir = r"C:\Users\omech\ycbv\real_subset"

os.makedirs(output_dir, exist_ok=True)

selected = {
    "train": train_scenes,
    "val": val_scenes
}

archive_paths = []

for split, scenes in selected.items():

    print(f"\n{split.upper()}")

    for scene in scenes:

        scene_dir = os.path.join(root, scene)

        camera_path = os.path.join(
            scene_dir, "scene_camera.json"
        )

        with open(camera_path, "r") as f:
            camera = json.load(f)

        image_ids = sorted(
            camera.keys(), key=lambda x: int(x)
        )

        count = min(100, len(image_ids))

        # Select evenly distributed image IDs.
        indices = [
            round(i * (len(image_ids) - 1) / (count - 1))
            for i in range(count)
        ]

        sampled_ids = [image_ids[i] for i in indices]

        print(
            f"Scene {scene}: "
            f"{len(image_ids)} available, "
            f"{len(sampled_ids)} selected"
        )

        for image_id in sampled_ids:

            filename = f"{int(image_id):06d}.png"

            archive_path = (
                f"train_real\\{scene}\\rgb\\{filename}"
            )

            archive_paths.append(archive_path)

# Save paths for 7-Zip.
list_path = os.path.join(output_dir, "image_list.txt")

with open(list_path, "w", encoding="utf-8") as f:
    for path in archive_paths:
        f.write(path + "\n")

print("\nTOTAL SELECTED:", len(archive_paths))
print("LIST SAVED:", list_path)
