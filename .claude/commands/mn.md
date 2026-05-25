# mn

使用 `naming-convention` skill，根據：

```text
.claude/skills/naming-convention/references/rules.md
```

檢查以下資料中的命名欄位：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/360.csv
```

需要檢查：

- `campaign_name`
- `ad_group`
- `ad_set`
- `ad_group_name`
- `ad_name`

並輸出 markdown 報告到：

```text
reports/naming-convention-YYYY-MM-DD.md
```

報告需包含：

- 檢查日期
- 使用的 skill
- 使用的 rules 檔案
- 檢查資料來源
- 命名規則摘要
- 不符合規則的清單
- 嚴重程度
- 建議命名修正
- 需要人工確認的事項

禁止：

- 不修改 `data/`
- 不修改 `fake-data-script/`
- 不覆寫既有報告，除非使用者明確要求
