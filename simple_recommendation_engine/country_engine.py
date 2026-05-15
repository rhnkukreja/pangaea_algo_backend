from weights_config import compute_country_weights, winsorize

COUNTRIES = {
    "Greece": {
        "region": "Europe",
        "citizenship_available": True,
        "golden_visa_available": True,
        "dtaa_india": True,
        "foreign_freehold_allowed": True,
        "min_program_investment_usd": 250000,
        "scores": {
            "political_stability_index": 5.68,
            "corruption_perception_index": 5.0,
            "currency_volatility": 5.2,
            "interest_rate_direction": 6.88,
            "foreign_buyer_market_share": 4.25,
            "property_taxation_for_foreigners": 4.0,
        },
        "raw_values": {
            "political_stability_index_raw": 0.34,
            "corruption_perception_index_raw": 50,
            "currency_volatility_pct": 7.2,
            "interest_rate_direction_pp": -0.75,
            "foreign_buyer_market_share_pct": 17.0,
            "tax_summary": "ENFIA 0.1-1.2%, rental tax 15-45%, transaction 3%, exit 15%",
        },
    },
    "Portugal": {
        "region": "Europe",
        "citizenship_available": True,
        "golden_visa_available": True,
        "dtaa_india": True,
        "foreign_freehold_allowed": True,
        "min_program_investment_usd": 250000,
        "scores": {
            "political_stability_index": 6.22,
            "corruption_perception_index": 5.6,
            "currency_volatility": 5.2,
            "interest_rate_direction": 6.88,
            "foreign_buyer_market_share": 5.0,
            "property_taxation_for_foreigners": 5.0,
        },
        "raw_values": {
            "political_stability_index_raw": 0.61,
            "corruption_perception_index_raw": 56,
            "currency_volatility_pct": 7.2,
            "interest_rate_direction_pp": -0.75,
            "foreign_buyer_market_share_pct": 20.0,
            "tax_summary": "Holding 0.3-0.8%, rental tax 28%, transaction 6-7.5%, exit 28%",
        },
    },
    "Thailand": {
        "region": "Asia",
        "citizenship_available": False,
        "golden_visa_available": True,
        "dtaa_india": True,
        "foreign_freehold_allowed": False,
        "min_program_investment_usd": 100000,
        "scores": {
            "political_stability_index": 4.64,
            "corruption_perception_index": 3.3,
            "currency_volatility": 3.47,
            "interest_rate_direction": 6.25,
            "foreign_buyer_market_share": 2.25,
            "property_taxation_for_foreigners": 6.0,
        },
        "raw_values": {
            "political_stability_index_raw": -0.18,
            "corruption_perception_index_raw": 33,
            "currency_volatility_pct": 9.8,
            "interest_rate_direction_pp": -0.5,
            "foreign_buyer_market_share_pct": 9.0,
            "tax_summary": "Holding 0.02-0.3%, rental up to 35%, transaction 2-6%",
        },
    },
    "UAE": {
        "region": "Middle East",
        "citizenship_available": False,
        "golden_visa_available": True,
        "dtaa_india": True,
        "foreign_freehold_allowed": True,
        "min_program_investment_usd": 545000,
        "scores": {
            "political_stability_index": 6.36,
            "corruption_perception_index": 6.9,
            "currency_volatility": 9.8,
            "interest_rate_direction": 5.0,
            "foreign_buyer_market_share": 10.0,
            "property_taxation_for_foreigners": 10.0,
        },
        "raw_values": {
            "political_stability_index_raw": 0.68,
            "corruption_perception_index_raw": 69,
            "currency_volatility_pct": 0.3,
            "interest_rate_direction_pp": 0.0,
            "foreign_buyer_market_share_pct": 40.0,
            "tax_summary": "0% holding, 0% rental, 4% transfer fee, 0% exit",
        },
    },
}


def apply_country_hard_filters(answers):
    """Apply Q2 (visa), Q3 (citizenship), Q4 (budget), Q6 (ownership type) as hard filters."""
    surviving = []
    eliminated = []

    for name, data in COUNTRIES.items():
        if answers.get("citizenship_required") == "yes" and not data["citizenship_available"]:
            eliminated.append({
                "country": name,
                "reason": "Does not offer Citizenship by Investment",
            })
            continue

        if answers.get("visa_required") == "mandatory" and not data["golden_visa_available"]:
            eliminated.append({
                "country": name,
                "reason": "Does not offer Golden Visa program",
            })
            continue

        ownership_pref = answers.get("ownership_structure", "any")
        freehold_allowed = data.get("foreign_freehold_allowed", True)
        if ownership_pref == "freehold_only" and not freehold_allowed:
            eliminated.append({
                "country": name,
                "reason": (
                    f"Investor requires freehold ownership; {name} does not permit "
                    f"foreign freehold (foreign_freehold_allowed: False) — "
                    f"only leasehold structures available to foreign buyers"
                ),
            })
            continue

        budget = answers.get("budget_usd", 0)
        if budget < data["min_program_investment_usd"]:
            eliminated.append({
                "country": name,
                "reason": f"Budget ${budget:,} below minimum ${data['min_program_investment_usd']:,}",
            })
            continue

        surviving.append(name)

    return surviving, eliminated


def score_country(country_name, normalized_weights, all_countries_data):
    """
    Scores a country using winsorized determinant values.
    all_countries_data: iterable of country names for surviving countries —
    used to compute Winsorization bounds.
    """
    data = COUNTRIES[country_name]
    breakdown = {}
    total = 0.0

    for det, weight_pct in normalized_weights.items():
        all_vals = [
            COUNTRIES[c]["scores"].get(det, 0)
            for c in all_countries_data
        ]
        raw_score = data["scores"].get(det, 0)
        winsorized_score = winsorize(raw_score, all_vals)

        contribution = (winsorized_score / 10) * weight_pct
        breakdown[det] = round(contribution, 2)
        total += contribution

    return round(total, 2), breakdown


def rank_countries(answers):
    """
    Full country pipeline:
    1. Apply hard filters
    2. Compute weights from answers
    3. Score and rank surviving countries
    Returns (ranked_list, eliminated, normalized_weights, weight_log)
    """
    surviving, eliminated = apply_country_hard_filters(answers)
    _, normalized_weights, weight_log = compute_country_weights(answers)

    ranked = []
    for country in surviving:
        score, breakdown = score_country(
            country, normalized_weights, surviving
        )
        ranked.append({"country": country, "score": score, "breakdown": breakdown})

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked, eliminated, normalized_weights, weight_log
