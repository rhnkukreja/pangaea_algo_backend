import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from country_engine import rank_countries, COUNTRIES
from city_engine import rank_cities, CITIES

# ---------------------------------------------------------------------------
# Personas (only the fields used by the current engine are consumed below)
# ---------------------------------------------------------------------------

PERSONAS = [
    {
        "name": "Citizenship Seeker",
        "primary_objective": "citizenship",
        "visa_required": "mandatory",
        "citizenship_required": "yes",
        "budget_usd": 500000,
        "risk_appetite": "conservative",
        "ownership_structure": "freehold_only",   # Q6: ownership type
        "usage_intent": "primary_relocation",
        "family_composition": "family_with_children",
        "proximity_preferences": ["airport", "schools", "hospital"],
        "prestige_sensitivity": "medium",
        "lifestyle_preference": "no_preference",
    },
    {
        "name": "Golden Visa Seeker",
        "primary_objective": "golden_visa",
        "visa_required": "mandatory",
        "citizenship_required": "no",
        "budget_usd": 800000,
        "risk_appetite": "moderate",
        "ownership_structure": "freehold_only",   # Q6: ownership type
        "usage_intent": "holiday_second_home",    # mapped ->primary_relocation
        "family_composition": "single_or_couple",
        "proximity_preferences": ["beach", "airport"],
        "prestige_sensitivity": "high",
        "lifestyle_preference": "coastal",
    },
    {
        "name": "ROI Focused Investor",
        "primary_objective": "roi",               # mapped ->rental_yield
        "visa_required": "not_required",          # mapped ->no
        "citizenship_required": "no",
        "budget_usd": 1000000,
        "risk_appetite": "opportunistic",
        "ownership_structure": "any",             # Q6: ownership type — no preference
        "usage_intent": "pure_investment",
        "family_composition": "single_or_couple",
        "proximity_preferences": ["airport"],
        "prestige_sensitivity": "high",
        "lifestyle_preference": "no_preference",
    },
]

# ---------------------------------------------------------------------------
# Field mappings (spec section "Apply these mappings before calling engines")
# ---------------------------------------------------------------------------

PRIMARY_OBJECTIVE_MAP = {
    "roi": "rental_yield",
}

VISA_REQUIRED_MAP = {
    "not_required": "no",
}

USAGE_INTENT_MAP = {
    "holiday_second_home": "primary_relocation",
}

COUNTRY_DETERMINANT_LABELS = {
    "political_stability_index": "Political Stability",
    "corruption_perception_index": "Corruption Index",
    "currency_volatility": "Currency Volatility",
    "interest_rate_direction": "Interest Rate Direction",
    "foreign_buyer_market_share": "Foreign Buyer Share",
    "property_taxation_for_foreigners": "Property Taxation",
}

CITY_DETERMINANT_LABELS = {
    "net_migration_rate": "Net Migration",
    "employment_growth": "Employment Growth",
    "price_appreciation_5y": "Price Appreciation",
    "liquidity_indicator": "Liquidity",
    "tourism_strength": "Tourism",
    "rental_demand_index": "Rental Demand",
    "rental_yield": "Rental Yield",
    "infrastructure_pipeline": "Infrastructure",
    "supply_pipeline": "Supply Pipeline",
    "quality_of_life_index": "Quality of Life",
}

COUNTRY_SCORE_SHORT = {
    "political_stability_index": "PS",
    "corruption_perception_index": "CPI",
    "currency_volatility": "CV",
    "interest_rate_direction": "IRD",
    "foreign_buyer_market_share": "FBS",
    "property_taxation_for_foreigners": "TAX",
}

CITY_SCORE_SHORT = {
    "net_migration_rate": "MIG",
    "employment_growth": "EMP",
    "price_appreciation_5y": "PRICE",
    "liquidity_indicator": "LIQ",
    "tourism_strength": "TOUR",
    "rental_demand_index": "RENT",
    "rental_yield": "YIELD",
    "infrastructure_pipeline": "INFRA",
    "supply_pipeline": "SUPPLY",
    "quality_of_life_index": "QOL",
}


def map_country_answers(persona):
    return {
        "primary_objective": PRIMARY_OBJECTIVE_MAP.get(
            persona["primary_objective"], persona["primary_objective"]
        ),
        "visa_required": VISA_REQUIRED_MAP.get(
            persona["visa_required"], persona["visa_required"]
        ),
        "citizenship_required": persona["citizenship_required"],
        "budget_usd": persona["budget_usd"],
        "risk_appetite": persona["risk_appetite"],
        "ownership_structure": persona.get("ownership_structure", "any"),
    }


def map_city_answers(persona):
    return {
        "usage_intent": USAGE_INTENT_MAP.get(
            persona["usage_intent"], persona["usage_intent"]
        ),
        "family_composition": persona["family_composition"],
        "proximity_preferences": persona["proximity_preferences"],
        "prestige_sensitivity": persona["prestige_sensitivity"],
        "lifestyle_preference": persona["lifestyle_preference"],
    }


def fmt(value, width=6):
    return str(round(value, 2)).rjust(width)


def print_country_weight_distribution(norm_weights):
    print("Country Weight Distribution (final normalized %):")
    for key, label in COUNTRY_DETERMINANT_LABELS.items():
        print(f"  {label:<30} ->{norm_weights.get(key, 0):.2f}%")


def print_city_weight_distribution(norm_weights):
    print("City Weight Distribution (final normalized %):")
    for key, label in CITY_DETERMINANT_LABELS.items():
        print(f"  {label:<22} ->{norm_weights.get(key, 0):.2f}%")


