---
name: naming-convention
description: Validate campaign, ad group, ad set, and ad names using naming rules maintained in references/rules.md.
---

# Naming Convention Skill

當使用者要求檢查命名規則、檢查 campaign name、檢查 ad group / ad set / ad name 格式，或要求找出不符合命名規範的項目時，使用這個 skill。

## 任務

1. 讀取本 skill 的規則檔：

```text
.claude/skills/naming-convention/references/rules.md
```

2. 檢查以下資料中的名稱欄位：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/360.csv
```

3. 驗證欄位：

- `campaign_name`
- `ad_group`
- `ad_set`
- `ad_group_name`
- `ad_name`

4. 找出不符合規則的名稱。

5. 將結果輸出為 markdown 報告，放在：

```text
reports/
```

## 報告內容

報告至少應包含：

- 檢查日期
- 使用的規則檔案
- 檢查資料來源
- 命名規則摘要
- 不符合規則的清單
- 嚴重程度：`High`、`Medium`、`Low`
- 建議命名修正
- 需要人工確認的事項

## 注意事項

- 不修改 raw data。
- 不修改 `fake-data-script/`。
- 不直接批次改名。
- 若命名規則不足以判斷，應標記為「需要人工確認」。
