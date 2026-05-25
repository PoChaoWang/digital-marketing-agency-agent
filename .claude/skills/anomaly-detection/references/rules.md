# Anomaly Detection Rules

這個檔案是行銷人員維護異常判斷標準的地方。

Agent 執行異常偵測時，應先讀取本檔案，再檢查 `data/360.csv`。

## 主要檢查資料

```text
data/360.csv
```

## 異常定義

以下情境需要標記為異常。

## Spend 異常

- 同一 campaign 的單日 spend 比前一日增加超過 200%，標記為 `High`。
- 同一 campaign 的單日 spend 比過去 7 日平均增加超過 200%，標記為 `High`。
- 同一 campaign spend 連續 3 日增加，但 revenue 沒有同步增加，標記為 `Medium`。
- 任一 campaign 單日 spend > 0，但 clicks = 0，標記為 `Medium`。

## Impression 異常

- 某 campaign 前一日有 impression，但今日 impression = 0，標記為 `High`。
- 某 source 整體 impression 單日下降超過 70%，標記為 `High`。
- retargeting campaign impression 連續 3 日下降，標記為 `Medium`。

## CTR 異常

CTR 定義：

```text
clicks / impressions
```

- CTR 突然比前一日增加超過 300%，標記為 `Medium`。
- CTR 突然比前一日下降超過 70%，標記為 `Medium`。
- impressions 很高但 clicks 接近 0，標記為 `Medium`。

## ROAS 異常

ROAS 定義：

```text
revenue / spend
```

- ROAS 連續 3 日下滑，標記為 `High`。
- ROAS 單日低於 0.5，標記為 `Medium`。
- ROAS 單日高於 20，標記為 `Medium`，需要確認 revenue 是否異常。
- spend 增加但 ROAS 明顯下降，標記為 `High`。

## GA4 指標異常

- clicks > 0 但 users = 0，標記為 `High`。
- spend > 0 但 ga4_revenue = 0，標記為 `Medium`，需要確認是否為正常無轉換或追蹤問題。
- conversions 與 ga4_conversions 差異過大，標記為 `Medium`。
- revenue 與 ga4_revenue 差異過大，標記為 `Medium`。

## 維度比較

偵測異常時，至少從以下維度觀察：

- source：`google`、`meta`
- campaign_type：`prospecting`、`retargeting`、`dynamic`
- ad_type：`pmax`、`sho`、`gdn`、`img`、`vid`、`col`、`car`
- campaign_name
- ad_group_name
- ad_name

## 報告要求

每個異常都應包含：

- 異常描述
- 影響日期
- 影響 campaign 或維度
- 實際數值
- 參考基準
- 嚴重程度
- 可能原因
- 建議下一步
