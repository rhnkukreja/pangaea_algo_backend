import logging
from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

# ---------------------------------------------------------------------------
# Property data
# ---------------------------------------------------------------------------
PROPERTIES = [
    {"id": "ae1", "name": "Emaar Arlo",         "developer": "Emaar",    "country": "UAE",      "city": "Dubai",  "price_min": 400000,  "price_max": 900000,   "property_type": "apartment", "delivery_year": 2027, "roi_estimate": 6.5, "amenities": ["pool", "gym", "concierge"]},
    {"id": "ae2", "name": "Emaar Greencrest",    "developer": "Emaar",    "country": "UAE",      "city": "Dubai",  "price_min": 600000,  "price_max": 1400000,  "property_type": "villa",     "delivery_year": 2026, "roi_estimate": 5.8, "amenities": ["garden", "pool", "gym"]},
    {"id": "ae3", "name": "DAMAC Islands",       "developer": "DAMAC",    "country": "UAE",      "city": "Dubai",  "price_min": 800000,  "price_max": 2500000,  "property_type": "villa",     "delivery_year": 2028, "roi_estimate": 7.2, "amenities": ["beach", "marina", "spa"]},
    {"id": "ae4", "name": "Safa One",            "developer": "DAMAC",    "country": "UAE",      "city": "Dubai",  "price_min": 350000,  "price_max": 750000,   "property_type": "apartment", "delivery_year": 2025, "roi_estimate": 8.1, "amenities": ["sky pool", "gym", "views"]},
    {"id": "th1", "name": "Via Ari",             "developer": "Origin",   "country": "Thailand", "city": "Bangkok","price_min": 120000,  "price_max": 300000,   "property_type": "apartment", "delivery_year": 2026, "roi_estimate": 6.0, "amenities": ["pool", "coworking", "gym"]},
    {"id": "th2", "name": "XELF Rama IV",        "developer": "XELF",     "country": "Thailand", "city": "Bangkok","price_min": 90000,   "price_max": 220000,   "property_type": "apartment", "delivery_year": 2027, "roi_estimate": 5.5, "amenities": ["rooftop", "pool", "security"]},
    {"id": "th3", "name": "Monument Thong Lo",   "developer": "SC Asset", "country": "Thailand", "city": "Bangkok","price_min": 200000,  "price_max": 500000,   "property_type": "apartment", "delivery_year": 2025, "roi_estimate": 7.0, "amenities": ["sky lounge", "pool", "concierge"]},
    {"id": "th4", "name": "Ashton Asoke",        "developer": "Ananda",   "country": "Thailand", "city": "Bangkok","price_min": 150000,  "price_max": 380000,   "property_type": "apartment", "delivery_year": 2026, "roi_estimate": 6.8, "amenities": ["gym", "pool", "sky garden"]},
    {"id": "pt1", "name": "Amoreiras Prime",     "developer": "Vanguard", "country": "Portugal", "city": "Lisbon", "price_min": 280000,  "price_max": 650000,   "property_type": "apartment", "delivery_year": 2026, "roi_estimate": 4.5, "amenities": ["terrace", "concierge", "parking"]},
    {"id": "pt2", "name": "Infante Residences",  "developer": "Merlin",   "country": "Portugal", "city": "Lisbon", "price_min": 350000,  "price_max": 800000,   "property_type": "apartment", "delivery_year": 2027, "roi_estimate": 5.0, "amenities": ["river views", "gym", "rooftop"]},
    {"id": "pt3", "name": "The Lisboans",        "developer": "CBRE",     "country": "Portugal", "city": "Lisbon", "price_min": 450000,  "price_max": 1100000,  "property_type": "apartment", "delivery_year": 2025, "roi_estimate": 4.8, "amenities": ["heritage building", "pool", "spa"]},
    {"id": "pt4", "name": "Infinite Living",     "developer": "Habita",   "country": "Portugal", "city": "Porto",  "price_min": 200000,  "price_max": 480000,   "property_type": "townhouse", "delivery_year": 2026, "roi_estimate": 5.2, "amenities": ["garden", "terrace", "parking"]},
    {"id": "gr1", "name": "Marina Residences",   "developer": "Prodea",   "country": "Greece",   "city": "Athens", "price_min": 180000,  "price_max": 420000,   "property_type": "apartment", "delivery_year": 2026, "roi_estimate": 5.5, "amenities": ["sea views", "pool", "concierge"]},
    {"id": "gr2", "name": "Marina Galleria",     "developer": "Lamda",    "country": "Greece",   "city": "Athens", "price_min": 300000,  "price_max": 700000,   "property_type": "apartment", "delivery_year": 2027, "roi_estimate": 6.0, "amenities": ["marina", "retail", "gym"]},
    {"id": "gr3", "name": "One Athens",          "developer": "Dimand",   "country": "Greece",   "city": "Athens", "price_min": 250000,  "price_max": 600000,   "property_type": "apartment", "delivery_year": 2025, "roi_estimate": 5.8, "amenities": ["rooftop bar", "concierge", "gym"]},
    {"id": "gr4", "name": "Riviera Tower",       "developer": "Ellaktor", "country": "Greece",   "city": "Athens", "price_min": 220000,  "price_max": 520000,   "property_type": "apartment", "delivery_year": 2026, "roi_estimate": 6.2, "amenities": ["sea views", "spa", "pool"]},
]

