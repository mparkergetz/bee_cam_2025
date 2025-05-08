#!/bin/bash

SCORES_CSV="train_scores.csv"
IMAGE_DIR="./train/background"
OUTPUT_DIR="./hard_negs/train"

mkdir -p "$OUTPUT_DIR"

awk -F',' 'NR > 1 && $2 > 0.1 { print $1 }' "$SCORES_CSV" | while read -r filename; do
    src="$IMAGE_DIR/$filename"
    if [ -f "$src" ]; then
        cp -n "$src" "$OUTPUT_DIR/"
    fi
done

echo "Done: copied hard negatives to $OUTPUT_DIR"
