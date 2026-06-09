---
name: dashboard-generator
description: Generate marketing dashboards from data/360.csv or user-provided Google Sheet templates using non-technical template markers.
---

# Dashboard Generator Skill

當使用者要求產生 dashboard、建立 Google Sheet 報表、把 `data/360.csv` 轉成視覺化看板，或要求套用 `template/` 裡的 dashboard 模板時，使用這個 skill。

## 設計原則

這個 skill 的目標是讓非技術人員可以維護 dashboard，不要求使用者撰寫 YAML、JSON 或程式碼。

優先支援兩種使用方式：

1. 沒有指定模板時，由 agent 根據資料內容自行決定 dashboard 版型。
2. 有指定模板時，優先讀取 `template/` 內的說明與標記，保留使用者設計好的版面、文字、顏色與圖表位置。

## 任務

1. 讀取本 skill 的規則與參考文件：

```text
.claude/skills/dashboard-generator/references/rules.md
.claude/skills/dashboard-generator/references/template-markers.md
.claude/skills/dashboard-generator/references/report-types.md
```

2. 優先讀取主要資料來源：

```text
data/360.csv
```

3. 如果使用者指定模板，讀取：

```text
template/
```

模板可以是 Google Sheet、Excel 檔、CSV 設定表，或以 markdown 描述的模板規格。

4. 先產生 dashboard plan，說明：

- 使用的資料來源
- 使用的模板或預設版型
- 主要 KPI
- 圖表與表格區塊
- 需要填入或替換的模板標記
- 產出位置

5. 依照執行環境選擇輸出方式：

- 如果可以操作 Google Sheet，優先建立或複製 Google Sheet dashboard。
- 如果無法操作 Google Sheet，輸出可上傳 Google Sheet 的 `.xlsx` 或 markdown dashboard 規格到 `reports/`。

6. 輸出完成後，附上使用說明，讓使用者知道如何查看、修改與重跑 dashboard。

## 預設 Dashboard 內容

如果使用者沒有指定模板，預設建立行銷成效總覽 dashboard，至少包含：

- Dashboard title
- Date range
- Total spend
- Total revenue
- Total conversions
- ROAS
- CPA
- CTR
- Daily spend / revenue trend
- Channel performance table
- Top campaign table
- Bottom campaign table
- Anomaly summary

## Google Sheet 模板使用方式

非技術人員可以在 Google Sheet 或 Excel 模板中放入 placeholder，例如：

```text
{{dashboard_title}}
{{date_range}}
{{total_spend}}
{{total_revenue}}
{{roas}}
{{daily_trend_chart}}
{{channel_performance_table}}
{{top_campaign_table}}
```

Agent 應找到這些 placeholder，並在相同位置或附近填入對應內容。

若模板中有 `Config` sheet，應優先讀取其中設定。`Config` 應使用一般表格格式：

```text
key | value | note
```

不要要求使用者編輯 YAML 或 JSON。

## 注意事項

- 優先保留模板原本的版面、顏色、說明文字與區塊順序。
- 不覆蓋使用者手動設計的內容，除非該位置是明確的 `{{...}}` placeholder。
- 不修改 `data/360.csv`。
- 不修改 `fake-data-script/`。
- 如果資料欄位不足以建立某個 KPI 或圖表，應在 dashboard 說明中列為「需要人工確認」。
- 如果不能直接建立 Google Sheet，應清楚說明替代輸出檔案與後續操作方式。
