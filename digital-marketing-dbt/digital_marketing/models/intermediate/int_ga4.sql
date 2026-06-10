with staging as (
    select * from {{ ref('stg_ga4') }}
)

select 
date, 
{{ get_year("date") }} as year, 
{{ get_month("date") }} as month, 
{{ get_week("date") }} as week,
source,
medium,
{{ get_media('campaign_name') }} as media,
campaign_name,
{{ get_channel('campaign_name') }} as channel,
{{ get_campaign_type('campaign_name') }} as campaign_type,
{{ get_product_line('campaign_name') }} AS product_line,
ad_group,
ad_name,
{{ get_ad_format('campaign_name', 'ad_name') }} as ad_format,
{{ get_ad_category('campaign_name', 'ad_name') }} as ad_category,
utm_code,
ga4_sessions,
ga4_users,
ga4_new_users,
ga4_engaged_sessions,
ga4_events,
ga4_key_events,
ga4_conversions,
ga4_revenue,
currency
from staging
