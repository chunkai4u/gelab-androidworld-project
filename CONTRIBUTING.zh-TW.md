# 團隊協作指南

[English](CONTRIBUTING.md) | **繁體中文** · [回到專案首頁](README.zh-TW.md)

1. 從 [Issues](https://github.com/chunkai4u/gelab-androidworld-project/issues) 挑選工作，先確認負責人。
2. 建立自己的分支，例如 `fix/emulator-stability` 或 `fix/text-input`。
3. 每個 pull request 集中處理一件事，說明改了什麼、驗證結果與仍存在的限制。
4. 只做程式審查、紀錄分析或文件整理的人，不需要在本機安裝 AndroidWorld。環境穩定前，先共用一台主要測試機。
5. 不要同時在同一台模擬器執行不同實驗，也不要在別人測試時修改環境設定。
6. 正式評估前，固定程式版本、模型、裝置設定、任務種子與步數上限。每次結果都要保留，包含失敗。

Wi-Fi 範例是先前一次開發測試的成功紀錄。目前候選的繪圖設定與文字輸入工具仍未驗證；報告與 pull request 都應清楚區分。

不要提交私鑰、帳號憑證、模型權重、虛擬環境、模擬器磁碟或影片。雲端連線使用各自獲授權的帳號與金鑰；影片另外保存，再把連結放進實驗紀錄。
