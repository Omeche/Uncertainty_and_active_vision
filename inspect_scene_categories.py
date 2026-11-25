
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

scene_dirs = sorted(
    d for d in os.listdir(root)
    if os.path.isdir(os.path.join(root, d))
)

scene_data = {}

for scene in scene_dirs:

    path = os.path.join(root, scene)

    with open(os.path.join(path, "scene_gt.json")) as f:
        gt = json.load(f)

    with open(os.path.join(path, "scene_gt_info.json")) as f:
        info = json.load(f)

    counts = defaultdict(int)
    usable = defaultdict(int)

    for image_id, objects in gt.items():

        object_info = info[image_id]

        for obj, obj_info in zip(objects, object_info):

            obj_id = int(obj["obj_id"])
            counts[obj_id] += 1

            if float(obj_info["visib_fract"]) >= 0.20:
                usable[obj_id] += 1

    scene_data[scene] = {
        "counts": counts,
        "usable": usable
    }

print("SCENE CATEGORY COVERAGE")
print("\n")

for scene, data in scene_data.items():

    categories = sorted(data["counts"])

    names = [
        f"{obj_id}:{object_names[obj_id]}"
        for obj_id in categories
    ]

    print(f"\nScene {scene} ({len(categories)} categories)")
    print(", ".join(names))

print("\n\nDIFFICULT CATEGORY COVERAGE")
print("\n")

for obj_id in [17, 18, 19, 20, 21]:

    print(f"\n{obj_id}: {object_names[obj_id]}")

    for scene, data in scene_data.items():

        count = data["usable"].get(obj_id, 0)

        if count > 0:
            print(f"  Scene {scene}: {count} usable instances")
