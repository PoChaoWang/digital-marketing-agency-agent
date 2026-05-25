# Data Quality Report

## 基本資訊

- 檢查日期：2026-05-25
- 使用 skill：`data-quality`
- 使用 rules 檔案：`.claude/skills/data-quality/references/rules.md`
- 輸出報告：`reports/data-quality-2026-05-25.md`

## 檢查資料來源

- `data/google_ads_raw.csv`
- `data/meta_ads_raw.csv`
- `data/ga4_raw.csv`
- `data/360.csv`

## 摘要

本次檢查未發現必要欄位空值、負數指標、`clicks > impressions`、`spend > 0 且 clicks = 0`、`clicks > 0 且 spend = 0` 等基礎資料品質問題。

`data/360.csv` 的 GA4 對應品質也通過基本檢查：沒有發現 `spend > 0 但 users = 0` 或 `clicks > 0 但 users = 0` 的 rows。

需要人工確認的問題集中在 ROAS 規則：以 campaign-day 聚合後，有部分 campaign-day ROAS 低於 0.5 或高於 20。這可能是正常 fake data 商業波動，也可能代表規則閾值需要依 campaign type 調整。

## 檢查結果總覽

| 檔案 | Rows | 必要欄位空值 | 負數指標 | clicks > impressions | spend > 0 且 clicks = 0 | clicks > 0 且 spend = 0 |
|---|---:|---:|---:|---:|---:|---:|
| `data/google_ads_raw.csv` | 77,760 | 0 | 0 | 0 | 0 | 0 |
| `data/meta_ads_raw.csv` | 37,440 | 0 | 0 | 0 | 0 | 0 |
| `data/ga4_raw.csv` | 122,169 | 0 | 0 | N/A | N/A | N/A |
| `data/360.csv` | 115,200 | 0 | 0 | 0 | 0 | 0 |

## 發現問題清單

### Medium: campaign-day ROAS 低於 0.5

- 影響檔案：`data/360.csv`
- 影響欄位：`date`, `source`, `campaign_name`, `spend`, `revenue`
- 影響筆數：9,484 個 campaign-day 聚合結果
- 嚴重程度：`Medium`

依據 `rules.md`，單日 ROAS 小於 0.5 需標記為 `Medium`。本次檢查以 `date + source + campaign_name` 聚合後計算：

```text
ROAS = sum(revenue) / sum(spend)
```

範例：

| date | source | campaign_name | spend | revenue | ROAS |
|---|---|---|---:|---:|---:|
| 2026-01-23 | meta | `jp_meta_vid_prospecting_women_yoga` | 2,607 | 0 | 0.000 |
| 2026-01-23 | meta | `jp_meta_vid_retargeting_men_running` | 845 | 0 | 0.000 |
| 2026-01-23 | meta | `jp_meta_vid_retargeting_women_training` | 1,338 | 0 | 0.000 |
| 2026-01-24 | meta | `jp_meta_vid_retargeting_men_training` | 1,444 | 0 | 0.000 |
| 2026-01-24 | meta | `jp_meta_vid_retargeting_women_yoga` | 1,032 | 0 | 0.000 |

可能原因：

- 單日 campaign 粒度較細，部分 campaign 當日沒有 conversion 或 revenue 是合理現象。
- 目前規則未區分 prospecting、retargeting、dynamic、Google、Meta 等不同投放類型。
- 若這是 API-like fake data，低 ROAS 案例可能代表需要以更長時間窗，例如 7 日或 14 日，評估 campaign 表現。

建議對策：

- 行銷人員確認是否要將 ROAS 低於 0.5 的規則改為連續多日或 rolling window。
- 建議在 `rules.md` 補充不同 campaign type 的 ROAS 閾值。
- 若要用單日規則，建議只對 spend 超過最低門檻的 campaign-day 套用，例如 spend >= 10,000 JPY。

### Medium: campaign-day ROAS 高於 20

- 影響檔案：`data/360.csv`
- 影響欄位：`date`, `source`, `campaign_name`, `spend`, `revenue`
- 影響筆數：420 個 campaign-day 聚合結果
- 嚴重程度：`Medium`

依據 `rules.md`，單日 ROAS 大於 20 需標記為 `Medium`，需要確認是否有 revenue 或 spend 回傳異常。

範例：

| date | source | campaign_name | spend | revenue | ROAS |
|---|---|---|---:|---:|---:|
| 2025-11-29 | meta | `jp_meta_dynamic_retargeting_women_running` | 1,646 | 66,258 | 40.254 |
| 2026-01-27 | meta | `jp_meta_dynamic_retargeting_women_yoga` | 1,309 | 47,032 | 35.930 |
| 2026-03-21 | meta | `jp_meta_dynamic_retargeting_women_training` | 1,067 | 37,692 | 35.325 |
| 2025-11-30 | meta | `jp_meta_vid_retargeting_women_training` | 1,903 | 63,650 | 33.447 |
| 2026-02-05 | meta | `jp_meta_dynamic_retargeting_women_yoga` | 1,221 | 39,593 | 32.427 |

可能原因：

- dynamic retargeting 或 retargeting campaign 在小 spend 下產生高 ROAS，可能是合理現象。
- 單日 spend 分母偏小，容易讓 ROAS 被放大。
- 規則目前未針對 dynamic retargeting 設定不同上限。

建議對策：

- 行銷人員確認 dynamic retargeting 的 ROAS 上限是否應高於一般 prospecting campaign。
- 建議加入最低 spend 門檻後再判斷高 ROAS，例如 spend >= 10,000 JPY。
- 建議分 source、campaign_type、ad_type 建立不同 ROAS 正常範圍。

## 通過檢查項目

- 必要欄位不得為空：通過
- 數值不得為負：通過
- `clicks` 不應超過 `impressions`：通過
- `spend > 0` 且 `clicks = 0`：未發現
- `clicks > 0` 且 `spend = 0`：未發現
- `spend > 0` 但 `users = 0`：未發現
- `clicks > 0` 但 `users = 0`：未發現
- Google PMax / Shopping campaign CTR 長期低於 0.5%：未發現
- Google Display campaign CTR 高於 5%：未發現
- Meta prospecting CTR 低於 0.3%：未發現
- Meta retargeting CTR 高於 8%：未發現

## 需要人工確認的事項

1. ROAS 規則是否要用單日 campaign 粒度判斷，或改用 7 日 / 14 日 rolling window。
2. 是否要為 prospecting、retargeting、dynamic 設定不同 ROAS 閾值。
3. 是否要設定最低 spend 門檻，避免小 spend campaign-day 產生大量 ROAS 過高或過低警示。
4. 是否要把 `revenue` 與 `ga4_revenue` 的差異納入下一版資料品質規則。

## 禁止行為遵守狀態

- 未修改 `data/` 內任何 CSV。
- 未修改 `fake-data-script/`。
- 未覆寫既有報告。
