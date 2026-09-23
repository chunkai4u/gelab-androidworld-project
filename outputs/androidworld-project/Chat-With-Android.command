#!/bin/bash
# Opens an interactive terminal chat that delegates supported requests to GELab-Zero.
set -e
cd "$(dirname "$0")"
source ./env.sh
exec python ./chat_with_android.py
