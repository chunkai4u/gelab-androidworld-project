# 課堂展示與驗證指南

本專案目前可以現場展示的成果是 **GELab-Zero-4B-preview 在 Runpod L4 上決策，控制 AndroidWorld 模擬器完成 `SystemWifiTurnOn`，並由 AndroidWorld 官方 verifier 判定 PASS**。

最新成功證據在 [`examples/live-wifi-pass/`](examples/live-wifi-pass/)：5 個 agent steps、71.16 秒、`score: 1.0`、`verifier: PASS`，以及對應的錄影、最後畫面與 trajectory。這是開發測試，不是作業所需的九次正式評估。

## 展示前（提早 10 分鐘）

1. 在 Runpod Console 確認 Pod 狀態是 **Running**。不要在展示期間停止 Pod。
2. 在 Mac 的 Finder 打開 `androidworld-project` 資料夾，準備好 `Show-Live-WiFi.command`。
3. 打開一個 Terminal 視窗，並讓 Android emulator 視窗可見。終端機和 emulator 並排，觀眾可同時看到日誌與手機畫面。
4. 不要預先開 Settings，也不要在 agent 執行時手動點模擬器。

## 現場流程（約 3 分鐘）

1. 說："We use GELab-Zero as the policy model and AndroidWorld as the task environment and verifier. The GPU does inference; AndroidWorld decides whether the task actually succeeded."
2. 雙擊 `Show-Live-WiFi.command`。它會在每次開始前把 Wi-Fi 重設為關閉，然後啟動一次 15-step 上限的測試與螢幕錄影。
3. 讓大家看 emulator：agent 會開啟 Settings、進入網路設定，並打開 Wi-Fi。Terminal 會逐步印出 `STEP` 與模型回傳的動作。
4. 等最後出現 `RESULT: PASS`。這通常約 70 秒；第一次啟動模擬器時可多等 1–2 分鐘。
5. 說："`COMPLETE` only means the agent believes it is finished. `PASS` and score `1.0` come from AndroidWorld's official task verifier, so this is the value we report."
6. 開啟剛生成的 `runs/<timestamp>-SystemWifiTurnOn-1/result.json`，展示 `verifier: PASS`、`score: 1.0`、`steps` 和 `seconds`。接著開啟同資料夾的 `recording.mp4`。

## 老師若要看 code

請依這個順序，不需要從頭讀完整個 repository：

1. [`outputs/gelab-runpod/server.py`](outputs/gelab-runpod/server.py)：在 Runpod GPU 載入 GELab-Zero 模型、提供每一步推論服務。
2. [`outputs/gelab-runpod/client.py`](outputs/gelab-runpod/client.py)：透過私有 SSH gateway 把截圖送到模型；repo 裡只有 placeholder，沒有金鑰。
3. [`outputs/androidworld-project/gelab_agent.py`](outputs/androidworld-project/gelab_agent.py)：把模型的 `CLICK`、`AWAKE`、`COMPLETE` 回應轉成 AndroidWorld 動作，並限制可用 app 和步數。
4. [`outputs/androidworld-project/run_task.py`](outputs/androidworld-project/run_task.py)：建立 AndroidWorld task、執行 agent、錄影、呼叫 `task.is_successful(env)`，把官方分數寫入 `result.json`。
5. [`outputs/androidworld-project/recorder.py`](outputs/androidworld-project/recorder.py)：擷取每次測試的 emulator 影片。

可用一句話說明架構：

> Android screenshot → private model request → GELab-Zero on Runpod L4 → next UI action → AndroidWorld → official verifier.

## 如何解釋 verify

`trajectory.jsonl` 是每一步的模型輸出與實際動作，`recording.mp4` 是可視證據；但兩者都不是成績判定。程式最後呼叫 AndroidWorld 的 `task.is_successful(env)`：只有它回傳 1.0 時，runner 才寫入 `verifier: "PASS"`。因此我們會同時保留影片、trajectory、final screenshot 和 `result.json`，讓結果可重看與可追查。

## 誠實說明目前範圍

- 已經 live verified：`SystemWifiTurnOn`，有兩次開發期 PASS，其中最新一次有完整錄影與可公開檢查的 artifacts。
- 尚未完成：`MarkorCreateNote`、`MarkorCreateNoteAndSms` 和每個 task 3 次的正式評估（共 9 次）。
- 所以展示時請說這是 **working prototype / live proof of the pipeline**，不要說整個 AndroidWorld benchmark 或三個作業 task 都已完成。

## 若現場出狀況

1. 不要在壓力下改 code。先確認 Runpod Pod 仍是 Running，然後重跑一次 `Show-Live-WiFi.command`。
2. 若模擬器首次開機太慢，直接開啟 [`examples/live-wifi-pass/recording.mp4`](examples/live-wifi-pass/recording.mp4)，並對照 [`result.json`](examples/live-wifi-pass/result.json) 與 [`trajectory.jsonl`](examples/live-wifi-pass/trajectory.jsonl)。清楚說明這是先前的成功錄影，不是假裝成現場結果。
3. 錄影後仍以 `result.json` 的 official verifier 為準，不只看畫面上的 Wi-Fi toggle。
