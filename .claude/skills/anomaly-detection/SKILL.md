---
name: anomaly-detection
description: Detect marketing performance anomalies in data/360.csv using business rules maintained in references/rules.md.
---

# Anomaly Detection Skill

當使用者要求偵測異常、找出表現不合理的 campaign、檢查 spend / ROAS / CTR / users 是否異常，或要求做跨維度比較時，使用這個 skill。

## 任務

1. 讀取本 skill 的規則檔：

```text
.claude/skills/anomaly-detection/references/rules.md
```

2. 讀取主要檢查資料：

```text
data/360.csv
```

3. 依照規則做跨維度比較，例如：

- 日期
- source
- campaign
- ad group
- ad name
- campaign type
- ad type

4. 找出超出預期範圍的數值或趨勢。

5. 將結果輸出為 markdown 報告，放在：

```text
reports/
```

## 報告內容

報告至少應包含：

- 檢查日期
- 使用的規則檔案
- 檢查資料來源
- 異常摘要
- 異常清單
- 嚴重程度：`High`、`Medium`、`Low`
- 可能原因
- 建議下一步
- 需要人工確認的事項

## 注意事項

- 不修改 `data/360.csv`。
- 不修改 raw data。
- 不修改 `fake-data-script/`。
- 如果缺少歷史比較基準，應在報告中說明限制，不可假裝已完成趨勢判斷。
