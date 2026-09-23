#!/usr/bin/env bash
set -euo pipefail
export HF_HUB_ENABLE_HF_TRANSFER=0
cd /workspace/gelab
python -m pip install 'transformers==4.57.6' accelerate pillow fastapi uvicorn huggingface_hub
hf download stepfun-ai/GELab-Zero-4B-preview --local-dir /workspace/gelab/model
nohup python /workspace/gelab/server.py > /workspace/gelab/server.log 2>&1 &
