# 行銷資料品質檢查 Agent

## 目的

這個 agent 的目標是協助行銷人員檢查 `data/` 內的行銷資料品質，包含 raw platform data 與合併後的 `360.csv`，並可根據 `360.csv` 產生行銷 dashboard。

行銷人員可以透過維護各 skill 底下的 `references/rules.md`，把業務經驗、異常判斷標準、命名規則、dashboard 規格與檢查邏輯文本化。Claude Code、Codex 或 Gemini CLI 執行時，應讀取這些規則，檢查資料，並輸出 markdown 報告或 dashboard。

## 可用 Skill

- `data-quality`：檢查 `data/` 下 CSV 的基本資料品質，例如必要欄位、數值合理性、clicks 與 impressions 關係、ROAS 與 CTR 範圍。
- `anomaly-detection`：針對 `data/360.csv` 做跨日期、campaign、source、ad type 等維度的異常偵測。
- `naming-convention`：檢查 campaign、ad group、ad set、ad name 是否符合 lululemon Japan 的命名規則。
- `dashboard-generator`：根據 `data/360.csv` 產生行銷 dashboard；如果使用者提供 `template/` 或 Google Sheet 模板，優先保留模板設計並填入資料。

## 執行方式

在 CLI 中描述要執行的檢查，例如：

```text
請使用 data-quality skill 檢查 data/ 下的 CSV，並輸出報告。
```

```text
請偵測 data/360.csv 是否有異常表現。
```

```text
請檢查 campaign 和 ad group 命名是否符合規則。
```

```text
請根據 data/360.csv 產生一份行銷 dashboard。
```

也可以使用短指令：

```text
mq
```

代表執行 `data-quality` skill。

```text
ma
```

代表執行 `anomaly-detection` skill。

```text
mn
```

代表執行 `naming-convention` skill。

```text
md
```

代表執行 `dashboard-generator` skill。

短指令定義放在：

```text
.claude/commands/
```

執行時應先讀取對應 skill 的：

```text
.claude/skills/<skill-name>/references/rules.md
```

再依照規則檢查資料。

## 輸出規格

所有檢查結果都應輸出為 markdown 檔案，放在：

```text
reports/
```

建議檔名格式：

```text
reports/data-quality-YYYY-MM-DD.md
reports/anomaly-detection-YYYY-MM-DD.md
reports/naming-convention-YYYY-MM-DD.md
reports/dashboard-YYYY-MM-DD.md
```

檢查報告至少應包含：

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

嚴重程度建議使用：

- `High`：會造成報表或判斷明顯錯誤，需要優先處理。
- `Medium`：可能影響分析品質，需要排查。
- `Low`：輕微問題或命名不一致，建議修正但不阻擋分析。

Dashboard 產出應優先使用 Google Sheet；如果無法直接操作 Google Sheet，則輸出 `.xlsx` 或 markdown dashboard 規格到 `reports/`。Dashboard 應說明使用的資料來源、模板、KPI、圖表、表格與需要人工確認的事項。

## 禁止行為

Agent 不可以執行以下行為：

- 不修改 `data/` 內的 raw data 或 `360.csv`
- 不修改 `fake-data-script/` 內的資料產生與合併邏輯
- 不覆寫既有報告，除非使用者明確要求
- 不覆寫既有 dashboard 或模板，除非使用者明確要求
- 不在未取得使用者同意前刪除任何檔案
- 不把推測當成事實；無法判斷時，應在報告中標註「需要人工確認」
- 不新增 API key、credential、webhook URL 或任何 secret

Agent 可以做的事情：

- 讀取 CSV
- 讀取 rules markdown
- 彙整檢查結果
- 產生 `reports/` 下的 markdown 報告
- 產生 Google Sheet、`.xlsx` 或 markdown dashboard 規格
- 讀取 `template/` 內的模板說明與 placeholder
- 提出修正建議
- 提出需要人工確認的問題
