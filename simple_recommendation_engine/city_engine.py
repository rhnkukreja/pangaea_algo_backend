from weights_config import compute_city_weights, winsorize

CITIES = {
    "Athens": {
        "country": "Greece",
        "coastal": False,
        "scores": {
            "net_migration_rate": 4.5,
            "employment_growth": 4.67,
            "price_appreciation_5y": 7.86,
            "liquidity_indicator": 4,
            "tourism_strength": 6,
            "rental_demand_index": 8,
            "rental_yield": 0,
            "infrastructure_pipeline": 7,
            "supply_pipeline": 4,
            "quality_of_life_index": 2.92,
        },
    },
    "Piraeus": {
        "country": "Greece",
        "coastal": True,
        "scores": {
            "net_migration_rate": 3.5,
            "employment_growth": 4.17,
            "price_appreciation_5y": 7.86,
            "liquidity_indicator": 4,
            "tourism_strength": 6,
            "rental_demand_index": 8,
            "rental_yield": 0,
            "infrastructure_pipeline": 7,
            "supply_pipeline": 4,
            "quality_of_life_index": 2.92,
        },
    },
    "Crete": {
        "country": "Greece",
        "coastal": True,
        "scores": {
            "net_migration_rate": 2.0,
            "employment_growth": 3.67,
            "price_appreciation_5y": 6.86,
            "liquidity_indicator": 2,
            "tourism_strength": 8,
            "rental_demand_index": 8,
            "rental_yield": 0,
            "infrastructure_pipeline": 6,
            "supply_pipeline": 4,
            "quality_of_life_index": 2.92,
        },
    },
    "Mykonos": {
        "country": "Greece",
        "coastal": True,
        "scores": {
            "net_migration_rate": 3.0,
            "employment_growth": 5.0,
            "price_appreciation_5y": 8.57,
            "liquidity_indicator": 4,
            "tourism_strength": 10,
            "rental_demand_index": 10,
            "rental_yield": 0,
            "infrastructure_pipeline": 3,
            "supply_pipeline": 2,
            "quality_of_life_index": 2.92,
        },
    },
    "Thessaloniki": {
        "country": "Greece",
        "coastal": True,
        "scores": {
            "net_migration_rate": 1.25,
            "employment_growth": 3.0,
            "price_appreciation_5y": 7.14,
            "liquidity_indicator": 4,
            "tourism_strength": 6,
            "rental_demand_index": 6,
            "rental_yield": 0,
            "infrastructure_pipeline": 8,
            "supply_pipeline": 4,
            "quality_of_life_index": 3.22,
        },
    },
    "Lisbon": {
        "country": "Portugal",
        "coastal": False,
        "scores": {
            "net_migration_rate": 3.25,
            "employment_growth": 5.83,
            "price_appreciation_5y": 6.43,
            "liquidity_indicator": 6,
            "tourism_strength": 8,
            "rental_demand_index": 8,
            "rental_yield": 0,
            "infrastructure_pipeline": 8,
            "supply_pipeline": 4,
            "quality_of_life_index": 5.36,
        },
    },
    "Cascais": {
        "country": "Portugal",
        "coastal": True,
        "scores": {
            "net_migration_rate": 4.0,
            "employment_growth": 6.33,
            "price_appreciation_5y": 7.14,
            "liquidity_indicator": 8,
            "tourism_strength": 8,
            "rental_demand_index": 10,
            "rental_yield": 0,
            "infrastructure_pipeline": 7,
            "supply_pipeline": 4,
            "quality_of_life_index": 5.36,
        },
    },
    "Algarve": {
        "country": "Portugal",
        "coastal": True,
        "scores": {
            "net_migration_rate": 4.5,
            "employment_growth": 5.33,
            "price_appreciation_5y": 7.86,
            "liquidity_indicator": 8,
            "tourism_strength": 10,
            "rental_demand_index": 10,
            "rental_yield": 0,
            "infrastructure_pipeline": 7,
            "supply_pipeline": 6,
            "quality_of_life_index": 5.36,
        },
    },
    "Braga": {
        "country": "Portugal",
        "coastal": False,
        "scores": {
            "net_migration_rate": 2.75,
            "employment_growth": 5.0,
            "price_appreciation_5y": 5.71,
            "liquidity_indicator": 6,
            "tourism_strength": 6,
            "rental_demand_index": 8,
            "rental_yield": 0,
            "infrastructure_pipeline": 6,
            "supply_pipeline": 4,
            "quality_of_life_index": 5.36,
        },
    },
    "Porto": {
        "country": "Portugal",
        "coastal": True,
        "scores": {
            "net_migration_rate": 2.25,
            "employment_growth": 4.33,
            "price_appreciation_5y": 6.0,
            "liquidity_indicator": 6,
            "tourism_strength": 8,
            "rental_demand_index": 6,
            "rental_yield": 0,
            "infrastructure_pipeline": 8,
            "supply_pipeline": 4,
            "quality_of_life_index": 7.72,
        },
    },
    "Phuket": {
        "country": "Thailand",
        "coastal": True,
        "scores": {
            "net_migration_rate": 3.5,
            "employment_growth": 6.67,
            "price_appreciation_5y": 4.29,
            "liquidity_indicator": 8,
            "tourism_strength": 10,
            "rental_demand_index": 0,
            "rental_yield": 0,
            "infrastructure_pipeline": 7,
            "supply_pipeline": 6,
            "quality_of_life_index": 0.68,
        },
    },
    "Bangkok": {
        "country": "Thailand",
        "coastal": False,
        "scores": {
            "net_migration_rate": 1.0,
            "employment_growth": 3.33,
            "price_appreciation_5y": 3.57,
            "liquidity_indicator": 4,
            "tourism_strength": 6,
            "rental_demand_index": 0,
            "rental_yield": 0,
            "infrastructure_pipeline": 9,
            "supply_pipeline": 6,
            "quality_of_life_index": 0.68,
        },
    },
    "Pattaya": {
        "country": "Thailand",
        "coastal": True,
        "scores": {
            "net_migration_rate": 2.75,
            "employment_growth": 5.83,
            "price_appreciation_5y": 4.0,
            "liquidity_indicator": 8,
            "tourism_strength": 10,
            "rental_demand_index": 0,
            "rental_yield": 0,
            "infrastructure_pipeline": 8,
            "supply_pipeline": 6,
            "quality_of_life_index": 0.68,
        },
    },
    "Chiang Mai": {
        "country": "Thailand",
        "coastal": False,
        "scores": {
            "net_migration_rate": 1.75,
            "employment_growth": 4.17,
            "price_appreciation_5y": 3.14,
            "liquidity_indicator": 6,
            "tourism_strength": 8,
            "rental_demand_index": 0,
            "rental_yield": 0,
            "infrastructure_pipeline": 6,
            "supply_pipeline": 6,
            "quality_of_life_index": 0.68,
        },
    },
    "Hua Hin": {
        "country": "Thailand",
        "coastal": True,
        "scores": {
            "net_migration_rate": 2.25,
            "employment_growth": 4.67,
            "price_appreciation_5y": 3.71,
            "liquidity_indicator": 6,
            "tourism_strength": 8,
            "rental_demand_index": 0,
            "rental_yield": 0,
            "infrastructure_pipeline": 6,
            "supply_pipeline": 6,
            "quality_of_life_index": 0.68,
        },
    },
    "Dubai": {
        "country": "UAE",
        "coastal": True,
        "scores": {
            "net_migration_rate": 9.0,
            "employment_growth": 9.17,
            "price_appreciation_5y": 10.0,
            "liquidity_indicator": 10,
            "tourism_strength": 8,
            "rental_demand_index": 10,
            "rental_yield": 0,
            "infrastructure_pipeline": 10,
            "supply_pipeline": 8,
            "quality_of_life_index": 7.55,
        },
    },
    "Abu Dhabi": {
        "country": "UAE",
        "coastal": True,
        "scores": {
            "net_migration_rate": 6.0,
            "employment_growth": 7.0,
            "price_appreciation_5y": 5.0,
            "liquidity_indicator": 6,
            "tourism_strength": 6,
            "rental_demand_index": 8,
            "rental_yield": 0,
            "infrastructure_pipeline": 9,
            "supply_pipeline": 6,
            "quality_of_life_index": 7.55,
        },
    },
    "Sharjah": {
        "country": "UAE",
        "coastal": True,
        "scores": {
            "net_migration_rate": 5.0,
            "employment_growth": 6.33,
            "price_appreciation_5y": 4.29,
            "liquidity_indicator": 6,
            "tourism_strength": 4,
            "rental_demand_index": 6,
            "rental_yield": 0,
            "infrastructure_pipeline": 7,
            "supply_pipeline": 6,
            "quality_of_life_index": 7.55,
        },
    },
    "Ras Al Khaimah": {
        "country": "UAE",
        "coastal": True,
        "scores": {
            "net_migration_rate": 5.5,
            "employment_growth": 6.67,
            "price_appreciation_5y": 5.43,
            "liquidity_indicator": 6,
            "tourism_strength": 6,
            "rental_demand_index": 8,
            "rental_yield": 0,
            "infrastructure_pipeline": 7,
            "supply_pipeline": 6,
            "quality_of_life_index": 7.55,
        },
    },
    "Ajman": {
        "country": "UAE",
        "coastal": True,
        "scores": {
            "net_migration_rate": 4.5,
            "employment_growth": 5.83,
            "price_appreciation_5y": 4.0,
            "liquidity_indicator": 6,
            "tourism_strength": 4,
            "rental_demand_index": 6,
            "rental_yield": 0,
            "infrastructure_pipeline": 6,
            "supply_pipeline": 6,
            "quality_of_life_index": 7.55,
        },
    },
}


def score_city(city_name, normalized_weights, candidate_cities):
    data = CITIES[city_name]
    breakdown = {}
    total = 0.0

    for det, weight_pct in normalized_weights.items():
        all_vals = [
            CITIES[c]["scores"].get(det, 0)
            for c in candidate_cities
        ]
        raw_score = data["scores"].get(det, 0)
        winsorized_score = winsorize(raw_score, all_vals)

        contribution = (winsorized_score / 10) * weight_pct
        breakdown[det] = round(contribution, 2)
        total += contribution

    return round(total, 2), breakdown


def rank_cities(surviving_countries, answers):
    """
    Returns ranked cities only within the surviving countries list.
    Returns (ranked_list, normalized_weights, weight_log)
    """
    _, normalized_weights, weight_log = compute_city_weights(answers)

    candidate_cities = [
        name for name, data in CITIES.items()
        if data["country"] in surviving_countries
    ]

    ranked = []
    for city in candidate_cities:
        score, breakdown = score_city(
            city, normalized_weights, candidate_cities
        )
        ranked.append({
            "city": city,
            "country": CITIES[city]["country"],
            "score": score,
            "breakdown": breakdown,
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked, normalized_weights, weight_log
