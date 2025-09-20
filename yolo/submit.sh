#!/bin/bash
#. /nfs/stak/users/getzm/miniconda3/etc/profile.d/conda.sh
#conda activate yolo11

BATCH_SIZE=128
export BATCH_SIZE

LOG_DIR="logs"

mkdir -p "${LOG_DIR}"

RUN_NUMBER=$(ls "${LOG_DIR}" | grep -Eo 'run[0-9]+' | grep -Eo '[0-9]+' | sort -n | tail -1)

if [ -z "${RUN_NUMBER}" ]; then
	    RUN_NUMBER=1
    else
	        RUN_NUMBER=$((RUN_NUMBER + 1))
fi

RUN_DIR="${LOG_DIR}/run${RUN_NUMBER}"
mkdir -p "${RUN_DIR}"
export RUN_DIR

NUM_GPUS=4
export NUM_GPUS

cd /home/bpp/getzm/yolo11
export WANDB_API_KEY='##################'
export RUN_DIR
#export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
echo 'copying'
cp -v default.yaml dataset.yaml submit.sh train.py "${RUN_DIR}/"

echo 'execute python distr run'
python -m torch.distributed.run --nproc_per_node=${NUM_GPUS} --master_port=50000 train.py --cfg default.yaml 2>> "${RUN_DIR}/error.log"


