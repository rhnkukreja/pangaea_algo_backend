# ─── CONSTANTS ────────────────────────────────────────────
WEIGHT_FLOOR = 5.0
WEIGHT_CAP = 35.0

# ─── INVERSE VARIABLES ────────────────────────────────────
# For these, higher raw value = worse outcome.
# They are already inverted during data normalization in the engine files.
# Tag them here for reference and validation.
INVERSE_COUNTRY_VARS = [
    "currency_volatility",
    "property_taxation_for_foreigners",
    "interest_rate_direction",
    "corruption_perception_index"
]
INVERSE_CITY_VARS = [
    "supply_pipeline"
]

# ─── COUNTRY BASELINES (must sum to 100) ──────────────────
COUNTRY_BASELINE_WEIGHTS = {
    "political_stability_index": 25,
    "currency_volatility": 20,
    "property_taxation_for_foreigners": 18,
    "interest_rate_direction": 15,
    "foreign_buyer_market_share": 12,
    "corruption_perception_index": 10
}

# ─── COUNTRY TIER 1 — Primary Objective (max ±15) ─────────
COUNTRY_TIER1_SHIFTS = {
     "capital_appreciation": {
        "foreign_buyer_market_share": 10,
        "interest_rate_direction": 5,
        "political_stability_index": -10,
        "corruption_perception_index": -5,
    },

    "yield_cash_flow": {
        "property_taxation_for_foreigners": 8,
        "currency_volatility": 7,
        "political_stability_index": -10,
        "foreign_buyer_market_share": -5,
    },

   "capital_preservation": {
    "political_stability_index": 5,
    "currency_volatility": 5,
    "foreign_buyer_market_share": -5,
    "interest_rate_direction": -10,
},

"investment_diversification": {
    "political_stability_index": 5,
    "currency_volatility": 5,
    "foreign_buyer_market_share": -5,
    "interest_rate_direction": -10,
},

    "residency_citizenship": {
        "political_stability_index": 10,
        "corruption_perception_index": 5,
        "property_taxation_for_foreigners": -10,
        "currency_volatility": -5,
    },
}

# ─── COUNTRY TIER 2 — Risk Appetite (max ±10) ─────────────
COUNTRY_TIER2_SHIFTS = {
    "conservative": {
        "political_stability_index": +7,
        "currency_volatility": +3,
        "foreign_buyer_market_share": -7,
        "interest_rate_direction": -3
    },
    "moderate": {},
    "opportunistic": {
        "foreign_buyer_market_share": +7,
        "interest_rate_direction": +3,
        "political_stability_index": -7,
        "currency_volatility": -3
    }
}

# ─── CITY BASELINES (must sum to 100) ─────────────────────
CITY_BASELINE_WEIGHTS = {
    "employment_growth": 15,
    "price_appreciation_5y": 15,
    "net_migration_rate": 14,
    "rental_demand_index": 14,
    "infrastructure_pipeline": 12,
    "liquidity_indicator": 10,
    "quality_of_life_index": 10,
    "tourism_strength": 5,
    "supply_pipeline": 5
}

# ─── CITY TIER 1 — Primary Objective (max ±15) ────────────
CITY_TIER1_SHIFTS = {
    "capital_appreciation": {
        "infrastructure_pipeline": +7,
        "price_appreciation_5y": +5,
        "net_migration_rate": +3,
        "rental_demand_index": -8,
        "liquidity_indicator": -4,
        "quality_of_life_index": -3
    },
    "yield_cash_flow": {
        "rental_demand_index": +8,
        "tourism_strength": +5,
        "employment_growth": +2,
        "price_appreciation_5y": -8,
        "infrastructure_pipeline": -7
    },
    "capital_preservation": {
        "liquidity_indicator": +8,
        "employment_growth": +5,
        "supply_pipeline": +2,
        "price_appreciation_5y": -9,
        "infrastructure_pipeline": -6
    },
    "lifestyle_end_use": {
        "quality_of_life_index": +10,
        "tourism_strength": +5,
        "rental_demand_index": -10,
        "price_appreciation_5y": -5
    },
    "residency_citizenship": {
        "liquidity_indicator": +8,
        "quality_of_life_index": +7,
        "rental_demand_index": -8,
        "infrastructure_pipeline": -4,
        "price_appreciation_5y": -3
    }
}

# ─── CITY TIER 2 — Risk Appetite (max ±10) ────────────────
CITY_TIER2_SHIFTS = {
    "conservative": {
        "liquidity_indicator": +5,
        "employment_growth": +3,
        "supply_pipeline": +2,
        "infrastructure_pipeline": -6,
        "price_appreciation_5y": -4
    },
    "moderate": {},
    "opportunistic": {
        "infrastructure_pipeline": +6,
        "net_migration_rate": +4,
        "liquidity_indicator": -6,
        "quality_of_life_index": -4
    }
}

