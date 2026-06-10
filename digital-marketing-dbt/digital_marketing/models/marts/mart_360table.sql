with ads_unified as (
    select * from {{ ref('int_google_ads') }}
    union all
    select * from {{ ref('int_google_ppc') }}
    union all
    select * from {{ ref('int_meta_ads') }}
    union all
    select * from {{ ref('int_yahoo_display') }}
    union all
    select * from {{ ref('int_yahoo_ppc') }}
),

ga4 as (
    select 
        date,
        campaign_name,
        ad_group,
        ad_name,
        sum(ga4_sessions) as ga4_sessions,
        sum(ga4_users) as ga4_users,
        sum(ga4_new_users) as ga4_new_users,
        sum(ga4_engaged_sessions) as ga4_engaged_sessions,
        sum(ga4_events) as ga4_events,
        sum(ga4_key_events) as ga4_key_events,
        sum(ga4_conversions) as ga4_conversions,
        sum(ga4_revenue) as ga4_revenue
    from {{ ref('int_ga4') }}
    group by 1, 2, 3, 4
)

select
    a.date,
    a.year,
    a.month,
    a.week,
    a.platform,
    a.account_name,
    a.media,
    a.campaign_name,
    a.channel,
    a.campaign_type,
    a.product_line,
    a.ad_group,
    a.ad_name,
    a.ad_format,
    a.ad_category,
    a.impressions,
    a.clicks,
    a.spend,
    a.currency,
    a.conversions,
    a.conversion_value,
    g.ga4_sessions,
    g.ga4_users,
    g.ga4_new_users,
    g.ga4_engaged_sessions,
    g.ga4_events,
    g.ga4_key_events,
    g.ga4_conversions,
    g.ga4_revenue
from ads_unified a
left join ga4 g
    on a.date = g.date
    and a.campaign_name = g.campaign_name
    and a.ad_group = g.ad_group
    and a.ad_name = g.ad_name
