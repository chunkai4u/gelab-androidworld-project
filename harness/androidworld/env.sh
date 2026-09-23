#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$PROJECT_DIR/../.." && pwd)"
export JAVA_HOME=/Library/Java/JavaVirtualMachines/openjdk-21.jdk/Contents/Home
export ANDROID_RUNTIME_DIR="${ANDROID_RUNTIME_DIR:-$TASK_DIR/work}"
export ANDROID_HOME="$ANDROID_RUNTIME_DIR/android-sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export ANDROID_USER_HOME="$ANDROID_RUNTIME_DIR/android-user"
export ANDROID_AVD_HOME="$ANDROID_RUNTIME_DIR/android-avd"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_RUNTIME_DIR/android-venv/bin:$PATH"
export PYTHONPATH="$ANDROID_RUNTIME_DIR/android_world:$TASK_DIR/model/runpod${PYTHONPATH:+:$PYTHONPATH}"
export GRPC_VERBOSITY=ERROR
unset GRPC_TRACE
export PYTHONUNBUFFERED=1
export SSL_CERT_FILE="$(python -m certifi)"
export REQUESTS_CA_BUNDLE="$SSL_CERT_FILE"
