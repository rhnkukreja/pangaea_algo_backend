"""
Deterministic 3-step investor-property matching engine.
No LLM, no Pinecone. Pure scoring logic.

Entry points:
  match(profile: dict) -> list[dict]
  get_funnel_stats(results: list[dict]) -> dict
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Property data  (all prices in USD; EUR converted at *1.08)
# ---------------------------------------------------------------------------

PROPERTIES: list[dict] = [
    {
        "id": "pt1",
        "project_name": "Palmares Ocean Living & Golf Resort",
        "country": "PT",
        "city": "Algarve",
        "project_type": "Mixed-use",
        "project_stage": "Under Construction",
        "min_ticket_usd": 214_920,
        "max_ticket_usd": 1_188_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 5.5,
        "expected_annual_returns_percent": None,
        "area_type": "Established",
        "nearby_infrastructure": "golf course, beach, airport 40 min",
        "price_positioning": "Mid-range",
    },
    {
        "id": "pt2",
        "project_name": "Infante Residences",
        "country": "PT",
        "city": "Lisbon",
        "project_type": "Residential",
        "project_stage": "Under Construction",
        "min_ticket_usd": round(431_280 * 1.08),   # EUR → USD
        "max_ticket_usd": 1_096_200,
        "golden_visa_linked": False,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 4.8,
        "expected_annual_returns_percent": None,
        "area_type": "Prime",
        "nearby_infrastructure": "schools, hospitals, metro, airport 30 min",
        "price_positioning": "Premium",
    },
    {
        "id": "gr1",
        "project_name": "LUX&EASY Thessaloniki",
        "country": "GR",
        "city": "Thessaloniki",
        "project_type": "Residential",
        "project_stage": "Under Construction",
        "min_ticket_usd": 129_600,
        "max_ticket_usd": 259_200,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 6.0,
        "expected_annual_returns_percent": None,
        "area_type": "Emerging",
        "nearby_infrastructure": "port, airport 15 min, university",
        "price_positioning": "Entry-level",
    },
    {
        "id": "gr2",
        "project_name": "One Athens",
        "country": "GR",
        "city": "Athens",
        "project_type": "Residential",
        "project_stage": "Ready to Move",
        "min_ticket_usd": 216_000,
        "max_ticket_usd": 4_860_000,
        "golden_visa_linked": False,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 5.8,
        "expected_annual_returns_percent": None,
        "area_type": "Prime",
        "nearby_infrastructure": "schools, metro, hospital, acropolis",
        "price_positioning": "Mid-range to Premium",
    },
    {
        "id": "gr3",
        "project_name": "The Ellinikon – Marina Residences",
        "country": "GR",
        "city": "Athens",
        "project_type": "Residential",
        "project_stage": "Under Construction",
        "min_ticket_usd": 1_080_000,
        "max_ticket_usd": 21_600_000,
        "golden_visa_linked": False,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 5.0,
        "expected_annual_returns_percent": None,
        "area_type": "Emerging",
        "nearby_infrastructure": "marina, beach, airport 10 min",
        "price_positioning": "Ultra-premium",
    },
    {
        "id": "pt3",
        "project_name": "The Lisboans",
        "country": "PT",
        "city": "Lisbon",
        "project_type": "Mixed-use",
        "project_stage": "Ready to Move",
        "min_ticket_usd": 486_000,
        "max_ticket_usd": 2_700_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 5.2,
        "expected_annual_returns_percent": None,
        "area_type": "Prime",
        "nearby_infrastructure": "schools, metro, river front, hospital",
        "price_positioning": "Premium",
    },
    {
        "id": "pt4",
        "project_name": "Amoreiras Prime Residences",
        "country": "PT",
        "city": "Lisbon",
        "project_type": "Residential",
        "project_stage": "Ready to Move",
        "min_ticket_usd": 810_000,
        "max_ticket_usd": 3_780_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 4.5,
        "expected_annual_returns_percent": None,
        "area_type": "Prime",
        "nearby_infrastructure": "schools, hospital, metro, shopping",
        "price_positioning": "Premium",
    },
    {
        "id": "th1",
        "project_name": "Noble Ploenchit",
        "country": "TH",
        "city": "Bangkok",
        "project_type": "Residential",
        "project_stage": "Ready to Move",
        "min_ticket_usd": round(8_500_000 / 35),    # THB -> USD
        "max_ticket_usd": round(185_000_000 / 35),
        "golden_visa_linked": False,
        "ownership_structure": "Leasehold",
        "rental_yield_estimate_percent": 4.5,
        "expected_annual_returns_percent": None,
        "area_type": "Prime",
        "nearby_infrastructure": "BTS skytrain, hospital, schools, airport link",
        "price_positioning": "Ultra-premium",
    },
    {
        "id": "th2",
        "project_name": "The Monument Thong Lo",
        "country": "TH",
        "city": "Bangkok",
        "project_type": "Residential",
        "project_stage": "Ready to Move",
        "min_ticket_usd": round(30_000_000 / 35),   # THB -> USD
        "max_ticket_usd": round(150_000_000 / 35),
        "golden_visa_linked": False,
        "ownership_structure": "Leasehold",
        "rental_yield_estimate_percent": 4.2,
        "expected_annual_returns_percent": None,
        "area_type": "Prime",
        "nearby_infrastructure": "BTS skytrain, schools, hospital, restaurants",
        "price_positioning": "Ultra-premium",
    },
    {
        "id": "th3",
        "project_name": "HYTHE by Botanica",
        "country": "TH",
        "city": "Phuket",
        "project_type": "Residential",
        "project_stage": "Under Construction",
        "min_ticket_usd": round(10_800_000 / 35),   # THB -> USD
        "max_ticket_usd": round(165_000_000 / 35),
        "golden_visa_linked": False,
        "ownership_structure": "Leasehold",
        "rental_yield_estimate_percent": 6.0,
        "expected_annual_returns_percent": None,
        "area_type": "Established",
        "nearby_infrastructure": "beach, golf, airport 30 min",
        "price_positioning": "Ultra-premium",
    },
    {
        "id": "th4",
        "project_name": "Laguna Lakelands",
        "country": "TH",
        "city": "Phuket",
        "project_type": "Mixed-use",
        "project_stage": "Under Construction",
        "min_ticket_usd": round(6_800_000 / 35),    # THB -> USD
        "max_ticket_usd": round(60_000_000 / 35),
        "golden_visa_linked": False,
        "ownership_structure": "Leasehold",
        "rental_yield_estimate_percent": 6.5,
        "expected_annual_returns_percent": None,
        "area_type": "Established",
        "nearby_infrastructure": "beach, golf, lagoon, airport 45 min",
        "price_positioning": "Premium",
    },
    {
        "id": "ae1",
        "project_name": "Sobha Hartland",
        "country": "AE",
        "city": "Dubai",
        "project_type": "Mixed-use",
        "project_stage": "Under Construction",
        "min_ticket_usd": 1_200_000,
        "max_ticket_usd": 85_000_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 6.5,
        "expected_annual_returns_percent": None,
        "area_type": "Established",
        "nearby_infrastructure": "schools, hospital, metro, downtown 10 min",
        "price_positioning": "Premium",
    },
    {
        "id": "ae2",
        "project_name": "Burj Binghatti Jacob & Co",
        "country": "AE",
        "city": "Dubai",
        "project_type": "Residential",
        "project_stage": "Under Construction",
        "min_ticket_usd": 8_200_000,
        "max_ticket_usd": 752_000_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": None,
        "expected_annual_returns_percent": None,
        "area_type": "Prime",
        "nearby_infrastructure": "burj khalifa, mall, metro, airport 20 min",
        "price_positioning": "Ultra-premium",
    },
    {
        "id": "ae3",
        "project_name": "DAMAC Islands",
        "country": "AE",
        "city": "Dubai",
        "project_type": "Mixed-use",
        "project_stage": "Under Construction",
        "min_ticket_usd": 2_250_000,
        "max_ticket_usd": 9_500_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 6.0,
        "expected_annual_returns_percent": None,
        "area_type": "Emerging",
        "nearby_infrastructure": "beach, marina, airport 35 min",
        "price_positioning": "Premium",
    },
    {
        "id": "ae4",
        "project_name": "Greencrest at Dubai Hills Estate",
        "country": "AE",
        "city": "Dubai",
        "project_type": "Residential",
        "project_stage": "Under Construction",
        "min_ticket_usd": 1_570_000,
        "max_ticket_usd": 3_890_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 6.5,
        "expected_annual_returns_percent": None,
        "area_type": "Established",
        "nearby_infrastructure": "schools, hospital, golf, mall, metro",
        "price_positioning": "Premium",
    },
    {
        "id": "ae5",
        "project_name": "Dubai Creek Harbour",
        "country": "AE",
        "city": "Dubai",
        "project_type": "Mixed-use",
        "project_stage": "Under Construction",
        "min_ticket_usd": 1_200_000,
        "max_ticket_usd": 15_000_000,
        "golden_visa_linked": True,
        "ownership_structure": "Freehold",
        "rental_yield_estimate_percent": 6.5,
        "expected_annual_returns_percent": 20.0,
        "area_type": "Emerging",
        "nearby_infrastructure": "creek, airport 15 min, downtown 10 min, metro",
        "price_positioning": "Mid-range to Premium",
    },
]


# ---------------------------------------------------------------------------
# Step 1 — Hard Knockouts
# ---------------------------------------------------------------------------

def _step1_knockout(prop: dict, profile: dict) -> str | None:
    budget = profile.get("budget_usd", 0)
    if budget < prop["min_ticket_usd"]:
        return "budget_below_minimum"
    if profile.get("risk_appetite") == "Conservative" and prop["min_ticket_usd"] > 5_000_000:
        return "premium_tier_mismatch"
    return None


# ---------------------------------------------------------------------------
# Step 2 — Soft Disqualifiers
# ---------------------------------------------------------------------------

def _step2_disqualify(prop: dict, profile: dict) -> str | None:
    preferred = profile.get("preferred_countries", [])
    if preferred and prop["country"] not in preferred:
        return "country_not_preferred"
    if profile.get("requires_golden_visa") and not prop["golden_visa_linked"]:
        return "no_golden_visa_program"
    if profile.get("requires_freehold") and prop["ownership_structure"] != "Freehold":
        return "ownership_not_freehold"
    return None


# ---------------------------------------------------------------------------
# Step 3 — Scoring
# ---------------------------------------------------------------------------

def _step3_score(prop: dict, profile: dict) -> tuple[int, list[str]]:
    score = 50
    breakdown: list[str] = ["base +50"]

    preferred = profile.get("preferred_countries", [])
    objective = profile.get("investment_objective", "")
    risk = profile.get("risk_appetite", "")
    proximity = profile.get("proximity_preferences", [])
    family = profile.get("family_composition", "")
    infra = prop["nearby_infrastructure"].lower()

    if prop["country"] in preferred:
        score += 30
        breakdown.append("country_match +30")

    if profile.get("requires_golden_visa") and prop["golden_visa_linked"]:
        score += 20
        breakdown.append("golden_visa +20")

    if prop["project_type"] == "Mixed-use" and objective in ("Yield / Cash Flow", "Residency"):
        score += 15
        breakdown.append(f"mixed_use_matches_{objective.lower().replace(' ', '_')} +15")

    if prop["project_stage"] == "Under Construction" and risk == "Opportunistic":
        score += 10
        breakdown.append("under_construction_opportunistic +10")

    if prop["project_stage"] == "Ready to Move" and risk == "Conservative":
        score += 10
        breakdown.append("ready_to_move_conservative +10")

    if "schools" in infra and family == "Family with children":
        score += 10
        breakdown.append("schools_nearby_family +10")

    if "hospital" in infra and "Schools / hospitals" in proximity:
        score += 10
        breakdown.append("hospital_proximity +10")

    if "airport" in infra and "Airport connectivity" in proximity:
        score += 5
        breakdown.append("airport_connectivity +5")

    if prop["rental_yield_estimate_percent"] is not None and objective == "Yield / Cash Flow":
        score += 5
        breakdown.append(f"rental_yield_{prop['rental_yield_estimate_percent']}pct +5")

    if prop["area_type"] == "Emerging" and risk == "Conservative":
        score -= 10
        breakdown.append("emerging_area_conservative -10")

    return score, breakdown


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def match(profile: dict) -> list[dict]:
    """
    Run 3-step matching for a given investor profile.
    Returns ALL 16 properties — eliminated ones carry step/reason, survivors carry score.
    """
    results = []

    for prop in PROPERTIES:
        result: dict = {
            "project_name":      prop["project_name"],
            "country":           prop["country"],
            "city":              prop["city"],
            "min_ticket_usd":    prop["min_ticket_usd"],
            "max_ticket_usd":    prop["max_ticket_usd"],
            "score":             None,
            "step_eliminated":   None,
            "elimination_reason": None,
            "score_breakdown":   [],
        }

        reason = _step1_knockout(prop, profile)
        if reason:
            result["step_eliminated"] = 1
            result["elimination_reason"] = reason
            results.append(result)
            continue

        reason = _step2_disqualify(prop, profile)
        if reason:
            result["step_eliminated"] = 2
            result["elimination_reason"] = reason
            results.append(result)
            continue

        score, breakdown = _step3_score(prop, profile)
        result["score"] = score
        result["score_breakdown"] = breakdown
        results.append(result)

    # sort survivors by score desc, eliminated go after
    results.sort(key=lambda r: (r["step_eliminated"] is not None, -(r["score"] or 0)))
    return results


def get_funnel_stats(results: list[dict]) -> dict:
    step1 = [r for r in results if r["step_eliminated"] == 1]
    step2 = [r for r in results if r["step_eliminated"] == 2]
    step3 = [r for r in results if r["step_eliminated"] is None]
    return {
        "step1_eliminated": step1,
        "step2_eliminated": step2,
        "step3_ranked":     sorted(step3, key=lambda r: -(r["score"] or 0)),
    }
