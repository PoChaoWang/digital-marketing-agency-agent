# Naming Convention Rules

這個檔案是行銷人員維護命名規則的地方。

Agent 執行命名檢查時，應先讀取本檔案，再檢查 `data/` 下的 campaign、ad group、ad set、ad name。

## Campaign 命名格式

lululemon Japan campaign name 建議格式：

```text
[市場]_[平台]_[類型]_[漏斗階段]_[產品線]
```

範例：

```text
jp_google_pmax_prospecting_women_yoga
jp_google_sho_retargeting_bags
jp_meta_img_prospecting_women_running
jp_meta_dynamic_retargeting_men_training
```

## 欄位定義

`市場`：

- `jp`

`平台`：

- `google`
- `meta`

`類型`：

Google Ads：

- `pmax`
- `sho`
- `gdn`

Meta Ads：

- `img`
- `vid`
- `col`
- `car`
- `dynamic`

`漏斗階段`：

- `prospecting`
- `retargeting`

`產品線`：

- `women_yoga`
- `women_running`
- `women_training`
- `women_new_arrivals`
- `men_running`
- `men_training`
- `bags`
- `accessories`

## Google Ads Ad Group 命名格式

Google Ads ad group 建議格式：

```text
[類型]_[漏斗階段]_[產品線]_[受眾]
```

範例：

```text
pmax_prospecting_women_yoga_core
sho_retargeting_bags_intent
gdn_prospecting_men_running_lookalike
```

允許的受眾：

- `core`
- `lookalike`
- `intent`

## Meta Ads Ad Set 命名格式

Meta Ads ad set 建議格式：

```text
[格式]_[漏斗階段]_[產品線]_[性別年齡]
```

範例：

```text
img_prospecting_women_yoga_women25_50
vid_retargeting_men_running_men25_50
dynamic_retargeting_bags
```

允許的性別年齡：

- `women25_50`
- `men25_50`

## Ad Name 命名格式

Google Ads ad name 建議格式：

```text
[產品線]_[素材角度]_[序號]
```

範例：

```text
women_yoga_benefit_1
bags_product_2
men_training_seasonal_3
```

Meta Ads ad name 建議格式：

```text
[產品線]_[格式]_[素材角度]
```

範例：

```text
women_yoga_img_lifestyle
men_running_vid_product
bags_col_offer
```

## 命名品質標準

- 全部使用小寫。
- 使用底線 `_` 分隔。
- 不使用空白。
- 不使用中文、日文或特殊符號。
- 不使用未定義縮寫。
- 不省略市場、平台、類型、漏斗階段或產品線。

## 嚴重程度

- `High`：campaign name 無法判斷市場、平台或漏斗階段。
- `Medium`：campaign name 可判斷主要資訊，但產品線或類型不符合規則。
- `Low`：大小寫、分隔符號、序號格式等輕微不一致。

## 報告要求

每個命名問題都應包含：

- 來源檔案
- 欄位名稱
- 原始名稱
- 違反的規則
- 嚴重程度
- 建議命名
