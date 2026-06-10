#!/usr/bin/env python3
"""
Generate fake raw Google Ads, Meta Ads, and GA4 CSV data for lululemon Japan.

The paid GA4 rows are generated from the ads rows, so these mappings hold:
- utm_campaign -> campaign_name
- utm_id       -> ad_group for Google Ads, ad_set for Meta Ads
- utm_content  -> ad_name
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


DEFAULT_SEED = 20260525
ACCOUNT_NAME_GOOGLE = "lululemon JP Google Ads"
ACCOUNT_NAME_META = "lululemon JP Meta Ads"
BRAND = "lululemon"
MARKET = "jp"
ACCOUNT_NAME_GOOGLE_PPC = "lululemon JP Google PPC"
ACCOUNT_NAME_YAHOO_PPC = "lululemon JP Yahoo PPC"
ACCOUNT_NAME_YAHOO_DISPLAY = "lululemon JP Yahoo Display"


@dataclass(frozen=True)
class ProductLine:
    slug: str
    landing_page: str
    base_cvr: float
    avg_order_value: int
    gender_weight: float


PRODUCT_LINES = [
    ProductLine("women-yoga", "/ja-jp/c/women/yoga", 0.035, 17800, 1.18),
    ProductLine("women-running", "/ja-jp/c/women/running", 0.028, 18800, 1.12),
    ProductLine("women-training", "/ja-jp/c/women/training", 0.031, 18200, 1.15),
    ProductLine(
        "women-new-arrivals", "/ja-jp/c/women/new-arrivals", 0.027, 19800, 1.08
    ),
    ProductLine("men-running", "/ja-jp/c/men/running", 0.022, 19200, 0.86),
    ProductLine("men-training", "/ja-jp/c/men/training", 0.021, 18800, 0.84),
    ProductLine("bags", "/ja-jp/c/accessories/bags", 0.039, 12800, 1.05),
    ProductLine("accessories", "/ja-jp/c/accessories", 0.033, 7200, 0.98),
]

GOOGLE_TYPES = {
    "pmax": {"label": "performance", "ctr": 0.032, "cpc": 92, "cvr": 1.10},
    "sho": {"label": "shopping", "ctr": 0.026, "cpc": 78, "cvr": 1.20},
    "gdn": {"label": "display", "ctr": 0.007, "cpc": 38, "cvr": 0.52},
}

META_FORMATS = {
    "img": {"label": "Image", "ctr": 0.013, "cpc": 72, "cvr": 0.82},
    "vid": {"label": "Video", "ctr": 0.010, "cpc": 65, "cvr": 0.70},
    "col": {"label": "Collection Ads", "ctr": 0.017, "cpc": 84, "cvr": 0.98},
    "car": {"label": "Carousel Ads", "ctr": 0.016, "cpc": 80, "cvr": 0.92},
}

NON_PAID_SOURCES = [
    ("google", "organic", "organic-search", 0.030),
    ("direct", "(none)", "direct", 0.025),
    ("line", "referral", "line-referral", 0.020),
    ("instagram", "organic-social", "organic-social", 0.018),
    ("newsletter", "email", "crm-email", 0.041),
]


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def date_range(start: date, end: date) -> list[date]:
    if end < start:
        raise ValueError("--end-date must be on or after --start-date")
    days = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)
    return days


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def rounded_jpy(value: float) -> int:
    return int(round(value))


def seasonal_multiplier(day: date) -> tuple[float, float, str]:
    """Return traffic, conversion, and season label multipliers."""
    traffic = 1.0
    conversion = 1.0
    labels = []

    if day.weekday() in (4, 5):  # Friday, Saturday
        traffic *= 1.22
        conversion *= 1.12
        labels.append("fri-sat-lift")
    elif day.weekday() == 6:
        traffic *= 0.94
        conversion *= 0.95

    if day.month == 11 and day.day >= 24:
        traffic *= 1.85
        conversion *= 1.35
        labels.append("black-friday")
    if day.month == 12 and day.day >= 15:
        traffic *= 1.65
        conversion *= 1.22
        labels.append("year-end-sale")
    if day.month == 1 and day.day <= 7:
        traffic *= 1.30
        conversion *= 1.08
        labels.append("new-year")
    if (day.month == 4 and day.day >= 29) or (day.month == 5 and day.day <= 5):
        traffic *= 1.10
        conversion *= 0.74
        labels.append("golden-week-low-intent")

    return traffic, conversion, "|".join(labels) if labels else "normal"


def random_multiplier(rng: random.Random, spread: float = 0.12) -> float:
    return clamp(rng.gauss(1.0, spread), 0.45, 1.8)


def build_utm_url(
    source: str,
    medium: str,
    campaign: str,
    utm_id: str,
    content: str,
    landing_page: str,
) -> str:
    return (
        f"https://www.lululemon.co.jp{landing_page}"
        f"?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}"
        f"&utm_id={utm_id}&utm_content={content}"
    )


def generate_google_ads(
    days: list[date], rng: random.Random
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    funnels = {
        "prospecting": {"traffic": 1.2, "cvr": 0.75},
        "lookalike": {"traffic": 0.85, "cvr": 1.10},
        "retargeting": {"traffic": 0.52, "cvr": 1.85},
    }
    ad_variants = ["benefit", "product", "seasonal"]
    spike_days = set(rng.sample(days, k=min(4, len(days))))
    pause_days = set(rng.sample(days, k=min(3, len(days))))

    for day in days:
        seasonal_traffic, seasonal_cvr, season_label = seasonal_multiplier(day)
        for ad_type, ad_type_cfg in GOOGLE_TYPES.items():
            for funnel, funnel_cfg in funnels.items():
                for product in PRODUCT_LINES:
                    campaign = f"{MARKET}_google_{ad_type}_{funnel}_{product.slug}"
                    ad_group = f"{ad_type}_{funnel}_{product.slug}"
                    for group_idx, variant in enumerate(ad_variants, start=1):
                        ad_name = f"{product.slug}_{variant}_{group_idx}"
                        traffic_base = rng.randint(380, 1250)
                        traffic = (
                            traffic_base
                            * seasonal_traffic
                            * funnel_cfg["traffic"]
                            * product.gender_weight
                        )
                        if day in spike_days:
                            traffic *= rng.uniform(2.2, 3.8)
                        if day in pause_days and rng.random() < 0.12:
                            traffic *= rng.uniform(0.0, 0.05)
                        ctr = ad_type_cfg["ctr"] * random_multiplier(rng, 0.18)
                        cpc = ad_type_cfg["cpc"] * random_multiplier(rng, 0.16)
                        impressions = max(0, int(traffic))
                        clicks = max(0, int(impressions * ctr))
                        spend = rounded_jpy(clicks * cpc)
                        cvr = (
                            product.base_cvr
                            * ad_type_cfg["cvr"]
                            * funnel_cfg["cvr"]
                            * seasonal_cvr
                        )
                        conversions = max(0, int(round(clicks * cvr * random_multiplier(rng, 0.22))))
                        conversion_value = rounded_jpy(conversions * product.avg_order_value * random_multiplier(rng, 0.18))
                        rows.append({
                            "date": day.isoformat(),
                            "platform": "google-ads",
                            "account-name": ACCOUNT_NAME_GOOGLE,
                            "campaign-name": campaign,
                            "ad-group": ad_group,
                            "ad-name": ad_name,
                            "campaign-type": ad_type,
                            "campaign-type-label": ad_type_cfg["label"],
                            "funnel": funnel,
                            "product-line": product.slug,
                            "season-label": season_label,
                            "impressions": impressions,
                            "clicks": clicks,
                            "spend": spend,
                            "currency": "JPY",
                            "conversions": conversions,
                            "conversion-value": conversion_value,
                        })
    return rows


def generate_meta_ads(days: list[date], rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    funnels = {
        "prospecting": {"traffic": 1.15, "cvr": 0.72},
        "lookalike": {"traffic": 0.90, "cvr": 1.05},
        "retargeting": {"traffic": 0.58, "cvr": 1.70},
    }
    ad_variants = ["lifestyle", "product", "offer"]
    spike_days = set(rng.sample(days, k=min(4, len(days))))
    pause_days = set(rng.sample(days, k=min(3, len(days))))

    for day in days:
        seasonal_traffic, seasonal_cvr, season_label = seasonal_multiplier(day)
        for funnel, funnel_cfg in funnels.items():
            for fmt, fmt_cfg in META_FORMATS.items():
                for product in PRODUCT_LINES:
                    campaign = f"{MARKET}_meta_{funnel}_{product.slug}"
                    ad_set = f"{funnel}_{product.slug}"
                    for variant in ad_variants:
                        ad_name = f"{product.slug}_{fmt}_{variant}"
                        traffic_base = rng.randint(520, 1450)
                        traffic = (traffic_base * seasonal_traffic * funnel_cfg["traffic"] * product.gender_weight)
                        if day in spike_days:
                            traffic *= rng.uniform(2.0, 3.5)
                        if day in pause_days and rng.random() < 0.10:
                            traffic *= rng.uniform(0.0, 0.04)
                        ctr = fmt_cfg["ctr"] * random_multiplier(rng, 0.20)
                        cpc = fmt_cfg["cpc"] * random_multiplier(rng, 0.18)
                        impressions = max(0, int(traffic))
                        clicks = max(0, int(impressions * ctr))
                        spend = rounded_jpy(clicks * cpc)
                        cvr = (product.base_cvr * fmt_cfg["cvr"] * funnel_cfg["cvr"] * seasonal_cvr)
                        conversions = max(0, int(round(clicks * cvr * random_multiplier(rng, 0.24))))
                        conversion_value = rounded_jpy(conversions * product.avg_order_value * random_multiplier(rng, 0.20))
                        rows.append({
                            "date": day.isoformat(),
                            "platform": "meta-ads",
                            "account-name": ACCOUNT_NAME_META,
                            "campaign-name": campaign,
                            "ad-set": ad_set,
                            "ad-name": ad_name,
                            "ad-format": fmt,
                            "ad-format-label": fmt_cfg["label"],
                            "funnel": funnel,
                            "product-line": product.slug,
                            "season-label": season_label,
                            "impressions": impressions,
                            "clicks": clicks,
                            "spend": spend,
                            "currency": "JPY",
                            "conversions": conversions,
                            "conversion-value": conversion_value,
                        })
        for product in PRODUCT_LINES:
            campaign = f"{MARKET}_meta_dynamic_retargeting_{product.slug}"
            ad_set = f"dynamic_retargeting_{product.slug}"
            for variant in ["catalog", "viewed_product"]:
                ad_name = f"{product.slug}_dynamic_{variant}"
                traffic_base = rng.randint(180, 680)
                traffic = traffic_base * seasonal_traffic * product.gender_weight
                ctr = 0.021 * random_multiplier(rng, 0.20)
                cpc = 88 * random_multiplier(rng, 0.18)
                impressions = max(0, int(traffic))
                clicks = max(0, int(impressions * ctr))
                spend = rounded_jpy(clicks * cpc)
                cvr = product.base_cvr * 1.95 * seasonal_cvr
                conversions = max(
                    0, int(round(clicks * cvr * random_multiplier(rng, 0.22)))
                )
                conversion_value = rounded_jpy(
                    conversions * product.avg_order_value * random_multiplier(rng, 0.18)
                )
                rows.append(
                    {
                        "date": day.isoformat(),
                        "platform": "meta-ads",
                        "account-name": ACCOUNT_NAME_META,
                        "campaign-name": campaign,
                        "ad-set": ad_set,
                        "ad-name": ad_name,
                        "ad-format": "dynamic",
                        "ad-format-label": "Dynamic Product Ads",
                        "funnel": "retargeting",
                        "product-line": product.slug,
                        "season-label": season_label,
                        "impressions": impressions,
                        "clicks": clicks,
                        "spend": spend,
                        "currency": "JPY",
                        "conversions": conversions,
                        "conversion-value": conversion_value,
                    }
                )

    return rows


def generate_google_ppc(
    days: list[date], rng: random.Random
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    ad_variants = ["benefit", "product", "seasonal"]
    match_types = ["exact", "phrase", "broad"]

    # Numerical logic based on prompt table
    ppc_types = {
        "brand": {"imp-base": 1200, "ctr": 0.10, "cpc": 55, "cvr-mult": 1.4},
        "non-brand": {"imp-base": 800, "ctr": 0.055, "cpc": 160, "cvr-mult": 1.0},
    }
    match_logic = {
        "exact": {"imp-mult": 1.0, "ctr-mult": 1.4, "cpc-mult": 0.8, "cvr-mult": 1.4},
        "phrase": {"imp-mult": 1.5, "ctr-mult": 1.0, "cpc-mult": 1.0, "cvr-mult": 1.0},
        "broad": {"imp-mult": 2.5, "ctr-mult": 0.6, "cpc-mult": 1.3, "cvr-mult": 0.7},
    }
    for day in days:
        seasonal_traffic, seasonal_cvr, season_label = seasonal_multiplier(day)
        for kw_type, cfg in ppc_types.items():
            for product in PRODUCT_LINES:
                # Subtypes: brand only has brand_name, non-brand has products and competitor
                if kw_type == "brand":
                    subtypes = ["brand-name"]
                else:
                    subtypes = [product.slug, "competitor"]

                for campaign_subtype in subtypes:
                    campaign_name = f"jp_google_ppc_{kw_type}_{campaign_subtype}"
                    for match_type in match_types:
                        m_cfg = match_logic[match_type]
                        ad_group = f"{campaign_name}_{match_type}"
                        for group_idx, variant in enumerate(ad_variants, start=1):
                            ad_name = f"{product.slug}_{variant}_{group_idx}"

                            # Math logic
                            traffic = (
                                cfg["imp-base"]
                                * m_cfg["imp-mult"]
                                * seasonal_traffic
                                * product.gender_weight
                                * random_multiplier(rng, 0.15)
                            )
                            impressions = max(0, int(traffic))

                            ctr = (
                                cfg["ctr"]
                                * m_cfg["ctr-mult"]
                                * random_multiplier(rng, 0.12)
                            )
                            clicks = max(0, int(impressions * ctr))

                            cpc = (
                                cfg["cpc"]
                                * m_cfg["cpc-mult"]
                                * random_multiplier(rng, 0.10)
                            )
                            spend = rounded_jpy(clicks * cpc)

                            cvr = (
                                product.base_cvr
                                * cfg["cvr-mult"]
                                * m_cfg["cvr-mult"]
                                * seasonal_cvr
                                * random_multiplier(rng, 0.18)
                            )
                            conversions = max(0, int(round(clicks * cvr)))
                            conversion_value = rounded_jpy(
                                conversions
                                * product.avg_order_value
                                * random_multiplier(rng, 0.15)
                            )

                            rows.append(
                                {
                                    "date": day.isoformat(),
                                    "platform": "google-ppc",
                                    "account-name": ACCOUNT_NAME_GOOGLE_PPC,
                                    "campaign-name": campaign_name,
                                    "ad-group": ad_group,
                                    "ad-name": ad_name,
                                    "keyword-type": kw_type,
                                    "match-type": match_type,
                                    "campaign-subtype": campaign_subtype,
                                    "product-line": product.slug,
                                    "season-label": season_label,
                                    "impressions": impressions,
                                    "clicks": clicks,
                                    "spend": spend,
                                    "currency": "JPY",
                                    "conversions": conversions,
                                    "conversion-value": conversion_value,
                                    "funnel": "prospecting",
                                }
                            )
    return rows


def generate_yahoo_ppc(days: list[date], rng: random.Random) -> list[dict[str, object]]:
    # Logic identical to google_ppc but with different platform/account and lower scale
    rows: list[dict[str, object]] = []
    ad_variants = ["benefit", "product", "seasonal"]
    match_types = ["exact", "phrase", "broad"]

    # Numerical logic with Yahoo scale adjustments
    ppc_types = {
        "brand": {
            "imp-base": 1200 * 0.62,
            "ctr": 0.10,
            "cpc": 55 * 0.85,
            "cvr-mult": 1.4,
        },
        "non-brand": {
            "imp-base": 800 * 0.62,
            "ctr": 0.055,
            "cpc": 160 * 0.85,
            "cvr-mult": 1.0,
        },
    }
    match_logic = {
        "exact": {"imp-mult": 1.0, "ctr-mult": 1.4, "cpc-mult": 0.8, "cvr-mult": 1.4},
        "phrase": {"imp-mult": 1.5, "ctr-mult": 1.0, "cpc-mult": 1.0, "cvr-mult": 1.0},
        "broad": {"imp-mult": 2.5, "ctr-mult": 0.6, "cpc-mult": 1.3, "cvr-mult": 0.7},
    }

    for day in days:
        seasonal_traffic, seasonal_cvr, season_label = seasonal_multiplier(day)
        for kw_type, cfg in ppc_types.items():
            for product in PRODUCT_LINES:
                # Subtypes: brand only has brand_name, non-brand has products and competitor
                if kw_type == "brand":
                    subtypes = ["brand-name"]
                else:
                    subtypes = [product.slug, "competitor"]

                for campaign_subtype in subtypes:
                    campaign_name = f"jp_yahoo_ppc_{kw_type}_{campaign_subtype}"
                    for match_type in match_types:
                        m_cfg = match_logic[match_type]
                        ad_group = f"{campaign_name}_{match_type}"
                        for group_idx, variant in enumerate(ad_variants, start=1):
                            ad_name = f"{product.slug}_{variant}_{group_idx}"

                            traffic = (
                                cfg["imp-base"]
                                * m_cfg["imp-mult"]
                                * seasonal_traffic
                                * product.gender_weight
                                * random_multiplier(rng, 0.15)
                            )
                            impressions = max(0, int(traffic))
                            ctr = (
                                cfg["ctr"]
                                * m_cfg["ctr-mult"]
                                * random_multiplier(rng, 0.12)
                            )
                            clicks = max(0, int(impressions * ctr))
                            cpc = (
                                cfg["cpc"]
                                * m_cfg["cpc-mult"]
                                * random_multiplier(rng, 0.10)
                            )
                            spend = rounded_jpy(clicks * cpc)
                            cvr = (
                                product.base_cvr
                                * cfg["cvr-mult"]
                                * m_cfg["cvr-mult"]
                                * seasonal_cvr
                                * random_multiplier(rng, 0.18)
                            )
                            conversions = max(0, int(round(clicks * cvr)))
                            conversion_value = rounded_jpy(
                                conversions
                                * product.avg_order_value
                                * random_multiplier(rng, 0.15)
                            )

                            rows.append(
                                {
                                    "date": day.isoformat(),
                                    "platform": "yahoo-ppc",
                                    "account-name": ACCOUNT_NAME_YAHOO_PPC,
                                    "campaign-name": campaign_name,
                                    "ad-group": ad_group,
                                    "ad-name": ad_name,
                                    "keyword-type": kw_type,
                                    "match-type": match_type,
                                    "campaign-subtype": campaign_subtype,
                                    "product-line": product.slug,
                                    "season-label": season_label,
                                    "impressions": impressions,
                                    "clicks": clicks,
                                    "spend": spend,
                                    "currency": "JPY",
                                    "conversions": conversions,
                                    "conversion-value": conversion_value,
                                    "funnel": "prospecting",
                                }
                            )
    return rows


def generate_yahoo_display(
    days: list[date], rng: random.Random
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    funnels = {
        "prospecting": {"traffic": 1.2, "cvr": 0.75},
        "lookalike": {"traffic": 0.85, "cvr": 1.10},
        "retargeting": {"traffic": 0.52, "cvr": 1.85},
    }
    display_cfg = {"label": "display", "ctr": 0.007, "cpc": 38, "cvr": 0.52}
    ad_variants = ["benefit", "product", "seasonal"]

    for day in days:
        seasonal_traffic, seasonal_cvr, season_label = seasonal_multiplier(day)
        for funnel, funnel_cfg in funnels.items():
            for product in PRODUCT_LINES:
                campaign = f"jp_yahoo_display_{funnel}_{product.slug}"
                ad_group = f"yahoo_display_{funnel}_{product.slug}"
                for group_idx, variant in enumerate(ad_variants, start=1):
                    ad_name = f"{product.slug}_{variant}_{group_idx}"
                    traffic_base = rng.randint(400, 1100)
                    traffic = (traffic_base * seasonal_traffic * funnel_cfg["traffic"] * product.gender_weight)
                    ctr = display_cfg["ctr"] * random_multiplier(rng, 0.18)
                    cpc = display_cfg["cpc"] * random_multiplier(rng, 0.16)
                    impressions = max(0, int(traffic))
                    clicks = max(0, int(impressions * ctr))
                    spend = rounded_jpy(clicks * cpc)
                    cvr = (product.base_cvr * display_cfg["cvr"] * funnel_cfg["cvr"] * seasonal_cvr)
                    conversions = max(0, int(round(clicks * cvr * random_multiplier(rng, 0.22))))
                    conversion_value = rounded_jpy(conversions * product.avg_order_value * random_multiplier(rng, 0.18))
                    rows.append({
                        "date": day.isoformat(),
                        "platform": "yahoo-display",
                        "account-name": ACCOUNT_NAME_YAHOO_DISPLAY,
                        "campaign-name": campaign,
                        "ad-group": ad_group,
                        "ad-name": ad_name,
                        "campaign-type": "display",
                        "campaign-type-label": "Yahoo Display",
                        "funnel": funnel,
                        "product-line": product.slug,
                        "season-label": season_label,
                        "impressions": impressions,
                        "clicks": clicks,
                        "spend": spend,
                        "currency": "JPY",
                        "conversions": conversions,
                        "conversion-value": conversion_value,
                        "ad-format": "display",
                        "ad-format-label": "Yahoo Display",
                    })
    return rows


def paid_ga4_from_ads(
    rows: list[dict[str, object]],
    rng: random.Random,
    platform: str,
    id_field: str,
    source: str,
    medium: str,
) -> list[dict[str, object]]:
    ga4_rows: list[dict[str, object]] = []

    # Mapping for Google Ads medium
    google_medium_map = {"gdn": "display", "pmax": "pmax", "sho": "shopping"}

    for row in rows:
        campaign = str(row["campaign-name"])
        utm_id = str(row[id_field])
        content = str(row["ad-name"])
        if not campaign or not utm_id or not content:
            continue

        # Determine medium
        current_medium = medium
        if source == "google":
            ctype = str(row.get("campaign-type", ""))
            current_medium = google_medium_map.get(ctype, medium)

        clicks = int(row["clicks"])
        if clicks <= 0:
            continue

        day = parse_date(str(row["date"]))
        tracking_rate = rng.uniform(0.76, 0.94)
        sessions = max(1, int(clicks * tracking_rate * random_multiplier(rng, 0.08)))
        users = max(1, int(sessions * rng.uniform(0.72, 0.96)))
        new_users = max(
            0,
            int(
                users
                * (0.74 if row["funnel"] == "prospecting" else 0.28)
                * random_multiplier(rng, 0.10)
            ),
        )
        engaged_sessions = max(0, int(sessions * rng.uniform(0.48, 0.76)))
        conversions = max(0, int(int(row["conversions"]) * rng.uniform(0.70, 1.04)))
        revenue = rounded_jpy(int(row["conversion-value"]) * rng.uniform(0.72, 1.05)) if conversions > 0 else 0
        event_count = sessions * rng.randint(3, 8) + conversions * rng.randint(2, 5)

        product = next(
            (p for p in PRODUCT_LINES if p.slug == row["product-line"]),
            PRODUCT_LINES[0],
        )
        landing_page = product.landing_page
        utm_code = build_utm_url(
            source, current_medium, campaign, utm_id, content, landing_page
        )

        ga4_rows.append(
            {
                "date": row["date"],
                "source": source,
                "medium": current_medium,
                "campaign": campaign,
                "utm-source": source,
                "utm-medium": current_medium,
                "utm-campaign": campaign,
                "utm-id": utm_id,
                "utm-content": content,
                "utm-code": utm_code,
                "sessions": sessions,
                "users": users,
                "new-users": new_users,
                "engaged-sessions": engaged_sessions,
                "events": event_count,
                "key-events": conversions,
                "conversions": conversions,
                "revenue": revenue,
                "currency": "JPY",
                "landing-page": landing_page,
                "page-path": landing_page,
                "platform-source": platform,
            }
        )

    return ga4_rows


def generate_non_paid_ga4(
    days: list[date], rng: random.Random
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for day in days:
        seasonal_traffic, seasonal_cvr, season_label = seasonal_multiplier(day)
        for source, medium, campaign, cvr in NON_PAID_SOURCES:
            for product in PRODUCT_LINES:
                sessions = int(
                    rng.randint(80, 480)
                    * seasonal_traffic
                    * product.gender_weight
                    * random_multiplier(rng, 0.18)
                )
                users = max(1, int(sessions * rng.uniform(0.70, 0.92)))
                new_users = max(0, int(users * rng.uniform(0.38, 0.74)))
                engaged_sessions = max(0, int(sessions * rng.uniform(0.44, 0.72)))
                conversions = max(
                    0,
                    int(
                        round(
                            sessions
                            * cvr
                            * product.gender_weight
                            * seasonal_cvr
                            * random_multiplier(rng, 0.24)
                        )
                    ),
                )
                revenue = rounded_jpy(
                    conversions * product.avg_order_value * random_multiplier(rng, 0.22)
                )
                landing_page = product.landing_page
                rows.append(
                    {
                        "date": day.isoformat(),
                        "source": source,
                        "medium": medium,
                        "campaign": campaign,
                        "utm-source": "",
                        "utm-medium": "",
                        "utm-campaign": "",
                        "utm-id": "",
                        "utm-content": "",
                        "utm-code": "",
                        "sessions": sessions,
                        "users": users,
                        "new-users": new_users,
                        "engaged-sessions": engaged_sessions,
                        "events": sessions * rng.randint(3, 7)
                        + conversions * rng.randint(1, 4),
                        "key-events": conversions,
                        "conversions": conversions,
                        "revenue": revenue,
                        "currency": "JPY",
                        "landing-page": landing_page,
                        "page-path": landing_page,
                        "platform-source": "non-paid",
                        "season-label": season_label,
                    }
                )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(
        rows, key=lambda row: tuple(str(row.get(key, "")) for key in fieldnames[:6])
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate lululemon Japan fake raw marketing data."
    )
    parser.add_argument(
        "--start-date",
        help="Start date in YYYY-MM-DD. Defaults to end-date minus 179 days.",
    )
    parser.add_argument(
        "--end-date", default=date.today().isoformat(), help="End date in YYYY-MM-DD."
    )
    parser.add_argument(
        "--output-dir", default="data", help="Directory for generated CSV files."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Random seed for reproducible output.",
    )
    args = parser.parse_args()

    end = parse_date(args.end_date)
    start = (
        parse_date(args.start_date) if args.start_date else end - timedelta(days=179)
    )
    days = date_range(start, end)
    rng = random.Random(args.seed)

    google_rows = generate_google_ads(days, rng)
    meta_rows = generate_meta_ads(days, rng)
    google_ppc_rows = generate_google_ppc(days, rng)
    yahoo_ppc_rows = generate_yahoo_ppc(days, rng)
    yahoo_display_rows = generate_yahoo_display(days, rng)

    ga4_rows = []
    ga4_rows.extend(
        paid_ga4_from_ads(google_rows, rng, "google-ads", "ad-group", "google", "cpc")
    )
    ga4_rows.extend(
        paid_ga4_from_ads(meta_rows, rng, "meta-ads", "ad-set", "meta", "paid-social")
    )
    ga4_rows.extend(
        paid_ga4_from_ads(
            google_ppc_rows, rng, "google-ppc", "ad-group", "google", "ppc"
        )
    )
    ga4_rows.extend(
        paid_ga4_from_ads(yahoo_ppc_rows, rng, "yahoo-ppc", "ad-group", "yahoo", "ppc")
    )
    ga4_rows.extend(
        paid_ga4_from_ads(
            yahoo_display_rows, rng, "yahoo-display", "ad-group", "yahoo", "display"
        )
    )
    ga4_rows.extend(generate_non_paid_ga4(days, rng))

    output_dir = Path(args.output_dir)
    google_fields = [
        "date",
        "platform",
        "account-name",
        "campaign-name",
        "ad-group",
        "ad-name",
        "campaign-type",
        "campaign-type-label",
        "funnel",
        "product-line",
        "season-label",
        "impressions",
        "clicks",
        "spend",
        "currency",
        "conversions",
        "conversion-value",
    ]
    meta_fields = [
        "date",
        "platform",
        "account-name",
        "campaign-name",
        "ad-set",
        "ad-name",
        "ad-format",
        "ad-format-label",
        "funnel",
        "product-line",
        "season-label",
        "impressions",
        "clicks",
        "spend",
        "currency",
        "conversions",
        "conversion-value",
    ]
    google_ppc_fields = [
        "date",
        "platform",
        "account-name",
        "campaign-name",
        "ad-group",
        "ad-name",
        "keyword-type",
        "match-type",
        "campaign-subtype",
        "product-line",
        "season-label",
        "impressions",
        "clicks",
        "spend",
        "currency",
        "conversions",
        "conversion-value",
    ]
    yahoo_ppc_fields = google_ppc_fields
    yahoo_display_fields = google_fields + ["ad-format", "ad-format-label"]

    ga4_fields = [
        "date",
        "source",
        "medium",
        "campaign",
        "utm-source",
        "utm-medium",
        "utm-campaign",
        "utm-id",
        "utm-content",
        "utm-code",
        "sessions",
        "users",
        "new-users",
        "engaged-sessions",
        "events",
        "key-events",
        "conversions",
        "revenue",
        "currency",
        "landing-page",
        "page-path",
        "platform-source",
        "season-label",
    ]

    write_csv(output_dir / "google_ads_raw.csv", google_rows, google_fields)
    write_csv(output_dir / "meta_ads_raw.csv", meta_rows, meta_fields)
    write_csv(output_dir / "google_ppc_raw.csv", google_ppc_rows, google_ppc_fields)
    write_csv(output_dir / "yahoo_ppc_raw.csv", yahoo_ppc_rows, yahoo_ppc_fields)
    write_csv(
        output_dir / "yahoo_display_raw.csv", yahoo_display_rows, yahoo_display_fields
    )
    write_csv(output_dir / "ga4_raw.csv", ga4_rows, ga4_fields)

    print(f"Generated {len(google_rows):,} Google Ads rows")
    print(f"Generated {len(meta_rows):,} Meta Ads rows")
    print(f"Generated {len(google_ppc_rows):,} Google PPC rows")
    print(f"Generated {len(yahoo_ppc_rows):,} Yahoo PPC rows")
    print(f"Generated {len(yahoo_display_rows):,} Yahoo Display rows")
    print(f"Generated {len(ga4_rows):,} GA4 rows")
    print(f"Date range: {start.isoformat()} to {end.isoformat()}")
    print(f"Output directory: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
