# Marketing Dashboard Template Example

這是一份可以複製到 Google Sheet 的 dashboard 模板範例。

實際使用時，建議在 Google Sheet 建立以下 sheet：

```text
README
Config
Raw Data
Dashboard
```

## Config

在 `Config` sheet 放入以下表格：

| key | value | note |
| --- | --- | --- |
| data_sheet | Raw Data | 原始資料放這裡 |
| dashboard_sheet | Dashboard | dashboard 放這裡 |
| date_column | date | 日期欄位 |
| default_days | 30 | 預設分析最近 30 天 |
| primary_dimension | source | 主要比較維度 |
| secondary_dimension | campaign_name | 次要比較維度 |
| currency | JPY | 顯示幣別 |
| dashboard_title | Marketing Performance Dashboard | dashboard 標題 |

## Dashboard

在 `Dashboard` sheet 放入以下 placeholder。你可以移動位置、改顏色、改字體、加上說明文字。

| 區塊 | 建議位置 | placeholder |
| --- | --- | --- |
| 標題 | A1 | `{{dashboard_title}}` |
| 日期區間 | A2 | `{{date_range}}` |
| Spend | A4 | `{{total_spend}}` |
| Revenue | C4 | `{{total_revenue}}` |
| Conversions | E4 | `{{total_conversions}}` |
| ROAS | G4 | `{{roas}}` |
| CPA | I4 | `{{cpa}}` |
| CTR | K4 | `{{ctr}}` |
| 每日趨勢圖 | A7 | `{{daily_trend_chart}}` |
| Channel 表格 | A25 | `{{channel_performance_table}}` |
| Campaign 表格 | A40 | `{{campaign_performance_table}}` |
| Top campaign | H25 | `{{top_campaign_table}}` |
| 異常摘要 | H40 | `{{anomaly_summary_table}}` |

## 使用方式

1. 在 Google Sheet 建立上述 sheet。
2. 將 `Config` 表格貼到 `Config` sheet。
3. 將 `Dashboard` placeholder 放到想要的位置。
4. 調整顏色、字體、欄寬與說明文字。
5. 請 AI 使用 `dashboard-generator` skill 或輸入：

```text
md
```

Agent 會優先保留你的版面，只替換 placeholder 或在 placeholder 附近插入圖表與表格。
