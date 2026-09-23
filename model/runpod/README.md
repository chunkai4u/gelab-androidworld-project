# GELab-Zero on Runpod — verified deployment

## Status

On 2026-09-23, deployed and tested Pod `gelab-zero-course` (`YOUR_POD_ID`) with one NVIDIA L4 24 GB, 30 GB temporary container disk, and no persistent volume. GPU rate was $0.49/hour plus approximately $0.004/hour disk. The Pod has been restarted and is being left running with user authorization (about $12 per day at this rate). If stopped, restarting depends on availability and its temporary filesystem must be rebuilt. No persistent volume was configured.

The official GELab-Zero-4B-preview model loaded on CUDA using Transformers 4.57.6 and the Runpod PyTorch 2.8.0 template. Ollama installation succeeded but model import failed with `unsupported MLX architecture: Qwen3VLForConditionalGeneration`, so the tested deployment uses Transformers instead.

## Verified

- CUDA model load and private health endpoint.
- Synthetic Wi-Fi screen test: `action:CLICK point:840,182` (normalized 0–1000 coordinates). This maps inside the depicted Wi-Fi switch.
- Local Mac → authenticated Runpod SSH gateway → model request → response.
- Initial inference 1.82 seconds; warm inference 0.77 seconds. These times exclude network/SSH overhead.
- The synthetic test is not an AndroidWorld benchmark result. AndroidWorld and the emulator are now installed; integration status and actual run artifacts are in the `harness/androidworld/` folder.

## Files

- `server.py`: private model service, listens only on 127.0.0.1:11435.
- `prompt.txt`: action-space prompt from the upstream GELab-Zero parser.
- `client.py`: local health and image requests over SSH, without a public model API.
- `setup.sh`: model installation and service start on the remote Pod.
- `bootstrap.py`: transfers service files over SSH and starts setup after a restart.
- `smoke_test.py`: synthetic screen test on the remote machine.
- `verification.json`: actual response from the local-to-cloud test.

## Restart

1. Start the Pod in Runpod, checking current rates and the agreed budget first.
2. If the SSH connection string changes, set `GELAB_SSH_HOST` to the new gateway user/host shown by Runpod.
3. Run `python3 bootstrap.py` from this folder. It starts remote installation in the background; logs are in `/workspace/gelab/setup.log`.
4. After setup, run `python3 client.py` to verify health.
5. Call `python3 client.py --image /absolute/path/screenshot.png --task 'Turn Wi-Fi on.'`.
6. Stop the Pod when finished. Without a persistent volume, remote files are lost; the local files here allow rebuilding.

SSH private key is intentionally excluded from this deliverable. On this Mac it is stored in the task's `work/runpod/gelab_ed25519`, with restricted file permissions. `client.py` uses it by default. Other members should use their own authorized keys via `GELAB_SSH_KEY` and their own known-host configuration; never commit or share private keys. The SSH gateway transport works, but direct TCP SSH timed out on this network. The current client opens a separate SSH session per request; later integration can optimize connection reuse.

The model service produces an action string. The `harness/androidworld/` folder implements the adapter, app allowlist, step budgets, recording, and official task verifier integration. See its README for limits and environment modifications.

## Sources

- https://github.com/stepfun-ai/gelab-zero
- https://huggingface.co/stepfun-ai/GELab-Zero-4B-preview
- https://console.runpod.io/pods?id=YOUR_POD_ID
