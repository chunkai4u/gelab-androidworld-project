# GELab-Zero × AndroidWorld 課程專案

[English](README.md) | **繁體中文**

**目前狀態：2026-09-23 已暫停實驗。這個專案仍在原型開發階段，尚未完成正式評估。**

[📋 中文待辦](ISSUES.zh-TW.md) · [🤝 中文協作指南](CONTRIBUTING.zh-TW.md) · [GitHub Issues](https://github.com/chunkai4u/gelab-androidworld-project/issues)

## 已經有的功能

- 在 Runpod 上執行 GELab-Zero-4B-preview，包含部署、重建服務與 SSH 連線程式。
- AndroidWorld agent 轉接程式、任務執行器、步數上限、限定 App 清單、截圖與動作紀錄、官方成功判定，以及模擬器錄影。
- 三個任務的啟動入口：`SystemWifiTurnOn`、`MarkorCreateNote`、`MarkorCreateNoteAndSms`。
- 一次已驗證的 Wi-Fi 開發測試：**6 步完成，官方分數 1.0／PASS，影片約 71 秒**。精簡紀錄在 [examples/wifi-pass](examples/wifi-pass)，影片另外保存。

## 還沒完成的部分

Intel Mac 上的模擬器反覆出現 Settings／System UI 無回應。Markor 筆記任務尚未通過完整流程，筆記加 SMS 的跨 App 任務也尚未測試。最新的軟體繪圖設定與官方 YADB 文字輸入工具仍待驗證。

**每個任務各測三次，共九次的正式評估還沒開始。**

Wi-Fi 成功範例使用較早的環境設定，不能用它來宣稱目前所有程式與設定都已驗證，也不能把開發測試當成正式成功率。

## 資料夾內容

| 路徑 | 用途 |
|---|---|
| `outputs/gelab-runpod/` | 雲端模型服務、私人連線程式與重建腳本 |
| `outputs/androidworld-project/` | Mac 啟動器、agent、錄影、初始狀態備份及環境說明 |
| `examples/wifi-pass/` | 已移除私人路徑的開發測試紀錄，影片另外保存 |
| [ISSUES.zh-TW.md](ISSUES.zh-TW.md) | 下一步待辦與建議分工 |

目前保留 `outputs/` 資料夾結構，因為啟動器會依此找到本機的 `work/` 目錄。調整資料夾位置時，也需要修改程式裡的路徑。

## 組員怎麼配合

**不用每個人都安裝 AndroidWorld。** 所有人都可以先下載程式、閱讀紀錄與文件。初期由一位組員操作主要測試機，環境穩定後再準備一台備援機。其他人可以負責 agent、模型服務、失敗分析或簡報。

每個待辦使用自己的分支，透過 pull request 審查修改。每次要納入報告的實驗，都記錄程式版本、模型、任務種子與環境設定。詳細流程請看 [中文協作指南](CONTRIBUTING.zh-TW.md)。

只有實際操作實驗的人需要完整模擬器與 AndroidWorld。這份程式目前不是跨電腦的一鍵安裝包：啟動器以 Intel Mac 為目標，預期未納入 Git 的 `work/` 目錄裡已有依賴、App 初始狀態、SDK／AVD 及 Python 環境。重建環境前，請先閱讀各元件的 README。

YADB 工具來自 GELab-Zero 官方程式，版本為 `7b619f6f67d2b1101021fc453cb27bd48a29e4f2`，預期放在 `work/gelab-zero-source`。AndroidWorld 固定在 `e3fea3ccc69787570e282c99573298f1c3019a34`。依賴鎖定檔記錄的是參考 Mac 的套件，並非所有平台通用的安裝包。

## 存取權限與大型檔案

這裡不含 SSH 私鑰、帳號憑證、模型權重、模擬器映像檔或虛擬環境。Runpod 連線資料已改成待填入的範例值。需要連線雲端的組員，應使用自己的授權 SSH 金鑰與主機設定，不要共用主要測試機的私鑰。

影片放在共用儲存空間，再把連結加入實驗紀錄；不要把大型影片提交到 Git。

這是私人的團隊 repository。目前尚未邀請協作者；工作進度集中在 [GitHub Issues](https://github.com/chunkai4u/gelab-androidworld-project/issues)。
