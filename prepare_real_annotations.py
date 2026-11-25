
import os
import json

# Paths
annotations_root = r"C:\Users\omech\ycbv\real_annotations\train_real"
subset_root = r"C:\Users\omech\ycbv\real_subset"
image_list = os.path.join(subset_root, "image_list.txt")

# Scene-level split
train_scenes = [
    "000087", "000038", "000040",
    "000011", "000014", "000035"
]

val_scenes = [
    "000028", "000033", "000070",
    "000086", "000026", "000027"
]

# Read selected image paths and group image IDs by scene
selected = {}

with open(image_list, "r", encoding="utf-8") as f:
    for line in f:
        path = line.strip().replace("/", "\\")
        if not path:
            continue

        parts = path.split("\\")
        scene = parts[1]
        filename = parts[-1]

        image_id = int(os.path.splitext(filename)[0])

        selected.setdefault(scene, set()).add(image_id)

print("Scenes found:", len(selected))

# Annotation files to retain
annotation_files = [
    "scene_camera.json",
    "scene_gt.json",
    "scene_gt_info.json"
]

total_annotations = 0

for scene, selected_ids in selected.items():

    source_dir = os.path.join(annotations_root, scene)
    target_dir = os.path.join(
        subset_root, "train_real", scene
    )

    os.makedirs(target_dir, exist_ok=True)

    print(f"\nProcessing scene {scene}")
    print("Selected image IDs:", len(selected_ids))

    # Filter each annotation file
    for filename in annotation_files:

        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)

        with open(source_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        available_ids = {int(key) for key in data.keys()}
        missing_ids = selected_ids - available_ids

        if missing_ids:
            raise ValueError(
                f"{filename} in scene {scene} is missing "
                f"image IDs: {sorted(missing_ids)[:10]}"
            )

        filtered = {
            key: value
            for key, value in data.items()
            if int(key) in selected_ids
        }

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(filtered, f)

        print(f"  {filename}: {len(filtered)} entries")

    # Remove any extra PNGs from the earlier extraction test
    rgb_dir = os.path.join(target_dir, "rgb")

    image_files = [
        name for name in os.listdir(rgb_dir)
        if name.lower().endswith(".png")
    ]

    for filename in image_files:
        image_id = int(os.path.splitext(filename)[0])

        if image_id not in selected_ids:
            os.remove(os.path.join(rgb_dir, filename))

    remaining_images = [
        name for name in os.listdir(rgb_dir)
        if name.lower().endswith(".png")
    ]

    if len(remaining_images) != len(selected_ids):
        raise ValueError(
            f"Scene {scene}: expected {len(selected_ids)} images, "
            f"found {len(remaining_images)}"
        )

    total_annotations += len(selected_ids)

    print("  Verified RGB images:", len(remaining_images))

# Save the train/validation split information
split_info = {
    "train": {
        scene: sorted(selected[scene])
        for scene in train_scenes
    },
    "val": {
        scene: sorted(selected[scene])
        for scene in val_scenes
    }
}

split_path = os.path.join(subset_root, "splits.json")

with open(split_path, "w", encoding="utf-8") as f:
    json.dump(split_info, f, indent=2)

print("\nFINAL SUMMARY")
print("Training scenes:", len(train_scenes))
print("Validation scenes:", len(val_scenes))
print("Total images:", total_annotations)
print("Split file:", split_path)
print("Annotation filtering completed.")