def print_country_breakdown(item, norm_weights):
    parts = []
    for key, abbr in COUNTRY_SCORE_SHORT.items():
        score = COUNTRIES[item["country"]]["scores"].get(key, 0)
        parts.append(f"{abbr}: {score}")
    print(f"     {' | '.join(parts)}")


def print_city_breakdown(item):
    scores = CITIES[item["city"]]["scores"]
    row1 = " | ".join(
        f"{CITY_SCORE_SHORT[k]}: {scores.get(k, 0)}"
        for k in ["net_migration_rate", "employment_growth", "price_appreciation_5y",
                  "liquidity_indicator", "tourism_strength"]
    )
    row2 = " | ".join(
        f"{CITY_SCORE_SHORT[k]}: {scores.get(k, 0)}"
        for k in ["rental_demand_index", "rental_yield", "infrastructure_pipeline",
                  "supply_pipeline", "quality_of_life_index"]
    )
    print(f"     {row1}")
    print(f"     {row2}")


def check_weight_change(norm_weights, city_answers, persona_name):
    """Flag lifestyle_preference if it triggered no weight delta."""
    lp = city_answers.get("lifestyle_preference", "")
    if lp and lp not in ("no_preference",):
        from weights_config import CITY_QUESTION_DELTAS
        if lp not in CITY_QUESTION_DELTAS.get("lifestyle_preference", {}):
            print(f"  [!] lifestyle_preference='{lp}' has no delta defined in config -- weights unchanged by this field")


def run_persona(persona, index):
    print()
    print("=" * 60)
    print(f"PERSONA: {persona['name']}")
    print("=" * 60)

    country_answers = map_country_answers(persona)
    city_answers = map_city_answers(persona)

    # Header summary
    print(f"Budget: ${persona['budget_usd']:,}")
    print(f"Objective: {country_answers['primary_objective']} | Risk: {country_answers['risk_appetite']}")
    print(f"Citizenship: {country_answers['citizenship_required']} | Visa: {country_answers['visa_required']}")
    print(f"Ownership: {country_answers['ownership_structure']}")
    print(f"Family: {city_answers['family_composition']} | Usage: {city_answers['usage_intent']}")
    print(f"Proximity: {city_answers['proximity_preferences']}")
    print(f"Prestige: {city_answers['prestige_sensitivity']} | Lifestyle: {city_answers['lifestyle_preference']}")

    # ------------------------------------------------------------------
    # PHASE 1 — Country
    # ------------------------------------------------------------------
    print()
    print("-" * 60)
    print("PHASE 1 — COUNTRY LEVEL")
    print("-" * 60)
    print()

    ranked_countries, eliminated, norm_cw, _ = rank_countries(country_answers)

    print_country_weight_distribution(norm_cw)
    print()

    surviving_names = [r["country"] for r in ranked_countries]

    print(f"Surviving Countries ({len(ranked_countries)}):")
    for i, item in enumerate(ranked_countries, 1):
        print(f"  #{i} {item['country']} — {item['score']}/100")
        print_country_breakdown(item, norm_cw)

    print()
    if eliminated:
        print("Eliminated:")
        for e in eliminated:
            print(f"  [X] {e['country']} -- {e['reason']}")
    else:
        print("Eliminated: none")

    # ------------------------------------------------------------------
    # PHASE 2 — City
    # ------------------------------------------------------------------
    print()
    print("-" * 60)
    print("PHASE 2 — CITY LEVEL")
    print("-" * 60)
    print()

    ranked_cities, norm_cityw, _ = rank_cities(surviving_names, city_answers)

    print_city_weight_distribution(norm_cityw)
    print()

    check_weight_change(norm_cityw, city_answers, persona["name"])

    print("Top 5 Cities:")
    for i, item in enumerate(ranked_cities[:5], 1):
        print(f"  #{i} {item['city']}, {item['country']} — {item['score']}/100")
        print_city_breakdown(item)

    top_country = ranked_countries[0]["country"] if ranked_countries else "—"
    top_city = ranked_cities[0]["city"] if ranked_cities else "—"

    return top_country, top_city


def main():
    results = []
    for i, persona in enumerate(PERSONAS, 1):
        top_country, top_city = run_persona(persona, i)
        results.append((i, persona["name"], top_country, top_city))

    # ------------------------------------------------------------------
    # Summary + sanity checks
    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for idx, name, top_country, top_city in results:
        print(f"Persona {idx}: Top country = {top_country}, Top city = {top_city}")
    print("=" * 60)

    warnings = []

    _, _, p1_country, p1_city = results[0]
    if set(PERSONAS[0]["name"]):  # always run checks
        # Persona 1: only Greece + Portugal should survive
        ranked1, _, _, _ = rank_countries(map_country_answers(PERSONAS[0]))
        surviving1 = {r["country"] for r in ranked1}
        expected1 = {"Greece", "Portugal"}
        if surviving1 != expected1:
            warnings.append(f"Persona 1: Expected surviving={expected1}, got={surviving1}")

    _, _, p3_country, p3_city = results[2]
    if p3_country != "UAE":
        warnings.append(f"Persona 3: Expected top country=UAE, got={p3_country}")
    if p3_city not in ("Dubai", "Abu Dhabi"):
        warnings.append(f"Persona 3: Expected top city=Dubai or Abu Dhabi, got={p3_city}")

    if warnings:
        print()
        for w in warnings:
            print(f"[!] {w}")
    else:
        print()
        print("All expected outcomes verified [OK]")


if __name__ == "__main__":
    main()
