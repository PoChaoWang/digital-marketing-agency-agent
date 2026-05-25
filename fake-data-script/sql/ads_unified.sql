-- Build data/360.csv from Google Ads, Meta Ads, and GA4 fake raw CSV exports.

WITH google_ads AS (
    SELECT
        CAST(date AS DATE) AS date,
        campaign_name,
        ad_group AS ad_group_name,
        ad_name,
        CAST(impressions AS BIGINT) AS impressions,
        CAST(clicks AS BIGINT) AS clicks,
        CAST(spend AS DOUBLE) AS spend,
        CAST(conversions AS DOUBLE) AS conversions,
        CAST(conversion_value AS DOUBLE) AS revenue,
        'google' AS source,
        CASE
            WHEN LOWER(campaign_name) LIKE '%dynamic%' THEN 'dynamic'
            WHEN LOWER(campaign_name) LIKE '%retargeting%' THEN 'retargeting'
            WHEN LOWER(campaign_name) LIKE '%prospecting%' THEN 'prospecting'
            ELSE 'unknown'
        END AS campaign_type,
        CASE
            WHEN LOWER(campaign_name) LIKE '%pmax%' THEN 'pmax'
            WHEN LOWER(campaign_name) LIKE '%performance%' THEN 'pmax'
            WHEN LOWER(campaign_name) LIKE '%sho%' THEN 'sho'
            WHEN LOWER(campaign_name) LIKE '%shopping%' THEN 'sho'
            WHEN LOWER(campaign_name) LIKE '%gdn%' THEN 'gdn'
            WHEN LOWER(campaign_name) LIKE '%display%' THEN 'gdn'
            ELSE 'unknown'
        END AS ad_type
    FROM read_csv_auto('data/google_ads_raw.csv', header = true)
),
meta_ads AS (
    SELECT
        CAST(date AS DATE) AS date,
        campaign_name,
        ad_set AS ad_group_name,
        ad_name,
        CAST(impressions AS BIGINT) AS impressions,
        CAST(clicks AS BIGINT) AS clicks,
        CAST(spend AS DOUBLE) AS spend,
        CAST(conversions AS DOUBLE) AS conversions,
        CAST(conversion_value AS DOUBLE) AS revenue,
        'meta' AS source,
        CASE
            WHEN LOWER(campaign_name) LIKE '%dynamic%' THEN 'dynamic'
            WHEN LOWER(campaign_name) LIKE '%retargeting%' THEN 'retargeting'
            WHEN LOWER(campaign_name) LIKE '%prospecting%' THEN 'prospecting'
            ELSE 'unknown'
        END AS campaign_type,
        CASE
            WHEN LOWER(ad_set) LIKE '%image%' THEN 'img'
            WHEN LOWER(ad_set) LIKE '%img%' THEN 'img'
            WHEN LOWER(ad_set) LIKE '%video%' THEN 'vid'
            WHEN LOWER(ad_set) LIKE '%vid%' THEN 'vid'
            WHEN LOWER(ad_set) LIKE '%collection%' THEN 'col'
            WHEN LOWER(ad_set) LIKE '%col%' THEN 'col'
            WHEN LOWER(ad_set) LIKE '%carousel%' THEN 'car'
            WHEN LOWER(ad_set) LIKE '%car%' THEN 'car'
            WHEN LOWER(ad_set) LIKE '%dynamic%' THEN 'dynamic'
            ELSE 'unknown'
        END AS ad_type
    FROM read_csv_auto('data/meta_ads_raw.csv', header = true)
),
ads_unified AS (
    SELECT * FROM google_ads
    UNION ALL
    SELECT * FROM meta_ads
),
ga4 AS (
    SELECT
        utm_campaign,
        utm_id,
        utm_content,
        SUM(CAST(users AS BIGINT)) AS users,
        SUM(CAST(new_users AS BIGINT)) AS new_users,
        SUM(CAST(conversions AS DOUBLE)) AS ga4_conversions,
        SUM(CAST(revenue AS DOUBLE)) AS ga4_revenue
    FROM read_csv_auto('data/ga4_raw.csv', header = true)
    WHERE utm_campaign IS NOT NULL
      AND utm_campaign != ''
      AND utm_id IS NOT NULL
      AND utm_id != ''
      AND utm_content IS NOT NULL
      AND utm_content != ''
    GROUP BY
        utm_campaign,
        utm_id,
        utm_content
)
SELECT
    ads_unified.date,
    ads_unified.source,
    ads_unified.campaign_name,
    ads_unified.ad_group_name,
    ads_unified.ad_name,
    ads_unified.impressions,
    ads_unified.clicks,
    ads_unified.spend,
    ads_unified.conversions,
    ads_unified.revenue,
    ads_unified.campaign_type,
    ads_unified.ad_type,
    COALESCE(ga4.users, 0) AS users,
    COALESCE(ga4.new_users, 0) AS new_users,
    COALESCE(ga4.ga4_conversions, 0) AS ga4_conversions,
    COALESCE(ga4.ga4_revenue, 0) AS ga4_revenue
FROM ads_unified
LEFT JOIN ga4
    ON ads_unified.campaign_name = ga4.utm_campaign
   AND ads_unified.ad_group_name = ga4.utm_id
   AND ads_unified.ad_name = ga4.utm_content;
