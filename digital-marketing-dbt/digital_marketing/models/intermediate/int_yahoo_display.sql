with staging as (
    select * from {{ ref('stg_yahoo_display') }}
)

select 
date, 
{{ get_year("date") }} as year, 
{{ get_month("date") }} as month, 
{{ get_week("date") }} as week,
platform,
account_name,
{{ get_media('campaign_name') }} as media,
campaign_name,
{{ get_channel('campaign_name') }} as channel,
{{ get_campaign_type('campaign_name') }} as campaign_type,
{{ get_product_line('campaign_name') }} AS product_line,
ad_group,
ad_name,
{{ get_ad_format('campaign_name', 'ad_name') }} as ad_format,
{{ get_ad_category('campaign_name', 'ad_name') }} as ad_category,
impressions,
clicks,
spend,
currency,
conversions,
conversion_value
from staging
