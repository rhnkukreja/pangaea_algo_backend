# =========================================================
# PROJECT ENGINE
# Cascading Archetype Model
# =========================================================

PROJECTS = {

    "Palm Residences": {

        "country": "UAE",
        "city": "Dubai",

        "price": 850000,
        "status": "ready",
        "ownership": "freehold",
        "property_type": "Apartment",

        "scores": {
            "delivery_history": 9,
            "project_exit_liquidity": 8,
            "project_completion_rate": 9,
            "financial_strength": 8,
            "expected_rental_yield": 7,
            "public_infrastructure_proximity": 9,
            "construction_quality": 9,
            "litigation_history": 9,
        },
    },

    "Marina Heights": {

        "country": "UAE",
        "city": "Dubai",

        "price": 650000,
        "status": "offplan",
        "ownership": "freehold",
        "property_type": "Apartment",

        "scores": {
            "delivery_history": 8,
            "project_exit_liquidity": 9,
            "project_completion_rate": 8,
            "financial_strength": 8,
            "expected_rental_yield": 9,
            "public_infrastructure_proximity": 10,
            "construction_quality": 8,
            "litigation_history": 8,
        },
    },

    "Lisbon Grand Park": {

        "country": "Portugal",
        "city": "Lisbon",

        "price": 1200000,
        "status": "ready",
        "ownership": "freehold",
        "property_type": "Villa",

        "scores": {
            "delivery_history": 9,
            "project_exit_liquidity": 7,
            "project_completion_rate": 8,
            "financial_strength": 9,
            "expected_rental_yield": 6,
            "public_infrastructure_proximity": 9,
            "construction_quality": 9,
            "litigation_history": 9,
        },
    },

    "Bangkok Riverside": {

        "country": "Thailand",
        "city": "Bangkok",

        "price": 450000,
        "status": "offplan",
        "ownership": "leasehold",
        "property_type": "Managed",

        "scores": {
            "delivery_history": 7,
            "project_exit_liquidity": 8,
            "project_completion_rate": 7,
            "financial_strength": 7,
            "expected_rental_yield": 9,
            "public_infrastructure_proximity": 8,
            "construction_quality": 7,
            "litigation_history": 8,
        },
    },
}

# =========================================================
# BASELINE WEIGHTS
# =========================================================

PROJECT_BASELINE_WEIGHTS = {

    "delivery_history": 18,

    "project_exit_liquidity": 16,

    "project_completion_rate": 15,

    "financial_strength": 15,

    "expected_rental_yield": 14,

    "public_infrastructure_proximity": 10,

    "construction_quality": 7,

    "litigation_history": 5,
}

# =========================================================
# SHIFT FUNCTION
# =========================================================

def apply_shift(
    weights,
    determinant,
    raw_shift,
    tier,
    weight_log,
):

    current_weight = weights[determinant]

    adjusted_shift = raw_shift * (
        1 - (current_weight / 100)
    )

    new_weight = current_weight + adjusted_shift

    # caps and floor
    new_weight = max(5, min(35, new_weight))

    weights[determinant] = round(new_weight, 2)

    weight_log.append({

        "tier": tier,

        "determinant": determinant,

        "raw_shift": raw_shift,

        "adjusted_shift": round(
            adjusted_shift,
            2,
        ),

        "before": current_weight,

        "after": round(new_weight, 2),
    })


# =========================================================
# WEIGHT ENGINE
# =========================================================

