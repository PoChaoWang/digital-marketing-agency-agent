with source as (
    select * from {{ source('raw_digital_marketing', 'raw_meta_ads') }}
),

renamed as (
    select
        cast(date as date) as date,
        platform,
        `account-name` as account_name,
        `campaign-name` as campaign_name,
        `ad-set` as ad_group,
        `ad-name` as ad_name,
        cast(impressions as int64) as impressions,
        cast(clicks as int64) as clicks,
        cast(spend as float64) as spend,
        currency,
        cast(conversions as float64) as conversions,
        cast(`conversion-value` as float64) as conversion_value
    from source
)

select * from renamed