# ---------------------------------------------------------------------------
# Survey answer → criteria mapping
# ---------------------------------------------------------------------------

# q2: budget range key → (min, max)
BUDGET_MAP = {
    "under_100k":   (0,        100_000),
    "100k_300k":    (100_000,  300_000),
    "300k_600k":    (300_000,  600_000),
    "600k_1m":      (600_000,  1_000_000),
    "1m_2m":        (1_000_000,2_000_000),
    "above_2m":     (2_000_000,10_000_000),
}

# q5: timeline key → years
TIMELINE_MAP = {
    "1_2": 2, "1-2": 2, "short": 2,
    "3_5": 5, "3-5": 5, "medium": 5,
    "5_plus": 7, "5+": 7, "long": 7,
}

# q6: lifestyle keyword → amenity keywords to match
LIFESTYLE_AMENITY_MAP = {
    "beach":          ["beach", "marina", "sea views"],
    "city":           ["concierge", "rooftop", "sky lounge", "views"],
    "golf":           ["golf", "garden", "terrace"],
    "family_friendly":["pool", "garden", "gym", "sky garden"],
    "wellness":       ["spa", "gym", "pool"],
    "urban":          ["concierge", "rooftop", "sky lounge"],
    "nature":         ["garden", "terrace", "views"],
}

# country name normalisation
COUNTRY_ALIASES = {
    "uae": "UAE", "dubai": "UAE", "united arab emirates": "UAE",
    "thailand": "Thailand", "bangkok": "Thailand",
    "portugal": "Portugal", "lisbon": "Portugal", "porto": "Portugal",
    "greece": "Greece", "athens": "Greece",
}

def _normalise_country(raw: str) -> str:
    return COUNTRY_ALIASES.get(raw.strip().lower(), raw.strip())

