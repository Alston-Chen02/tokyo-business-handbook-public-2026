# Tokyo business handbook public edition
公開網址：https://alston-chen02.github.io/tokyo-business-handbook-public-2026/
公開版不刊登個人聯絡人姓名或電話；私人聯絡與備忘僅保存在使用者手機。

## 匯率
日圓金額 × 臺灣銀行「即期賣出」= 台幣預算。
GitHub Actions 以官方牌告網頁讀取 JPY 即期賣出及牌告時間，約每 15 分鐘排程一次；排程可能延遲。只有成功解析的官方資料才寫入 rate-data 分支的 jpy.json，手機從該公開 JSON 讀取。開啟、回到前景、恢復連線、更新按鈕及頁面每分鐘會檢查同步資料。
無法抓取時保留上次牌告；同步超過 45 分鐘明示延遲。資料沒有宣稱是逐秒報價。離線已有快取時仍可換算。輸入金額不送往後端。

## 部署
GitHub Actions 的 Publish handbook to GitHub Pages：mode=publish 发布網站，mode=rates 僅更新匯率，不部署網站。schedule 僅同步匯率。匯率同步失敗不寫入任何替代或虛構值。

天氣由 Open-Meteo 提供，頁面開啟期間每 15 分鐘更新；現況為模式估計。
原始資料為山善 R1 及 JIMTOF 行程，注意事項由官方資料於 2026/10/14 查證。個人機票、每日集合及巡航預訂須與導遊確認。
