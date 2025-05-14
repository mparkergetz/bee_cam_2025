#!/bin/bash
csv_file="csv_output/val_scores.csv"
source_dir="/home/mpgetz/nas/bee_cam_slicing/tiled_prune_bg_050725/val/background"
output_dir="./hard_negs"

mkdir -p "$output_dir"

declare -A seen

tail -n +2 "$csv_file" | cut -d',' -f1 | while IFS= read -r file; do
    file=$(echo "$file" | xargs)  # Trim spaces
    
    if [[ -n "${seen[$file]}" ]]; then
        echo "Duplicate entry skipped: $file"
        continue
    fi
    seen[$file]=1
    
    src="$source_dir/$file"
    dst="$output_dir/$file"
    
    if [ -f "$src" ]; then
        cp -n "$src" "$dst"
        echo "Copied: $file"
    else
        echo "File not found: $file"
    fi
done
