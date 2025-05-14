from ultralytics import YOLO
import pandas as pd
from pathlib import Path
import os
import torch
import gc

torch.cuda.empty_cache()
torch.cuda.ipc_collect()


data_path = '/home/mpgetz/nas/bee_cam_slicing/tiled_prune_bg_050725'

model_path = 'slicing_model_022325/weights/best.pt'  # GET SLICING MODEL
input_dirs = [os.path.join(data_path,'train/background'), os.path.join(data_path, 'val/background')]
output_files = ['train_scores.csv', 'val_scores.csv']

model = YOLO(model_path)

for input_dir, output_csv in zip(input_dirs, output_files):
    image_dir = Path(input_dir)
    results_data = []

    for img_path in image_dir.glob('*.[jp][pn]g'):
        results = model(img_path, conf=0.1)
        
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf.cpu().item())
                    results_data.append({
                        'file': img_path.name,
                        'conf': conf
                    })
        del results
        torch.cuda.empty_cache()
        gc.collect()

    df = pd.DataFrame(results_data)
    df.to_csv(output_csv, index=False)
    print(f"Done: {input_dir} → {output_csv}")