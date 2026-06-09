# Dashboard Template Markers

Google Sheet 或 Excel 模板可以使用下列 placeholder。Agent 會依照 placeholder 所在位置填入資料、公式、表格或圖表。

## 基本資訊

```text
{{dashboard_title}}
{{generated_at}}
{{date_range}}
{{data_source}}
{{dashboard_note}}
```

## KPI

```text
{{total_spend}}
{{total_revenue}}
{{total_conversions}}
{{roas}}
{{cpa}}
{{ctr}}
{{total_clicks}}
{{total_impressions}}
{{total_users}}
```

## 表格

```text
{{channel_performance_table}}
{{campaign_performance_table}}
{{top_campaign_table}}
{{bottom_campaign_table}}
{{anomaly_summary_table}}
```

## 圖表

```text
{{daily_trend_chart}}
{{spend_revenue_chart}}
{{channel_mix_chart}}
{{roas_by_channel_chart}}
{{campaign_top10_chart}}
```

## 設定表

如果模板中有 `Config` sheet，建議使用三欄：

```text
key | value | note
```

常用 key：

```text
data_sheet
dashboard_sheet
date_column
default_days
primary_dimension
secondary_dimension
currency
timezone
dashboard_title
```

範例：

```text
key | value | note
data_sheet | Raw Data | 原始資料貼到這張 sheet
dashboard_sheet | Dashboard | dashboard 放在這張 sheet
date_column | date | 日期欄位
default_days | 30 | 預設分析最近 30 天
primary_dimension | source | 主要比較維度
secondary_dimension | campaign_name | 次要比較維度
currency | JPY | 顯示幣別
```

## 使用規則

- Placeholder 必須使用雙大括號，例如 `{{roas}}`。
- 使用者可以移動 placeholder 到想要的位置。
- 使用者可以改顏色、字體、欄寬、圖表位置。
- Agent 只應替換 placeholder 或在 placeholder 附近插入內容。
- 不要覆蓋沒有 placeholder 的手動說明文字。