# ─── CORE MATH FUNCTION ───────────────────────────────────


OBJECTIVE_ALIASES = {
    "rental_yield":               "yield_cash_flow",
    "yield":                      "yield_cash_flow",
    "roi":                        "yield_cash_flow",
    "citizenship":                "residency_citizenship",
    "golden_visa":                "residency_citizenship",
    "residency":                  "residency_citizenship",
    "lifestyle":                  "lifestyle_end_use",
    "end_use":                    "lifestyle_end_use",
    "vacation_home":              "lifestyle_end_use",
    "capital_appreciation":       "capital_appreciation",
    "capital_preservation":       "capital_preservation",
    "investment_diversification": "capital_appreciation",
    "yield_cash_flow":            "yield_cash_flow",
    "residency_citizenship":      "residency_citizenship",
    "lifestyle_end_use":          "lifestyle_end_use",
}


def apply_shifts(baseline_weights, tier1_shifts, tier2_shifts):
    """
    Applies Tier 1 then Tier 2 shifts using Diminishing Returns.
    Then proportionally normalizes to sum to 100.

    Rule 1: Tier 1 max ±15, Tier 2 max ±10 (enforced by the shift
            values defined above — not re-validated in code)
    Rule 2: Floor 5%, Cap 35% — enforced on every shift before normalization
    Rule 3: Adjusted Shift = Raw Shift × (1 - Current Weight / 100)
    """
    weights = {k: float(v) for k, v in baseline_weights.items()}
    log = []

    for tier_label, shifts in [("Tier 1", tier1_shifts),
                                ("Tier 2", tier2_shifts)]:
        if not shifts:
            continue

        # Positives first
        for det, raw in sorted(shifts.items(), key=lambda x: -x[1]):
            if raw <= 0:
                continue
            current = weights.get(det, 0.0)
            adjusted = raw * (1 - current / 100)
            new_val = min(max(current + adjusted, WEIGHT_FLOOR), WEIGHT_CAP)
            log.append({
                "tier": tier_label, "determinant": det,
                "raw_shift": raw, "adjusted_shift": round(adjusted, 3),
                "before": round(current, 3), "after": round(new_val, 3)
            })
            weights[det] = new_val

        # Negatives second
        for det, raw in sorted(shifts.items(), key=lambda x: x[1]):
            if raw >= 0:
                continue
            current = weights.get(det, 0.0)
            adjusted = raw * (1 - current / 100)
            new_val = min(max(current + adjusted, WEIGHT_FLOOR), WEIGHT_CAP)
            log.append({
                "tier": tier_label, "determinant": det,
                "raw_shift": raw, "adjusted_shift": round(adjusted, 3),
                "before": round(current, 3), "after": round(new_val, 3)
            })
            weights[det] = new_val

    # Proportional normalization — caps already enforced above, do not re-apply
    total = sum(weights.values())
    normalized = {
        k: round((v / total) * 100, 2)
        for k, v in weights.items()
    }

    return weights, normalized, log


def compute_country_weights(answers):
    objective = OBJECTIVE_ALIASES.get(answers.get("primary_objective", ""),
                                      answers.get("primary_objective", ""))
    risk = answers.get("risk_appetite", "moderate")
    t1 = COUNTRY_TIER1_SHIFTS.get(objective, {})
    t2 = COUNTRY_TIER2_SHIFTS.get(risk, {})
    return apply_shifts(COUNTRY_BASELINE_WEIGHTS, t1, t2)


def compute_city_weights(answers):
    objective = OBJECTIVE_ALIASES.get(answers.get("primary_objective", ""),
                                      answers.get("primary_objective", ""))
    risk = answers.get("risk_appetite", "moderate")
    t1 = CITY_TIER1_SHIFTS.get(objective, {})
    t2 = CITY_TIER2_SHIFTS.get(risk, {})
    return apply_shifts(CITY_BASELINE_WEIGHTS, t1, t2)


# ─── WINSORIZATION ────────────────────────────────────────

def winsorize(value, all_values, percentile=95):
    """
    Caps value at the 95th percentile of all_values.
    """
    if not all_values:
        return value
    sorted_vals = sorted(all_values)
    cap_idx = min(int(len(sorted_vals) * percentile / 100),
                  len(sorted_vals) - 1)
    return min(value, sorted_vals[cap_idx])


# Empty placeholder: some callers import this symbol for diagnostics.
CITY_QUESTION_DELTAS = {}
