import zipfile
import os
import re
import json
from collections import Counter
import random

archive_path = r"C:\Users\Omech\ycbv\ycbv_train_pbr.zip"

random.seed(42)

training_scenes = ["000000", "000001", "000002"]
validation_scenes = ["000003"]

selected_images = {}

with zipfile.ZipFile(archive_path, "r") as archive:

    for scene_id in training_scenes + validation_scenes:

        gt_path = f"train_pbr/{scene_id}/scene_gt.json"

        with archive.open(gt_path) as file:
            ground_truth = json.load(file)

        # Randomly select 100 images from this scene
        image_ids = sorted(ground_truth.keys())

        sampled_ids = random.sample(image_ids, 100)

        selected_images[scene_id] = sampled_ids

        counts = Counter()

        for image_id in sampled_ids:

            for annotation in ground_truth[image_id]:
                counts[annotation["obj_id"]] += 1

        split = (
            "TRAINING"
            if scene_id in training_scenes
            else "VALIDATION"
        )

        print(f"\nScene {scene_id} ({split})")
        print("Selected images:", len(sampled_ids))
        print("Object instances:", sum(counts.values()))
        print("Categories represented:", len(counts))

        missing = [
            obj_id
            for obj_id in range(1, 22)
            if counts[obj_id] == 0
        ]

        print("Missing categories:", missing)

        print("Instances per category:")

        for obj_id in range(1, 22):
            print(f"  Object {obj_id}: {counts[obj_id]}")