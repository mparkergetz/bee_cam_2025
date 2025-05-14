#!/bin/bash

cut -d',' -f1 train_scores.csv | tail -n +2 | sort > files1.txt
cut -d',' -f1 val_scores.csv | tail -n +2 | sort > files2.txt

comm -12 files1.txt files2.txt > common_filenames.txt

echo "Common filenames:"
cat common_filenames.txt
