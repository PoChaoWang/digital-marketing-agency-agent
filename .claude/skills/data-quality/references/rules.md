# Data Quality Rules

這個檔案是行銷人員維護資料品質規則的地方。

請用自然語言描述 lululemon Japan 行銷資料的品質標準。Agent 執行資料品質檢查時，應先讀取本檔案，再檢查 `data/` 下的 CSV。

## 檢查資料

需要檢查的檔案：

- `data/google_ads_raw.csv`
- `data/meta_ads_raw.csv`
- `data/ga4_raw.csv`
- `data/360.csv`

## 必要欄位不得為空

Google Ads raw data：

- `date`
- `campaign_name`
- `ad_group`
- `ad_name`
- `impressions`
- `clicks`
- `spend`
- `conversions`
- `conversion_value`

Meta Ads raw data：

- `date`
- `campaign_name`
- `ad_set`
- `ad_name`
- `impressions`
- `clicks`
- `spend`
- `conversions`
- `conversion_value`

GA4 raw data：

- `date`
- `source`
- `medium`
- `sessions`
- `users`
- `new_users`
- `conversions`
- `revenue`

360 data：

- `date`
- `source`
- `campaign_name`
- `ad_group_name`
- `ad_name`
- `impressions`
- `clicks`
- `spend`
- `conversions`
- `revenue`
- `users`
- `new_users`
- `ga4_conversions`
- `ga4_revenue`

## 數值合理性

- `impressions` 不應小於 0。
- `clicks` 不應小於 0。
- `spend` 不應小於 0。
- `conversions` 不應小於 0。
- `revenue` 不應小於 0。
- `clicks` 不應超過 `impressions`。
- 若 `spend > 0` 且 `clicks = 0`，需要標記為 `Medium`，並確認是否為曝光型投放。
- 若 `clicks > 0` 且 `spend = 0`，需要標記為 `Medium`，並確認是否為平台回傳延遲或資料缺失。

## CTR 標準

CTR 定義：

```text
clicks / impressions
```

一般判斷：

- Google Search / Shopping / PMax 類型 CTR 長期低於 0.5% 時，需要人工確認。
- Google Display 類型 CTR 高於 5% 時，需要人工確認。
- Meta prospecting CTR 低於 0.3% 時，需要人工確認。
- Meta retargeting CTR 高於 8% 時，需要人工確認是否有受眾過小或資料異常。

## ROAS 標準

ROAS 定義：

```text
revenue / spend
```

一般判斷：

- 單日 ROAS 小於 0.5，標記為 `Medium`。
- 單日 ROAS 大於 20，標記為 `Medium`，需要確認是否有 revenue 或 spend 回傳異常。
- 連續多日 ROAS 小於 1，標記為 `High`，需要人工排查 campaign 表現或資料追蹤問題。

## GA4 對應品質

- `data/360.csv` 中，若 `spend > 0` 但 `users = 0`，標記為 `High`。
- `data/360.csv` 中，若 `clicks > 0` 但 `users = 0`，標記為 `High`。
- Google Ads 的 `campaign_name + ad_group + ad_name` 應可對應到 GA4 的 `utm_campaign + utm_id + utm_content`。
- Meta Ads 的 `campaign_name + ad_set + ad_name` 應可對應到 GA4 的 `utm_campaign + utm_id + utm_content`。

## 報告要求

報告中每個問題都應包含：

- 問題描述
- 影響檔案
- 影響欄位
- 影響筆數或範例 rows
- 嚴重程度
- 建議處理方式
