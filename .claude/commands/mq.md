# mq

使用 `data-quality` skill，根據：

```text
.claude/skills/data-quality/references/rules.md
```

檢查 `data/` 下所有 CSV：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/ga4_raw.csv
data/360.csv
```

並輸出 markdown 報告到：

```text
reports/data-quality-YYYY-MM-DD.md
```

報告需包含：

- 檢查日期
- 使用的 skill
- 使用的 rules 檔案
- 檢查資料來源
- 摘要
- 發現問題清單
- 嚴重程度
- 可能原因
- 建議對策
- 需要人工確認的事項

禁止：

- 不修改 `data/`
- 不修改 `fake-data-script/`
- 不覆寫既有報告，除非使用者明確要求
