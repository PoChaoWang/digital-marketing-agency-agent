---
name: data-quality
description: Check marketing CSV data quality using business rules maintained in references/rules.md.
---

# Data Quality Skill

當使用者要求執行資料品質檢查、檢查 raw data、檢查 360.csv、盤查資料是否合理，或要求找出資料問題時，使用這個 skill。

## 任務

1. 讀取本 skill 的規則檔：

```text
.claude/skills/data-quality/references/rules.md
```

2. 逐一檢查 `data/` 下的 CSV 檔案：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/ga4_raw.csv
data/360.csv
```

3. 依照 `references/rules.md` 的規則，找出資料品質問題。

4. 將檢查結果輸出為 markdown 報告，放在：

```text
reports/
```

## 報告內容

報告至少應包含：

- 檢查日期
- 使用的規則檔案
- 檢查的 CSV 檔案
- 檢查摘要
- 問題清單
- 嚴重程度：`High`、`Medium`、`Low`
- 問題影響
- 建議處理方式
- 需要人工確認的事項

## 注意事項

- 不修改 `data/` 內任何 CSV。
- 不修改 `fake-data-script/`。
- 不自行改寫規則。
- 如果規則不清楚，應在報告中列為「需要人工確認」。
