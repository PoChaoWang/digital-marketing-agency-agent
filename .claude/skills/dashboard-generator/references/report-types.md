# Dashboard Report Types

當使用者沒有指定模板時，agent 可依照需求選擇最適合的 dashboard 類型。

## Executive Overview

適合回答：

- 整體行銷表現如何？
- 這段期間 spend、revenue、ROAS 是否健康？
- 哪些 channel 或 campaign 最值得注意？

預設內容：

- KPI summary
- Daily spend and revenue trend
- Channel performance
- Top campaigns
- Anomaly summary

## Channel Comparison

適合回答：

- Google 和 Meta 哪個表現較好？
- 不同 source 的 ROAS、CPA、CTR 差異如何？

預設內容：

- KPI by source
- Spend share by source
- ROAS by source
- Channel performance table

## Campaign Deep Dive

適合回答：

- 哪些 campaign 表現最好或最差？
- campaign 的 spend、revenue、ROAS、CTR 排名如何？

預設內容：

- Campaign performance table
- Top 10 campaigns by revenue
- Bottom 10 campaigns by ROAS
- Campaign anomaly notes

## Anomaly Monitoring

適合回答：

- 哪些數字怪怪的？
- spend 暴增但 revenue 沒有跟上嗎？
- clicks 有量但 users 或 conversions 異常嗎？

預設內容：

- High risk summary
- Spend / revenue daily trend
- ROAS risk table
- Campaigns requiring manual review

## Template-Based Dashboard

適合情境：

- 使用者已經有固定報表格式。
- 使用者希望維持品牌樣式、顏色、文字與區塊位置。
- 使用者把模板放在 `template/` 或提供 Google Sheet 模板連結。

預設行為：

- 先讀模板標記。
- 再讀 `Config` sheet 或設定表。
- 最後才用 agent 自行判斷補齊缺少的表格或圖表。
