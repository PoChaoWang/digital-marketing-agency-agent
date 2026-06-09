# Dashboard Generator Rules

這份規則給 `dashboard-generator` skill 使用。行銷人員可以用自然語言修改規則，不需要寫程式。

## 基本原則

- Dashboard 主要服務非技術行銷人員，輸出要能直接閱讀與分享。
- 預設使用 `data/360.csv`。
- 預設不要修改 raw data，也不要修改 fake data 產生腳本。
- 預設以 Google Sheet dashboard 為優先輸出。
- 如果環境無法直接產生 Google Sheet，改產生 `.xlsx` 或 markdown dashboard 規格。
- 若使用者提供模板，優先保留模板設計，只替換明確標記或填入指定區塊。

## 預設分析期間

- 如果使用者沒有指定日期，使用資料中最新日期往前 30 天。
- 如果資料少於 30 天，使用全部資料。
- Dashboard 應顯示實際使用的日期區間。

## 預設 KPI

Dashboard 至少應包含：

- Spend
- Revenue
- Conversions
- ROAS
- CPA
- CTR

計算方式：

- `spend = sum(spend)`
- `revenue = sum(revenue)`
- `conversions = sum(conversions)`
- `roas = revenue / spend`
- `cpa = spend / conversions`
- `ctr = clicks / impressions`

如果分母為 0，該 KPI 顯示為 `N/A`，不要硬算成 0。

## 預設維度

優先使用以下維度：

- `date`
- `source`
- `campaign_name`
- `ad_type`
- `campaign_type`

如果欄位不存在，使用最接近的欄位，並在說明中註記。

## 預設區塊

沒有指定模板時，dashboard 預設包含：

- KPI summary
- Daily trend
- Channel performance
- Campaign performance
- Top 10 campaigns by revenue
- Bottom 10 campaigns by ROAS
- Anomaly summary

## 條件格式

建議使用以下視覺提示：

- ROAS 低於 1：標示為 High risk
- ROAS 介於 1 到 2：標示為 Medium risk
- CPA 明顯高於平均：標示為需要確認
- spend 有量但 revenue 或 conversions 為 0：標示為需要確認

## 模板優先規則

如果使用者指定 `template/` 內的模板：

- 優先使用模板中的 placeholder。
- 優先讀取模板中的 `Config` sheet 或設定表。
- 不要求使用者提供 YAML。
- 如果找不到 placeholder，但模板有明確 dashboard 頁面，保留模板並在空白區域新增資料表。
- 如果模板完全無法判斷用途，改用預設 dashboard 版型，並在說明中列出原因。

## 產出要求

產出完成後，需提供：

- 使用的資料來源
- 使用的模板
- 建立的 sheet 或檔案
- Dashboard 包含哪些 KPI、圖表、表格
- 哪些內容是自動判斷
- 哪些內容需要人工確認
- 如何調整模板後重新產生
