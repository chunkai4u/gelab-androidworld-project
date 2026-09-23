# GELab-Zero × AndroidWorld 課程專案

[English](README.md) | **繁體中文**

**目前狀態：2026-09-23 已完成一次可現場展示的 Wi-Fi 開發測試。這個專案仍在原型開發階段，尚未完成正式評估。**

[📋 中文待辦](docs/ISSUES.zh-TW.md) · [🤝 中文協作指南](docs/CONTRIBUTING.zh-TW.md) · [GitHub Issues](https://github.com/chunkai4u/gelab-androidworld-project/issues)

## 已經有的功能

- 在 Runpod 上執行 GELab-Zero-4B-preview，包含部署、重建服務與 SSH 連線程式。
- AndroidWorld agent 轉接程式、任務執行器、步數上限、限定 App 清單、截圖與動作紀錄、官方成功判定，以及模擬器錄影。
- 三個任務的啟動入口：`SystemWifiTurnOn`、`MarkorCreateNote`、`MarkorCreateNoteAndSms`。
- 一次可現場重現的 Wi-Fi 開發測試：**5 個動作，官方分數 1.0／PASS，71.16 秒影片**。影片、最終畫面、trajectory 和結果在 [results/development/live-wifi-pass](results/development/live-wifi-pass)。
- [展示與驗證指南](docs/LIVE_DEMO.zh-TW.md)，包含現場講稿、code 導覽與備案。

## 還沒完成的部分

Intel Mac 上的模擬器曾出現 Settings／System UI 無回應。Markor 筆記任務尚未通過完整流程，筆記加 SMS 的跨 App 任務也尚未測試。官方 YADB 文字輸入工具仍待完成端到端驗證。

**每個任務各測三次，共九次的正式評估還沒開始。**

Wi-Fi 成功範例只驗證 `result.json` 所記錄的參考環境，不能把開發測試當成正式成功率。

## 資料夾內容

| 路徑 | 用途 |
|---|---|
| `model/runpod/` | 模型（課程第一天）：雲端模型服務、私人連線程式與重建腳本 |
| `harness/androidworld/` | Harness（課程第二、三天）：Mac 啟動器、agent、錄影、初始狀態備份及環境說明 |
| `results/` | 評估（課程第四天）：`runs.csv` 每次測試一列；`development/` 放開發測試，`formal/` 放九次正式評估 |
| `presentation/` | 簡報（課程第五天） |
| `docs/` | 待辦、協作指南與展示指南（含中文版） |

資料夾依課程的一週安排。課程概念與程式位置的完整對照，請看英文 [README](README.md) 的 "Where each harness part lives"。

`harness/androidworld/` 與 `model/runpod/` 都位於第二層，因為程式依此找到 repository 根目錄的 `work/`。移動資料夾時請保持這個深度。

## 組員怎麼配合

**不用每個人都安裝 AndroidWorld。** 所有人都可以先下載程式、閱讀紀錄與文件。初期由一位組員操作主要測試機，環境穩定後再準備一台備援機。其他人可以負責 agent、模型服務、失敗分析或簡報。

每個待辦使用自己的分支，透過 pull request 審查修改。每次要納入報告的實驗，都記錄程式版本、模型、任務種子與環境設定。詳細流程請看 [中文協作指南](docs/CONTRIBUTING.zh-TW.md)。

只有實際操作實驗的人需要完整模擬器與 AndroidWorld。這份程式目前不是跨電腦的一鍵安裝包：啟動器以 Intel Mac 為目標，預期未納入 Git 的 `work/` 目錄裡已有依賴、App 初始狀態、SDK／AVD 及 Python 環境。重建環境前，請先閱讀各元件的 README。

YADB 工具來自 GELab-Zero 官方程式，版本為 `7b619f6f67d2b1101021fc453cb27bd48a29e4f2`，預期放在 `work/gelab-zero-source`。AndroidWorld 固定在 `e3fea3ccc69787570e282c99573298f1c3019a34`。依賴鎖定檔記錄的是參考 Mac 的套件，並非所有平台通用的安裝包。

## 存取權限與大型檔案

這裡不含 SSH 私鑰、帳號憑證、模型權重、模擬器映像檔或虛擬環境。Runpod 連線資料已改成待填入的範例值。需要連線雲端的組員，應使用自己的授權 SSH 金鑰與主機設定，不要共用主要測試機的私鑰。

最新 Wi-Fi 影片很小（約 0.6 MB），所以和對應 verifier evidence 一起提交；大型影片仍應放在共用儲存空間。

這是私人的團隊 repository。工作進度集中在 [GitHub Issues](https://github.com/chunkai4u/gelab-androidworld-project/issues)。
