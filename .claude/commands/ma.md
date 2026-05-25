# ma

使用 `anomaly-detection` skill，根據：

```text
.claude/skills/anomaly-detection/references/rules.md
```

檢查：

```text
data/360.csv
```

做跨維度異常偵測，並輸出 markdown 報告到：

```text
reports/anomaly-detection-YYYY-MM-DD.md
```

報告需包含：

- 檢查日期
- 使用的 skill
- 使用的 rules 檔案
- 檢查資料來源
- 異常摘要
- 異常清單
- 嚴重程度
- 可能原因
- 建議下一步
- 需要人工確認的事項

禁止：

- 不修改 `data/`
- 不修改 `fake-data-script/`
- 不覆寫既有報告，除非使用者明確要求
