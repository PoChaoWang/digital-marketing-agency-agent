# Dashboard Template Guide

這個資料夾用來放 dashboard 模板。

非技術使用者不需要寫 YAML、JSON 或程式碼。建議直接用 Google Sheet 或 Excel 做模板，然後把要給 AI 填入的位置放上 placeholder。

可以先參考這份範例：

```text
template/marketing-dashboard-template.md
```

## 建議模板結構

一份 dashboard 模板建議包含這幾張 sheet：

```text
README
Config
Raw Data
Dashboard
```

用途：

- `README`：給使用者看的說明。
- `Config`：給 AI 讀取的設定表。
- `Raw Data`：放原始資料。
- `Dashboard`：放最後要看的 dashboard。

## Config Sheet

`Config` 建議使用一般表格，不需要寫程式：

```text
key | value | note
data_sheet | Raw Data | 原始資料放這裡
dashboard_sheet | Dashboard | dashboard 放這裡
date_column | date | 日期欄位
default_days | 30 | 預設分析最近 30 天
primary_dimension | source | 主要比較維度
secondary_dimension | campaign_name | 次要比較維度
currency | JPY | 顯示幣別
```

## Placeholder

在 `Dashboard` sheet 放入 placeholder，AI 會把資料填到對應位置。

常用 placeholder：

```text
{{dashboard_title}}
{{date_range}}
{{total_spend}}
{{total_revenue}}
{{total_conversions}}
{{roas}}
{{cpa}}
{{ctr}}
{{daily_trend_chart}}
{{channel_performance_table}}
{{campaign_performance_table}}
{{top_campaign_table}}
{{anomaly_summary_table}}
```

## 使用方式

1. 複製一份 Google Sheet 或 Excel dashboard 模板。
2. 調整顏色、標題、文字與區塊位置。
3. 把 placeholder 放到希望 AI 填入的位置。
4. 如果需要調整分析邏輯，修改 `Config` sheet。
5. 請 AI 使用 `dashboard-generator` skill 或輸入短指令：

```text
md
```

## 注意事項

- 不要刪掉需要 AI 填入的 placeholder。
- 可以自由調整模板外觀。
- 可以新增說明文字，AI 預設不會覆蓋沒有 placeholder 的文字。
- 如果 HTML 或圖表產生時間較久，建議先產出 markdown 或 Google Sheet 版本確認內容。
