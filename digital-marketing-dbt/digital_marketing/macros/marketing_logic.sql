{% macro get_media(campaign_name) %}
case
    when lower({{ campaign_name }}) like '%yahoo%' then 'Yahoo'
    when lower({{ campaign_name }}) like '%google%' then 'Google'
    when lower({{ campaign_name }}) like '%meta%' then 'Meta'
end
{% endmacro %}

{% macro get_channel(campaign_name) %}
case
    when lower({{ campaign_name }}) like '%gdn%' then 'GDN'
    when lower({{ campaign_name }}) like '%pmax%' then 'PerformanceMax'
    when lower({{ campaign_name }}) like '%sho%' then 'Shopping'
    when lower({{ campaign_name }}) like '%google%' and lower({{ campaign_name }}) like '%ppc%' then 'Google PPC'
    when lower({{ campaign_name }}) like '%yahoo%' and lower({{ campaign_name }}) like '%ppc%' then 'Yahoo PPC'
    when lower({{ campaign_name }}) like '%yahoo_display%' then 'YDA'
    when lower({{ campaign_name }}) like '%meta%' then 'Meta'
end
{% endmacro %}

{% macro get_campaign_type(campaign_name) %}
case
    when lower({{ campaign_name }}) like '%dynamic%' and lower({{ campaign_name }}) like '%retargeting%' then 'Dynamic'
    when lower({{ campaign_name }}) like '%prospecting%' then 'Prospecting'
    when lower({{ campaign_name }}) like '%retargeting%' then 'Retargeting'
    when lower({{ campaign_name }}) like '%lookalike%' then 'Lookalike'
    when lower({{ campaign_name }}) like '%_brand_%' then 'Brand'
    when lower({{ campaign_name }}) like '%_non-brand_%' then 'Non-Brand'
end
{% endmacro %}

{% macro get_ad_format(campaign_name, ad_name) %}
case 
    when lower({{ campaign_name }}) like '%meta%' and lower({{ ad_name }}) like '%col_%' then 'Collection Ads'
    when lower({{ campaign_name }}) like '%meta%' and lower({{ ad_name }}) like '%img_%' then 'Single Image Ads'
    when lower({{ campaign_name }}) like '%meta%' and lower({{ ad_name }}) like '%vid_%' then 'Video Ads'
    when lower({{ campaign_name }}) like '%meta%' and lower({{ ad_name }}) like '%car_%' then 'Carousel Ads'
    when lower({{ campaign_name }}) like '%dynamic%' then 'Dynamic Ads'
    else ''
end
{% endmacro %}

{% macro get_ad_category(campaign_name, ad_name) %}
case
    when lower({{ campaign_name }}) like '%meta%' then SPLIT({{ ad_name }}, '_')[SAFE_OFFSET(ARRAY_LENGTH(SPLIT({{ ad_name }}, '_')) - 1)]
    else SPLIT({{ ad_name }}, '_')[SAFE_OFFSET(ARRAY_LENGTH(SPLIT({{ ad_name }}, '_')) - 2)] || SPLIT({{ ad_name }}, '_')[SAFE_OFFSET(ARRAY_LENGTH(SPLIT({{ ad_name }}, '_')) - 1)]
end
{% endmacro %}

{% macro get_product_line(campaign_name) %}
SPLIT({{ campaign_name }}, '_')[SAFE_OFFSET(ARRAY_LENGTH(SPLIT({{ campaign_name }}, '_')) - 1)]
{% endmacro %}
