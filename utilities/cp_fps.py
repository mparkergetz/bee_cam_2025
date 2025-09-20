import os
import shutil

# Paths
train_dir = "yolo/datasets/background"
val_dir = "yolo/datasets/tiled_bombusvaledit_061725/val"
output_dir = "yolo/datasets/preprunebacks_fps"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to read filenames from a text file
def read_filenames(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# # Combine all filenames from both text files
# fps_files = read_filenames("bombusvaledit_fps.txt")
# train_fps_files = read_filenames("bombusvaledit_train_fps.txt")
all_files = read_filenames("preprunebackgrounds_train_fps.txt")
all_files = set(all_files)  # use set to avoid duplicates


for filename in all_files:
    for src_dir in [train_dir, val_dir]:
        src_path = os.path.join(src_dir, filename)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(output_dir, filename))
            break  # once found and copied, no need to check other dir
        else:
            continue

print(f"Copied {len(all_files)} files to {output_dir}")
