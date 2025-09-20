from ultralytics import YOLO
import ultralytics
from datetime import datetime
import wandb
import os
import yaml
import re
import gc

cfg = ultralytics.cfg.get_cfg(cfg='config.yaml')
run_name = cfg.name
project_name = cfg.project

run_dir = os.path.join(project_name, run_name)
os.makedirs(run_dir, exist_ok=True)

os.environ["WANDB_MODE"] = "online"
wandb_cfg = ultralytics.cfg.cfg2dict(cfg)
run = wandb.init(project=project_name, config=wandb_cfg, name=run_name)
artifact = wandb.Artifact(name="2025_tiling", type="dataset")
artifact.add_dir(run_dir)
wandb.log_artifact(artifact)

with open('temp_config.yaml', 'w') as f:
    yaml.dump(vars(cfg), f, allow_unicode=True)

model = YOLO(cfg.model)
results = model.train(cfg='temp_config.yaml')
wandb.log(results.metrics)
wandb.finish()