def _parse_answers(answers: dict) -> dict:
    """Map raw survey answers to matching criteria."""

    # --- budget (q2) ---
    budget_raw = answers.get("q2", "")
    if isinstance(budget_raw, dict):
        budget_min = float(budget_raw.get("min", 0))
        budget_max = float(budget_raw.get("max", 10_000_000))
    elif isinstance(budget_raw, str) and budget_raw in BUDGET_MAP:
        budget_min, budget_max = BUDGET_MAP[budget_raw]
    else:
        budget_min, budget_max = 0, 10_000_000  # no filter

    # --- countries (q3) ---
    raw_countries = answers.get("q3", [])
    if isinstance(raw_countries, str):
        raw_countries = [raw_countries]
    countries = [_normalise_country(c) for c in raw_countries]

    # --- property types (q4) ---
    raw_types = answers.get("q4", [])
    if isinstance(raw_types, str):
        raw_types = [raw_types]
    property_types = [t.strip().lower() for t in raw_types]

    # --- investment goal (q1) ---
    goal_raw = (answers.get("q1") or "").lower().replace(" ", "_")
    goal_map = {
        "capital_growth": "capital_growth",
        "capital_appreciation": "capital_growth",
        "rental_yield": "rental_yield",
        "rental": "rental_yield",
        "lifestyle": "lifestyle",
        "balanced": "balanced",
    }
    investment_goal = goal_map.get(goal_raw, "balanced")

    # --- lifestyle (q6) ---
    raw_lifestyle = answers.get("q6", [])
    if isinstance(raw_lifestyle, str):
        raw_lifestyle = [raw_lifestyle]
    lifestyle = [l.strip().lower() for l in raw_lifestyle]

    # --- timeline (q5) ---
    timeline_raw = answers.get("q5", "3_5")
    if isinstance(timeline_raw, (int, float)):
        timeline_years = int(timeline_raw)
    elif str(timeline_raw) in TIMELINE_MAP:
        timeline_years = TIMELINE_MAP[str(timeline_raw)]
    else:
        try:
            timeline_years = int(timeline_raw)
        except (ValueError, TypeError):
            timeline_years = 5

    return {
        "budget_min": budget_min,
        "budget_max": budget_max,
        "countries": countries,
        "property_types": property_types,
        "investment_goal": investment_goal,
        "lifestyle": lifestyle,
        "timeline_years": timeline_years,
    }

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _score(prop: dict, criteria: dict) -> tuple[float, list[str]]:
    score = 0.0
    reasons = []

    # Budget fit (30 pts)
    b_min, b_max = criteria["budget_min"] * 0.8, criteria["budget_max"] * 1.2
    overlap = min(criteria["budget_max"], prop["price_max"]) - max(criteria["budget_min"], prop["price_min"])
    budget_range = criteria["budget_max"] - criteria["budget_min"]
    if overlap > 0 and budget_range > 0:
        fit = min(overlap / budget_range, 1.0)
        score += 30 * fit
        reasons.append(f"Budget fit")

    # Investment goal (30 pts)
    goal = criteria["investment_goal"]
    if goal == "rental_yield":
        roi_score = min(prop["roi_estimate"] / 8.0, 1.0)
        score += 30 * roi_score
        reasons.append(f"ROI {prop['roi_estimate']}%")
    elif goal == "capital_growth":
        mkt = {"UAE": 1.0, "Greece": 0.9, "Portugal": 0.8, "Thailand": 0.75}.get(prop["country"], 0.5)
        score += 30 * mkt
        reasons.append(f"{prop['country']} strong for capital growth")
    else:
        score += 20
        reasons.append("Lifestyle match")

    # Timeline (20 pts)
    delivery_in = prop["delivery_year"] - 2025
    if delivery_in <= criteria["timeline_years"]:
        score += 20
        reasons.append(f"Delivers {prop['delivery_year']}")
    elif delivery_in <= criteria["timeline_years"] + 1:
        score += 10
        reasons.append(f"Delivers {prop['delivery_year']} (slight stretch)")

    # Lifestyle amenities (20 pts)
    lifestyle = criteria["lifestyle"]
    if lifestyle:
        hits = sum(
            1 for pref in lifestyle
            if any(kw in a.lower() for kw in LIFESTYLE_AMENITY_MAP.get(pref, [pref]) for a in prop["amenities"])
        )
        lifestyle_score = min(hits / len(lifestyle), 1.0)
        score += 20 * lifestyle_score
        if hits:
            reasons.append("Amenities match lifestyle")

    return round(score, 1), reasons

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class SurveyRequest(BaseModel):
    # new survey format
    answers: dict | None = None
    # legacy flat format
    budget_min: float | None = None
    budget_max: float | None = None
    countries: list[str] | None = None
    property_type: list[str] | None = None
    investment_goal: str | None = None
    lifestyle_priorities: list[str] | None = None
    timeline_years: int | None = None

