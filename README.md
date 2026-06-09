# Digital Marketing Agency Agent Demo

這個專案是用模擬行銷資料展示：行銷人員如何透過維護文字規則，請 AI agent 協助檢查資料品質、偵測異常、檢查命名規則，並輸出可閱讀的報告。

目前資料是 lululemon Japan 的模擬資料，包含 Google Ads、Meta Ads、GA4，以及合併後的 360 行銷資料表。

## 目錄

- [第一次使用：給非技術人員的建議流程](#第一次使用給非技術人員的建議流程)
- [AI Agent 可以做什麼](#ai-agent-可以做什麼)
- [可用指令](#可用指令)
- [報告會輸出到哪裡](#報告會輸出到哪裡)
- [四個 Skill 的功用](#四個-skill-的功用)
- [行銷人員該怎麼維護規則](#行銷人員該怎麼維護規則)
- [如何擴展 Agent](#如何擴展-agent)
- [專案結構](#專案結構)
- [假資料內容](#假資料內容)
- [假資料如何產生](#假資料如何產生)
- [各腳本的功用](#各腳本的功用)

## 第一次使用：給非技術人員的建議流程

如果你不熟悉終端機，建議先使用 VS Code 操作。
VS Code 是工程師常用的編輯器，可以在這裡下載：[https://code.visualstudio.com/download](https://code.visualstudio.com/download)。
它可以把專案檔案和終端機放在同一個畫面，比較不容易迷路。

### 1. 安裝並打開 VS Code

1. 安裝 VS Code。
2. 打開 VS Code。
3. 選擇你想要放專案的資料夾。例如你想把專案放在桌面，就先在 VS Code 打開桌面或桌面上的某個資料夾。
4. 在 VS Code 上方選單打開終端機，或從畫面下方把終端機拉起來。
5. 貼上以下指令，把這個 repo 下載到剛剛選好的資料夾裡：

```bash
gh repo clone PoChaoWang/digital-marketing-agency-agent
```

6. 下載完成後，VS Code 左側會看到一個新的資料夾：

```text
digital-marketing-agency-agent
```

7. 接著在 VS Code 打開這個新下載的專案資料夾，或在終端機輸入：

```bash
cd digital-marketing-agency-agent
```

接下來的指令都要在 `digital-marketing-agency-agent` 這個專案資料夾裡執行。

### 2. 建立 Python 環境並安裝套件

請確認終端機目前在專案根目錄，也就是看得到 `README.md` 和 `requirements.txt` 的位置。

第一次使用時，你可以把下面三行都複製一次貼到終端機裡執行，又或者是分三行依序輸入：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

如果終端機的輸入欄位最前面出現 `(.venv)`，代表 Python 環境已經啟用。
使用`(.venv)`的好處是當你不希望這個專案佔用你的電腦空間時，你把專案全部刪除，放在venv裡的套件也可以一次清除，避免麻煩

### 3. 第一次先產生預設 180 天假資料

第一次使用不建議指定日期，先用預設的 180 天資料即可，所以在終端機輸入：

```bash
python fake-data-script/generate_lululemon_fake_data.py
```

`data`資料夾裡會產生三個檔案：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/ga4_raw.csv
```
這個就是平台的模擬資料

### 4. 合併資料並產生 360.csv

產生 raw data 後，再執行資料合併，一樣在終端機輸：

```bash
python fake-data-script/build_360_csv.py
```

這會產生：

```text
data/360.csv
```
這樣三個平台的模擬資料就被合併完成了，如果你想更改合併邏輯，你可以在`fake-data-script/sql/ads_unified.sql`裡修改SQL

### 5. 開啟 Claude Code、Codex 或 Gemini CLI

完成假資料與 `360.csv` 後，再開啟 Claude Code、Codex 或 Gemini CLI，請 AI agent 執行檢查。

如果你是第一次使用 Claude Code、Codex 或 Gemini CLI，請先確認自己是否已經有對應服務的帳號或訂閱方案，並依照官方文件完成 CLI 安裝與登入。這個 repo 不包含這些 CLI 工具本身。

例如可以輸入：

```text
mq
```

或用自然語言：

```text
請檢查這批行銷資料有沒有品質問題，並輸出報告。
```

## AI Agent 可以做什麼

這個 agent 的工作不是取代行銷判斷，而是把行銷人員的經驗規則變成可重複執行的檢查流程。

你可以請它做：

- 檢查資料品質：必要欄位是否缺失、數值是否合理、clicks 是否超過 impressions、GA4 是否有對應到廣告資料。
- 偵測異常：檢查 `data/360.csv` 中 spend、ROAS、CTR、users、revenue 是否出現不合理波動。
- 檢查命名規則：檢查 campaign、ad group、ad set、ad name 是否符合命名格式。
- 產生 dashboard：根據 `data/360.csv` 建立行銷成效 dashboard，也可以套用 `template/` 裡的 Google Sheet 模板。
- 產出報告：把檢查結果寫成 markdown 報告，放在 `reports/`。
- 轉成更好讀的格式：例如把 markdown 報告整理成 HTML，方便給團隊閱讀。

Agent 預設不會修改原始資料，也不會修改 fake data 產生腳本。它的角色是「讀資料、讀規則、產出檢查報告與建議」。

## 可用指令

在 Claude Code / Codex / Gemini CLI 中，可以直接輸入以下短指令。

```text
mq
```
(marketing quality)

執行資料品質檢查，使用 `data-quality` skill。

```text
ma
```
(marketing anomaly detection)

執行異常偵測，使用 `anomaly-detection` skill。

```text
mn
```
(marketing naming convention)

執行命名規則檢查，使用 `naming-convention` skill。

```text
md
```
(marketing dashboard)

產生行銷 dashboard，使用 `dashboard-generator` skill。沒有指定模板時，agent 會自行決定 dashboard 版型；如果 `template/` 裡有模板，會優先保留模板設計並填入資料。

也可以用自然語言說明，例如：

```text
請檢查這批行銷資料有沒有品質問題，並輸出報告。
```

```text
請找出 360.csv 裡 ROAS 或 spend 異常的 campaign。
```

```text
請檢查 campaign 和 ad group 命名是否符合規則。
```

```text
請根據 360.csv 產生一份行銷 dashboard。
```

注意：某些 CLI 不支援自訂 slash command，所以請輸入 `mq`，不要輸入 `/mq`。

## 報告會輸出到哪裡

Agent 產出的報告會放在：

```text
reports/
```

例如：

```text
reports/data-quality-2026-05-25.md
reports/anomaly-detection-2026-05-25.md
reports/naming-convention-2026-05-25.md
```

報告通常會包含：

- 檢查日期
- 使用的 skill
- 使用的規則檔案
- 檢查資料來源
- 摘要
- 發現問題清單
- 嚴重程度
- 可能原因
- 建議對策
- 需要人工確認的事項

如果你想調整報告格式或內容，可以到對應 skill 的 `rules.md`，修改裡面的「## 報告要求」。

例如資料品質報告的規格在：

```text
.claude/skills/data-quality/references/rules.md
```

目前主要輸出格式是 markdown 檔案。建議在 VS Code 安裝 [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)，方便直接預覽報告。

`reports/` 裡可能也會看到 HTML 檔案。這是另外請 AI 生成的版本，用來測試 HTML 報告的可讀性；不過 HTML 產生時間通常比較久，所以目前仍以 markdown 報告為主。

## 四個 Skill 的功用

### data-quality

位置：

```text
.claude/skills/data-quality/
```

用途：

- 檢查 `data/` 下的 CSV 是否符合基本資料品質標準。
- 適合用來回答「這批資料能不能用」、「有沒有缺欄位」、「數字有沒有明顯錯誤」。

會讀取的規則：

```text
.claude/skills/data-quality/references/rules.md
```

會檢查的資料：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/ga4_raw.csv
data/360.csv
```

範例檢查項目：

- 必要欄位不應為空
- clicks 不應超過 impressions
- spend、revenue、conversions 不應為負數
- spend > 0 時 GA4 users 不應為 0
- ROAS 是否落在合理範圍
- CTR 是否落在合理範圍

### anomaly-detection

位置：

```text
.claude/skills/anomaly-detection/
```

用途：

- 針對 `data/360.csv` 做跨日期、campaign、source、ad type 等維度比較。
- 適合用來回答「哪個 campaign 表現怪怪的」、「今天 spend 是否暴增」、「ROAS 是否連續下滑」。

會讀取的規則：

```text
.claude/skills/anomaly-detection/references/rules.md
```

會檢查的資料：

```text
data/360.csv
```

範例檢查項目：

- spend 單日暴增
- campaign 突然 0 impression
- ROAS 連續下滑
- CTR 突然升高或降低
- clicks 有量但 users 為 0

### naming-convention

位置：

```text
.claude/skills/naming-convention/
```

用途：

- 檢查 campaign、ad group、ad set、ad name 是否符合命名規則。
- 適合用來回答「命名有沒有亂掉」、「新 campaign 是否符合規範」。

會讀取的規則：

```text
.claude/skills/naming-convention/references/rules.md
```

會檢查的資料：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/360.csv
```

範例命名格式：

```text
[市場]_[平台]_[類型]_[漏斗階段]_[產品線]
```

例如：

```text
jp_google_pmax_prospecting_women_yoga
jp_meta_img_retargeting_bags
```

### dashboard-generator

位置：

```text
.claude/skills/dashboard-generator/
```

用途：

- 根據 `data/360.csv` 產生行銷 dashboard。
- 沒有指定模板時，由 agent 自行決定 dashboard 版型。
- 有指定模板時，優先使用 `template/` 裡的 Google Sheet 或 Excel 模板。
- 適合用來回答「請幫我做 dashboard」、「請把 360.csv 做成報表」、「請套用這個模板產生 dashboard」。

會讀取的規則：

```text
.claude/skills/dashboard-generator/references/rules.md
.claude/skills/dashboard-generator/references/template-markers.md
.claude/skills/dashboard-generator/references/report-types.md
```

會使用的資料：

```text
data/360.csv
template/
```

模板維護方式：

- 非技術使用者可以直接維護 Google Sheet 或 Excel 模板。
- 在模板中放入 `{{dashboard_title}}`、`{{roas}}`、`{{daily_trend_chart}}` 這類 placeholder。
- Agent 會優先替換 placeholder，並保留模板原本的顏色、文字與版面。
- 如果模板裡有 `Config` sheet，可以用一般表格設定資料來源、日期欄位、預設天數與主要分析維度。

## 行銷人員該怎麼維護規則

行銷人員主要維護的是各 skill 底下的 `references/rules.md`。

```text
.claude/skills/data-quality/references/rules.md
.claude/skills/anomaly-detection/references/rules.md
.claude/skills/naming-convention/references/rules.md
.claude/skills/dashboard-generator/references/rules.md
```

這些檔案可以用純文字描述業務規則，不需要寫程式。

例如你可以寫：

```text
Meta prospecting CTR 低於 0.3% 時，需要人工確認。
```

```text
ROAS 連續 3 天下滑，標記為 High。
```

```text
campaign name 必須使用小寫英文和底線，不可以有空白。
```

建議維護方式：

- 一次只修改一個規則主題。
- 寫清楚適用對象，例如 Google、Meta、prospecting、retargeting。
- 寫清楚嚴重程度，例如 High、Medium、Low。
- 寫清楚 agent 應該怎麼回報，例如列出 campaign、日期、影響筆數。
- 如果不確定閾值，先寫「需要人工確認」，不要直接寫成阻擋條件。

## 如何擴展 Agent

如果你想新增一種檢查，例如「預算 pacing 檢查」，可以新增一個 skill：

```text
.claude/skills/budget-pacing/
├── SKILL.md
└── references/
    └── rules.md
```

再新增一個短指令：

```text
.claude/commands/mp.md
```

建議每個 skill 只負責一種明確任務，避免一個規則檔混在一起變得難維護。

## 專案結構

```text
digital-marketing-agent/
├── AGENT.md
├── README.md
├── requirements.txt
├── .claude/
│   ├── commands/
│   │   ├── mq.md
│   │   ├── ma.md
│   │   ├── mn.md
│   │   └── md.md
│   └── skills/
│       ├── data-quality/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── rules.md
│       ├── anomaly-detection/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── rules.md
│       ├── naming-convention/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── rules.md
│       └── dashboard-generator/
│           ├── SKILL.md
│           └── references/
│               ├── rules.md
│               ├── template-markers.md
│               └── report-types.md
├── data/
│   ├── google_ads_raw.csv
│   ├── meta_ads_raw.csv
│   ├── ga4_raw.csv
│   └── 360.csv
├── template/
│   ├── README.md
│   └── marketing-dashboard-template.md
├── fake-data-script/
│   ├── README.md
│   ├── generate_lululemon_fake_data.py
│   ├── build_360_csv.py
│   └── sql/
│       └── ads_unified.sql
└── reports/
    └── .gitkeep
```

## 假資料內容

這個專案使用 lululemon Japan 的模擬行銷資料。

### Google Ads raw data

檔案：

```text
data/google_ads_raw.csv
```

內容包含：

- campaign
- ad group
- ad
- impressions
- clicks
- spend
- conversions
- conversion value

模擬的 campaign type：

- PMax
- Shopping
- Display

### Meta Ads raw data

檔案：

```text
data/meta_ads_raw.csv
```

內容包含：

- campaign
- ad set
- ad
- impressions
- clicks
- spend
- conversions
- conversion value

模擬的 ad format：

- Image
- Video
- Collection
- Carousel
- Dynamic retargeting

### GA4 raw data

檔案：

```text
data/ga4_raw.csv
```

內容包含：

- source
- medium
- UTM campaign
- UTM id
- UTM content
- sessions
- users
- new users
- conversions
- revenue

Paid GA4 rows 會對應回 Google Ads 與 Meta Ads：

```text
utm_campaign -> campaign_name
utm_id       -> ad_group 或 ad_set
utm_content  -> ad_name
```

### 360.csv

檔案：

```text
data/360.csv
```

這是合併後的行銷分析資料表，整合：

- Google Ads
- Meta Ads
- GA4

合併邏輯在：

```text
fake-data-script/sql/ads_unified.sql
```

## 假資料如何產生

產生三份 raw data。第一次使用建議不要指定日期，直接使用預設的 180 天資料：

```bash
python fake-data-script/generate_lululemon_fake_data.py
```

輸出：

```text
data/google_ads_raw.csv
data/meta_ads_raw.csv
data/ga4_raw.csv
```

合併成 360.csv：

```bash
python fake-data-script/build_360_csv.py
```

輸出：

```text
data/360.csv
```

## 各腳本的功用

### generate_lululemon_fake_data.py

位置：

```text
fake-data-script/generate_lululemon_fake_data.py
```

用途：

- 產生 Google Ads raw data
- 產生 Meta Ads raw data
- 產生 GA4 raw data

這支腳本模擬的是 API 回傳的乾淨資料，不刻意製造缺失值、格式錯誤或重複列。

### build_360_csv.py

位置：

```text
fake-data-script/build_360_csv.py
```

用途：

- 讀取 `fake-data-script/sql/ads_unified.sql`
- 使用 DuckDB 合併三份 raw CSV
- 輸出 `data/360.csv`

### ads_unified.sql

位置：

```text
fake-data-script/sql/ads_unified.sql
```

用途：

- 統一 Google Ads 與 Meta Ads 欄位
- 用 `UNION ALL` 合併廣告資料
- 聚合 GA4 UTM 資料
- 將 GA4 指標接到廣告資料上
