# 接手待辦

[English](ISSUES.md) | **繁體中文** · [回到專案首頁](README.zh-TW.md)

1. **[P0：讓模擬器穩定](https://github.com/chunkai4u/gelab-androidworld-project/issues/1)｜環境負責人**  
   排查 Settings／System UI 反覆無回應的問題。準備好的 3 GB 記憶體、SwiftShader 與原生 540×1200 設定尚未完成開機測試。先確認 App 能正常開啟、重複輸入保持順暢，再進行模型實驗。
2. **[P0：驗證文字輸入工具](https://github.com/chunkai4u/gelab-androidworld-project/issues/2)｜Agent 負責人**  
   測試官方 YADB 工具能否正確輸入檔名、空白、標點與多行文字。原本的輸入方式曾漏字，替代工具已接上但未驗證。必須保留要求的完整內容，且不要自動送出欄位。
3. **[P1：完成筆記與 SMS 的基本測試](https://github.com/chunkai4u/gelab-androidworld-project/issues/3)｜實驗負責人**  
   透過模型操作完成 `MarkorCreateNote` 與 `MarkorCreateNoteAndSms`，使用未修改的官方判定器檢查結果，確認錄影完整。失敗也保留，並記下實際原因。
4. **[P1：固定設定並進行九次正式評估](https://github.com/chunkai4u/gelab-androidworld-project/issues/4)｜評估負責人**  
   固定程式、環境與模型設定後，每個任務執行三次並記錄種子。收集官方判定、動作數、耗時、完整影片與紀錄連結，以及失敗分類。環境故障要另外標示，不可直接省略。
5. **[P1：準備專案故事、結果與簡報](https://github.com/chunkai4u/gelab-androidworld-project/issues/5)｜報告負責人**  
   說明三類任務、系統架構、實際成功率，以及失敗與恢復的例子。清楚註明這是自行整合的 GELab agent，且 AndroidWorld 使用經過調整的任務子集環境。

建議審查原則：正式設定固定前，若修改模型提示、輸入工具、裝置設定或判定器的串接方式，需補上清楚標記的基本功能測試。不要為了取得 PASS 而修改官方判定邏輯。