class PropertyResult(BaseModel):
    id: str
    name: str
    developer: str
    location: str
    priceRange: str
    matchScore: float
    reasoning: str
    image: str

class MatchResponse(BaseModel):
    properties: list[PropertyResult]

# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

def _fmt_price(n: int) -> str:
    if n >= 1_000_000:
        return f"${n / 1_000_000:.1f}M"
    return f"${n // 1000}K"

def _criteria_from_legacy(req: SurveyRequest) -> dict:
    """Convert flat legacy payload into the same criteria dict as _parse_answers."""
    goal_map = {
        "capital_growth": "capital_growth", "capital_appreciation": "capital_growth",
        "rental_yield": "rental_yield", "rental": "rental_yield",
        "lifestyle": "lifestyle", "balanced": "balanced",
    }
    goal_raw = (req.investment_goal or "balanced").lower().replace(" ", "_")
    timeline = req.timeline_years or 5
    return {
        "budget_min":      req.budget_min or 0,
        "budget_max":      req.budget_max or 10_000_000,
        "countries":       [_normalise_country(c) for c in (req.countries or [])],
        "property_types":  [t.strip().lower() for t in (req.property_type or [])],
        "investment_goal": goal_map.get(goal_raw, "balanced"),
        "lifestyle":       [l.strip().lower() for l in (req.lifestyle_priorities or [])],
        "timeline_years":  timeline,
    }


@router.post("/match", response_model=MatchResponse)
async def match_properties(req: SurveyRequest):
    if req.answers:
        logger.info("POST /api/match (survey format) answers: %s", req.answers)
        criteria = _parse_answers(req.answers)
    else:
        logger.info("POST /api/match (legacy format): %s", req.model_dump(exclude_none=True))
        criteria = _criteria_from_legacy(req)
    logger.info(
        "Parsed criteria → budget: $%s–$%s | countries: %s | types: %s | goal: %s | lifestyle: %s | timeline: %d yrs",
        criteria["budget_min"], criteria["budget_max"],
        criteria["countries"], criteria["property_types"],
        criteria["investment_goal"], criteria["lifestyle"],
        criteria["timeline_years"],
    )

    b_low  = criteria["budget_min"] * 0.8
    b_high = criteria["budget_max"] * 1.2
    timeline_cutoff = 2025 + criteria["timeline_years"] + 1  # +1 buffer

    # Step 2 – filter (target 10-12)
    candidates = [
        p for p in PROPERTIES
        if (not criteria["countries"]     or p["country"]       in criteria["countries"])
        and (not criteria["property_types"] or p["property_type"] in criteria["property_types"])
        and p["price_min"] <= b_high
        and p["price_max"] >= b_low
        and p["delivery_year"] <= timeline_cutoff
    ]
    logger.info("After filtering: %d candidates — %s", len(candidates), [p["name"] for p in candidates])

    # Step 3 – score & rank
    scored = sorted(
        [{"prop": p, "score": _score(p, criteria)} for p in candidates],
        key=lambda x: x["score"][0],
        reverse=True,
    )[:4]
    logger.info("Top matches: %s", [(s["prop"]["name"], s["score"][0]) for s in scored])

    results = []
    for s in scored:
        p, (score, reasons) = s["prop"], s["score"]
        results.append(PropertyResult(
            id=p["id"],
            name=p["name"],
            developer=p["developer"],
            location=f"{p['city']}, {p['country']}",
            priceRange=f"{_fmt_price(p['price_min'])} – {_fmt_price(p['price_max'])}",
            matchScore=score,
            reasoning=" · ".join(reasons) if reasons else "General match",
            image="",
        ))

    return MatchResponse(properties=results)
