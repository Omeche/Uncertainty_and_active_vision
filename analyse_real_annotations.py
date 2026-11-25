
import os
import json
from collections import defaultdict

root = r"C:\Users\omech\ycbv\real_annotations\train_real"

object_names = {
    1: "Master Chef Can",
    2: "Cracker Box",
    3: "Sugar Box",
    4: "Tomato Soup Can",
    5: "Mustard Bottle",
    6: "Tuna Fish Can",
    7: "Pudding Box",
    8: "Gelatin Box",
    9: "Potted Meat Can",
    10: "Banana",
    11: "Pitcher Base",
    12: "Bleach Cleanser",
    13: "Bowl",
    14: "Mug",
    15: "Power Drill",
    16: "Wood Block",
    17: "Scissors",
    18: "Large Marker",
    19: "Large Clamp",
    20: "Extra Large Clamp",
    21: "Foam Brick"
}

scene_summary = []
global_counts = defaultdict(int)
global_usable = defaultdict(int)

scene_dirs = sorted(
    d for d in os.listdir(root)
    if os.path.isdir(os.path.join(root, d))
)

print("Number of extracted scenes:", len(scene_dirs))

for scene in scene_dirs:

    scene_path = os.path.join(root, scene)

    gt_path = os.path.join(scene_path, "scene_gt.json")
    info_path = os.path.join(scene_path, "scene_gt_info.json")
    camera_path = os.path.join(scene_path, "scene_camera.json")

    if not all(os.path.exists(p) for p in [
        gt_path, info_path, camera_path
    ]):
        print("Incomplete scene:", scene)
        continue

    with open(gt_path, "r") as f:
        gt = json.load(f)

    with open(info_path, "r") as f:
        info = json.load(f)

    with open(camera_path, "r") as f:
        camera = json.load(f)

    scene_counts = defaultdict(int)
    scene_usable = defaultdict(int)

    for image_id, objects in gt.items():

        object_info = info.get(image_id, [])

        for obj, obj_info in zip(objects, object_info):

            obj_id = int(obj["obj_id"])
            visibility = float(obj_info["visib_fract"])

            scene_counts[obj_id] += 1
            global_counts[obj_id] += 1

            if visibility >= 0.20:
                scene_usable[obj_id] += 1
                global_usable[obj_id] += 1

    scene_summary.append({
        "scene": scene,
        "images": len(camera),
        "instances": sum(scene_counts.values()),
        "categories": len(scene_counts),
        "usable": sum(scene_usable.values())
    })

print("\nSCENE SUMMARY")
print("\n")

for s in scene_summary:
    print(
        f"Scene {s['scene']} | "
        f"Images: {s['images']:4d} | "
        f"Instances: {s['instances']:5d} | "
        f"Categories: {s['categories']:2d} | "
        f"Usable (visibility >= 0.20): {s['usable']:5d}"
    )

print("\nOBJECT COVERAGE ACROSS ALL EXTRACTED SCENES")
print("\n")

for obj_id in sorted(object_names):
    print(
        f"{obj_id:2d}. {object_names[obj_id]:22s} | "
        f"All instances: {global_counts[obj_id]:6d} | "
        f"Usable: {global_usable[obj_id]:6d}"
    )

print("\nTOTAL SCENES:", len(scene_summary))
print("TOTAL IMAGES:", sum(s["images"] for s in scene_summary))
print("TOTAL INSTANCES:", sum(s["instances"] for s in scene_summary))
