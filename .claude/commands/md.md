# md

使用 `dashboard-generator` skill，根據：

```text
.claude/skills/dashboard-generator/references/rules.md
.claude/skills/dashboard-generator/references/template-markers.md
.claude/skills/dashboard-generator/references/report-types.md
```

讀取主要資料：

```text
data/360.csv
```

產生行銷 dashboard。

如果使用者沒有指定模板，使用預設行銷成效總覽版型。

如果使用者指定 `template/` 內的模板，優先保留模板版面，並依照 placeholder 或 `Config` sheet 填入資料。

產出優先順序：

1. Google Sheet dashboard
2. `.xlsx` dashboard
3. markdown dashboard 規格或說明

Dashboard 至少需包含：

- Spend
- Revenue
- Conversions
- ROAS
- CPA
- CTR
- Daily trend
- Channel performance
- Campaign performance
- Top / bottom campaign
- Anomaly summary

禁止：

- 不修改 `data/360.csv`
- 不修改 raw data
- 不修改 `fake-data-script/`
- 不覆寫既有 dashboard 或報告，除非使用者明確要求
