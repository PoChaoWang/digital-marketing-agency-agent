with source as (
    select * from {{ source('raw_digital_marketing', 'raw_ga4') }}
),

renamed as (
    select
        cast(date as date) as date,
        `utm-source` as source,
        `utm-medium` as medium,
        `utm-campaign` as campaign_name,
        `utm-id` as ad_group,
        `utm-content` as ad_name,
        `utm-code` as utm_code,
        cast(sessions as int64) as ga4_sessions,
        cast(users as int64) as ga4_users,
        cast(`new-users` as int64) as ga4_new_users,
        cast(`engaged-sessions` as int64) as ga4_engaged_sessions,
        cast(events as int64) as ga4_events,
        cast(`key-events` as int64) as ga4_key_events,
        cast(conversions as float64) as ga4_conversions,
        cast(revenue as float64) as ga4_revenue,
        currency
    from source
    where `utm-campaign` != ''
)

select * from renamed
