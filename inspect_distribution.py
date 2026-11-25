
import os
import json
import pandas as pd

annotation_root = r"C:\Users\omech\ycbv\real_annotations"

target_ids = [20, 21]

scene_records = []

for scene_id in sorted(os.listdir(annotation_root)):

    scene_path = os.path.join(annotation_root, scene_id)

    gt_path = os.path.join(scene_path, "scene_gt.json")

    if not os.path.isfile(gt_path):
        continue

    with open(gt_path, "r") as f:
        annotations = json.load(f)

    clamp_count = 0
    foam_count = 0

    for image_annotations in annotations.values():

        for obj in image_annotations:

            object_id = obj["obj_id"]

            if object_id == 20:
                clamp_count += 1

            elif object_id == 21:
                foam_count += 1

    if clamp_count > 0 or foam_count > 0:

        scene_records.append({
            "Scene": scene_id,
            "Extra Large Clamp": clamp_count,
            "Foam Brick": foam_count,
            "Both present": (
                clamp_count > 0 and foam_count > 0
            )
        })

scene_df = pd.DataFrame(scene_records)

print("Scenes containing either target object:",
      len(scene_df))

print("\nScenes containing both objects:",
      scene_df["Both present"].sum())

#display(scene_df)
