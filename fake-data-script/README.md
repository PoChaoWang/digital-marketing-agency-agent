# Fake Data Scripts

這個資料夾負責產生 lululemon Japan 的 fake raw marketing data，並把 raw CSV 合併成 `data/360.csv`。

## Scripts

```text
generate_lululemon_fake_data.py  # 產生三份 raw CSV
build_360_csv.py                 # 用 DuckDB + SQL 合併成 data/360.csv
sql/ads_unified.sql              # 合併邏輯
```

## 產生 Raw CSV

```bash
.venv/bin/python fake-data-script/generate_lululemon_fake_data.py --end-date 2026-05-25
```

指定日期區間：

```bash
.venv/bin/python fake-data-script/generate_lululemon_fake_data.py \
  --start-date 2026-05-01 \
  --end-date 2026-05-25
```

指定輸出資料夾：

```bash
.venv/bin/python fake-data-script/generate_lululemon_fake_data.py \
  --start-date 2026-05-25 \
  --end-date 2026-05-25 \
  --output-dir data
```

參數：

- `--start-date YYYY-MM-DD`：資料起始日期。未指定時會從 `--end-date` 往前推 179 天。
- `--end-date YYYY-MM-DD`：資料結束日期。預設是執行當天。
- `--output-dir data`：CSV 輸出資料夾。
- `--seed 20260525`：random seed，用來讓資料可重現。

輸出：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/ga4_raw.csv
```

## 合併成 360.csv

```bash
.venv/bin/python fake-data-script/build_360_csv.py
```

輸出：

```text
data/360.csv
```

如需指定輸出路徑：

```bash
.venv/bin/python fake-data-script/build_360_csv.py --output data/360.csv
```

## GA4 Paid Data 對應規則

GA4 paid rows 由 Google Ads 與 Meta Ads raw rows 產生，因此 key 可以直接回連：

- `utm_campaign` 對應 `campaign_name`
- `utm_id` 對應 Google Ads `ad_group` 或 Meta Ads `ad_set`
- `utm_content` 對應 `ad_name`
- Google Ads 使用 `source=google`、`medium=cpc`
- Meta Ads 使用 `source=meta`、`medium=paid_social`

## 資料特徵

- 日本市場
- JPY 幣別
- 每日粒度
- Google Ads campaign type：`pmax`、`sho`、`gdn`
- Meta ad format：`img`、`vid`、`col`、`car`
- Meta 另有 `dynamic` retargeting 活動
- campaign 區分 `prospecting` 與 `retargeting`
- 週五、週六表現較好
- Black Friday、年末促銷、新年檔期有流量與轉換提升
- Golden Week 期間流量不低，但轉換率較差

## 乾淨資料原則

目前 fake data 模擬 API 回傳的乾淨平台資料，不再刻意加入 ETL 測試用髒資料：

- 不產生缺失 key
- 不產生空白 campaign / ad group / ad set / ad name
- 不產生 duplicated rows
- 不產生 clicks 大於 impressions
- 不產生隨機格式錯誤
- 不產生人為 tracking loss 測試情境
