import os
import re

# Set directory with .jpg and .txt pairs
base_dir = 'yolo/datasets/val_tps'

# Extract base group by removing final _digit before .jpg/.txt
def extract_tile_group(filename):
    return re.sub(r'_\d+\.(jpg|txt)$', '', filename)

# Parse .txt file and return the largest bbox area (YOLO format)
def max_bbox_area(txt_path):
    max_area = 0
    with open(txt_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            _, _, _, w, h = map(float, parts)
            area = w * h
            if area > max_area:
                max_area = area
    return max_area

# Collect all .txt files and group by tile group
tile_groups = {}
for fname in os.listdir(base_dir):
    if not fname.endswith('.txt'):
        continue
    group = extract_tile_group(fname)
    tile_groups.setdefault(group, []).append(fname)

deleted_count = 0

for group, txt_files in tile_groups.items():
    best_file = None
    best_area = -1
    for txt in txt_files:
        txt_path = os.path.join(base_dir, txt)
        area = max_bbox_area(txt_path)
        if area > best_area:
            best_area = area
            best_file = txt

    # Keep best_file, delete others in the group
    for txt in txt_files:
        if txt == best_file:
            continue
        # Delete both .txt and .jpg
        jpg = txt.replace('.txt', '.jpg')
        txt_path = os.path.join(base_dir, txt)
        jpg_path = os.path.join(base_dir, jpg)
        if os.path.exists(txt_path):
            os.remove(txt_path)
        if os.path.exists(jpg_path):
            os.remove(jpg_path)
        deleted_count += 1

print(f"✅ Cleaned: Deleted {deleted_count} image+label pairs with smaller bboxes.")