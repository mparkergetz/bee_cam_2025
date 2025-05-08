from ultralytics import YOLO
import pandas as pd
from pathlib import Path

model_path = ''  # GET SLICING MODEL
input_dirs = ['train/background', 'val/background']
output_files = ['train_scores.csv', 'val_scores.csv']


model = YOLO(model_path)

for input_dir, output_csv in zip(input_dirs, output_files):
    image_dir = Path(input_dir)
    results_data = []

    for img_path in image_dir.glob('*.[jp][pn]g'):
        results = model(img_path)
        for r in results:
            for box in r.boxes:
                conf = float(box.conf.item())
                results_data.append({
                    'file': img_path.name,
                    'conf': conf
                })

    df = pd.DataFrame(results_data)
    df.to_csv(output_csv, index=False)
    print(f"Done: {input_dir} → {output_csv}")