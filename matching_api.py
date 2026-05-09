import logging
from fastapi import APIRouter
from pydantic import BaseModel
from matching_engine import match, get_funnel_stats

logger = logging.getLogger(__name__)
router = APIRouter()

# ---------------------------------------------------------------------------
# Survey answer mappings
# ---------------------------------------------------------------------------

BUDGET_MAP = {
    "< 5 Crore":       {"budget_inr_crore": 5.0,   "budget_usd": round(5   * 10_000_000 / 84)},
    "5–10 Crore":      {"budget_inr_crore": 10.0,  "budget_usd": round(10  * 10_000_000 / 84)},
    "10–15 Crore":     {"budget_inr_crore": 15.0,  "budget_usd": round(15  * 10_000_000 / 84)},
    "< 15 Crore":      {"budget_inr_crore": 15.0,  "budget_usd": round(15  * 10_000_000 / 84)},
    "15–25 Crore":     {"budget_inr_crore": 25.0,  "budget_usd": round(25  * 10_000_000 / 84)},
    "25–50 Crore":     {"budget_inr_crore": 50.0,  "budget_usd": round(50  * 10_000_000 / 84)},
    "50 Crore+":       {"budget_inr_crore": 75.0,  "budget_usd": round(75  * 10_000_000 / 84)},
    "50+ Crore":       {"budget_inr_crore": 75.0,  "budget_usd": round(75  * 10_000_000 / 84)},
}

COUNTRY_MAP = {
    "Portugal": "PT",
    "Greece":   "GR",
    "Thailand": "TH",
    "UAE":      "AE",
    "PT": "PT", "GR": "GR", "TH": "TH", "AE": "AE",
}


def _map_survey_to_profile(answers: dict) -> dict:
    # Q1 — budget
    q1_raw = answers.get("q1", "")
    budget_entry = BUDGET_MAP.get(q1_raw, {"budget_inr_crore": 15.0, "budget_usd": round(15 * 10_000_000 / 84)})

    # Q2 — investment objective
    investment_objective = answers.get("q2", "")

    # Q5 — golden visa requirement
    q5_raw = answers.get("q5", "")
    requires_golden_visa = q5_raw == "Mandatory"

    # Q7 — ownership preference
    q7_raw = answers.get("q7", "")
    requires_freehold = q7_raw == "Freehold"

    # Q8 — risk appetite
    risk_appetite = answers.get("q8", "Moderate")

    # Q11 — family composition
    family_composition = answers.get("q11", "Single / couple")

    # Q13 — preferred countries (list of display names → ISO codes)
    raw_countries = answers.get("q13", [])
    if isinstance(raw_countries, str):
        raw_countries = [raw_countries]
    preferred_countries = [COUNTRY_MAP[c] for c in raw_countries if c in COUNTRY_MAP]

    # Q14 — proximity preferences (list, passed through directly)
    proximity_preferences = answers.get("q14", [])
    if isinstance(proximity_preferences, str):
        proximity_preferences = [proximity_preferences]

    return {
        "budget_inr_crore":     budget_entry["budget_inr_crore"],
        "budget_usd":           budget_entry["budget_usd"],
        "investment_objective": investment_objective,
        "requires_golden_visa": requires_golden_visa,
        "requires_freehold":    requires_freehold,
        "risk_appetite":        risk_appetite,
        "preferred_countries":  preferred_countries,
        "proximity_preferences": proximity_preferences,
        "family_composition":   family_composition,
        "investment_timeline":  answers.get("q15", ""),
    }


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class SurveyV2Request(BaseModel):
    answers: dict


class MatchV2Response(BaseModel):
    funnel: dict
    top_matches: list[dict]


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.post("/match/v2", response_model=MatchV2Response)
async def match_v2(req: SurveyV2Request):
    logger.info("POST /api/match/v2 raw answers: %s", req.answers)

    profile = _map_survey_to_profile(req.answers)
    logger.info(
        "Mapped profile -> budget_usd=%s | objective=%s | visa=%s | freehold=%s | "
        "risk=%s | countries=%s | family=%s",
        profile["budget_usd"], profile["investment_objective"],
        profile["requires_golden_visa"], profile["requires_freehold"],
        profile["risk_appetite"], profile["preferred_countries"],
        profile["family_composition"],
    )

    results = match(profile)
    stats = get_funnel_stats(results)

    top_matches = stats["step3_ranked"][:4]
    logger.info(
        "Funnel: step1_eliminated=%d, step2_eliminated=%d, step3_ranked=%d, top_matches=%s",
        len(stats["step1_eliminated"]), len(stats["step2_eliminated"]),
        len(stats["step3_ranked"]), [p["project_name"] for p in top_matches],
    )

    return MatchV2Response(
        funnel={
            "step1": stats["step1_eliminated"],
            "step2": stats["step2_eliminated"],
            "step3": stats["step3_ranked"],
        },
        top_matches=top_matches,
    )