def compute_project_weights(answers):

    weights = PROJECT_BASELINE_WEIGHTS.copy()

    weight_log = []

    # =====================================================
    # TIER 1
    # =====================================================

    # -----------------------------------------------------
    # Usage Intent
    # -----------------------------------------------------

    if answers["usage_intent"] == "pure_investment":

        apply_shift(
            weights,
            "expected_rental_yield",
            8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            7,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "delivery_history",
            -6,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "financial_strength",
            -5,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "public_infrastructure_proximity",
            -4,
            "Tier 1",
            weight_log,
        )

    elif answers["usage_intent"] == "investment_occasional_use":

        apply_shift(
            weights,
            "expected_rental_yield",
            6,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "construction_quality",
            5,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "public_infrastructure_proximity",
            4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            -8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "financial_strength",
            -4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "delivery_history",
            -3,
            "Tier 1",
            weight_log,
        )

    elif answers["usage_intent"] == "primary_relocation":

        apply_shift(
            weights,
            "construction_quality",
            8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "public_infrastructure_proximity",
            7,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "expected_rental_yield",
            -8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            -4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_completion_rate",
            -3,
            "Tier 1",
            weight_log,
        )

    # -----------------------------------------------------
    # Holding Period
    # -----------------------------------------------------

    if answers["holding_period"] == "short_term":

        apply_shift(
            weights,
            "project_completion_rate",
            8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            7,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "expected_rental_yield",
            -8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "delivery_history",
            -4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "financial_strength",
            -3,
            "Tier 1",
            weight_log,
        )

    elif answers["holding_period"] == "medium_term":

        apply_shift(
            weights,
            "expected_rental_yield",
            6,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            5,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_completion_rate",
            4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "delivery_history",
            -7,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "financial_strength",
            -5,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "public_infrastructure_proximity",
            -3,
            "Tier 1",
            weight_log,
        )

    elif answers["holding_period"] == "long_term":

        apply_shift(
            weights,
            "expected_rental_yield",
            8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "construction_quality",
            7,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            -8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_completion_rate",
            -4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "public_infrastructure_proximity",
            -3,
            "Tier 1",
            weight_log,
        )

    # -----------------------------------------------------
    # Liquidity Preference
    # -----------------------------------------------------

    if answers["liquidity_preference"] == "high_resale":

        apply_shift(
            weights,
            "project_exit_liquidity",
            10,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_completion_rate",
            5,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "expected_rental_yield",
            -8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "financial_strength",
            -4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "delivery_history",
            -3,
            "Tier 1",
            weight_log,
        )

    elif answers["liquidity_preference"] == "long_lockin":

        apply_shift(
            weights,
            "expected_rental_yield",
            8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "financial_strength",
            7,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            -10,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_completion_rate",
            -5,
            "Tier 1",
            weight_log,
        )

    # -----------------------------------------------------
    # Risk Appetite
    # -----------------------------------------------------

    if answers["risk_appetite"] == "conservative":

        apply_shift(
            weights,
            "financial_strength",
            6,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "delivery_history",
            5,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_completion_rate",
            2,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "litigation_history",
            2,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "expected_rental_yield",
            -8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            -4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "public_infrastructure_proximity",
            -3,
            "Tier 1",
            weight_log,
        )

    elif answers["risk_appetite"] == "opportunistic":

        apply_shift(
            weights,
            "expected_rental_yield",
            8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_exit_liquidity",
            7,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "delivery_history",
            -8,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "financial_strength",
            -4,
            "Tier 1",
            weight_log,
        )

        apply_shift(
            weights,
            "project_completion_rate",
            -3,
            "Tier 1",
            weight_log,
        )

    # =====================================================
    # NORMALIZATION
    # =====================================================

    total = sum(weights.values())

    normalized_weights = {

        k: round((v / total) * 100, 1)

        for k, v in weights.items()
    }

    return normalized_weights, weight_log


# =========================================================
# PROJECT RANKING ENGINE
# =========================================================

def rank_projects(
    surviving_countries,
    answers,
):

    normalized_weights, weight_log = (
        compute_project_weights(answers)
    )

    ranked = []

    eliminated = []

    # =====================================================
    # HARD FILTERS
    # =====================================================

    for project_name, project_data in PROJECTS.items():

        if (
            project_data["country"]
            not in surviving_countries
        ):
            continue

        # -------------------------------------------------
        # Budget Filter
        # -------------------------------------------------

        budget_limit = answers["budget"] * 1.2

        if project_data["price"] > budget_limit:

            eliminated.append({
                "project": project_name,
                "reason": "Budget exceeded",
            })

            continue

        # -------------------------------------------------
        # Status Filter
        # -------------------------------------------------

        if (
            answers["ready_to_move"] == "yes"
            and project_data["status"] != "ready"
        ):

            eliminated.append({
                "project": project_name,
                "reason": "Not ready to move",
            })

            continue

        # -------------------------------------------------
        # Ownership Filter
        # -------------------------------------------------

        if (
            answers["ownership_required"]
            == "freehold"
            and project_data["ownership"]
            != "freehold"
        ):

            eliminated.append({
                "project": project_name,
                "reason": "Leasehold property",
            })

            continue

        # -------------------------------------------------
        # Property Type Filter
        # -------------------------------------------------

        if (
            project_data["property_type"]
            != answers["property_type"]
        ):

            eliminated.append({
                "project": project_name,
                "reason": "Property type mismatch",
            })

            continue

        # =================================================
        # SCORING
        # =================================================

        total_score = 0

        breakdown = {}

        for determinant, weight in normalized_weights.items():

            raw_score = (
                project_data["scores"][determinant]
            )

            contribution = round(
                raw_score * (weight / 10),
                2,
            )

            breakdown[determinant] = contribution

            total_score += contribution

        ranked.append({

            "project": project_name,

            "country": project_data["country"],

            "city": project_data["city"],

            "score": round(total_score, 1),

            "breakdown": breakdown,
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return (
        ranked,
        eliminated,
        normalized_weights,
        weight_log,
    )