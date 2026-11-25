
import zipfile
import json
import os
import random
import shutil


archive_path =  r"C:\Users\Omech\ycbv\ycbv_train_pbr.zip"

output_dir = r"C:\Users\omech\ycbv_pbr_subset"
output_zip = r"C:\Users\omech\ycbv_pbr_subset.zip"

# Dataset Split

training_scenes = ["000000", "000001", "000002"]
validation_scenes = ["000003"]

all_scenes = training_scenes + validation_scenes

images_per_scene = 100

random.seed(42)

# Prepare output directory

os.makedirs(output_dir, exist_ok=True)

# Extract selected images and annotations

manifest = {
    "training_scenes": training_scenes,
    "validation_scenes": validation_scenes,
    "images_per_scene": images_per_scene,
    "random_seed": 42
}

with zipfile.ZipFile(archive_path, "r") as archive:

    for scene_id in all_scenes:

        print(f"\nProcessing scene {scene_id}...")

        source_prefix = f"train_pbr/{scene_id}/"
        destination_scene = os.path.join(
            output_dir, "train_pbr", scene_id
        )

        destination_rgb = os.path.join(
            destination_scene, "rgb"
        )

        os.makedirs(destination_rgb, exist_ok=True)

        # Read annotation files directly from original ZIP
        annotations = {}

        for filename in [
            "scene_gt.json",
            "scene_gt_info.json",
            "scene_camera.json"
        ]:

            source_path = source_prefix + filename

            with archive.open(source_path) as file:
                annotations[filename] = json.load(file)

        ground_truth = annotations["scene_gt.json"]
        ground_truth_info = annotations["scene_gt_info.json"]
        camera_info = annotations["scene_camera.json"]

        # Select 100 images randomly from this scene
        image_ids = sorted(ground_truth.keys())

        selected_ids = sorted(
            random.sample(image_ids, images_per_scene)
        )

        # Keep only the selected image annotations
        selected_gt = {
            image_id: ground_truth[image_id]
            for image_id in selected_ids
        }

        selected_info = {
            image_id: ground_truth_info[image_id]
            for image_id in selected_ids
        }

        selected_camera = {
            image_id: camera_info[image_id]
            for image_id in selected_ids
        }

        # Save reduced annotation files
        reduced_annotations = {
            "scene_gt.json": selected_gt,
            "scene_gt_info.json": selected_info,
            "scene_camera.json": selected_camera
        }

        for filename, data in reduced_annotations.items():

            destination = os.path.join(
                destination_scene, filename
            )

            with open(destination, "w") as file:
                json.dump(data, file)

        # Extract only selected RGB images
        for image_id in selected_ids:

            image_filename = f"{int(image_id):06d}.jpg"

            source_image = (
                source_prefix + "rgb/" + image_filename
            )

            destination_image = os.path.join(
                destination_rgb, image_filename
            )

            with archive.open(source_image) as source:
                with open(destination_image, "wb") as target:
                    shutil.copyfileobj(source, target)

        print("Selected images:", len(selected_ids))
        print("Annotations saved.")

        manifest[scene_id] = selected_ids

# Save dataset manifest

manifest_path = os.path.join(output_dir, "manifest.json")

with open(manifest_path, "w") as file:
    json.dump(manifest, file, indent=2)

print("\nAll selected scenes extracted.")

# Create a smaller ZIP for Colab

print("\nCreating subset ZIP...")

with zipfile.ZipFile(
    output_zip, "w", compression=zipfile.ZIP_STORED
) as output_archive:

    for root, directories, files in os.walk(output_dir):

        for filename in files:

            full_path = os.path.join(root, filename)

            relative_path = os.path.relpath(
                full_path, os.path.dirname(output_dir)
            )

            output_archive.write(full_path, relative_path)

print("\nFinished!")
print("Output folder:", output_dir)
print("Output ZIP:", output_zip)

size_mb = os.path.getsize(output_zip) / (1024 ** 2)

print(f"ZIP size: {size_mb:.2f} MB")
