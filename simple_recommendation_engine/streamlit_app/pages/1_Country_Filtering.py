import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from country_engine import rank_countries, COUNTRIES
from weights_config import COUNTRY_BASELINE_WEIGHTS, compute_country_weights

st.set_page_config(page_title="Country Filtering", layout="wide")

if "country_answers" not in st.session_state:
    st.session_state.country_answers = {}
if "city_answers" not in st.session_state:
    st.session_state.city_answers = {}
if "surviving_countries" not in st.session_state:
    st.session_state.surviving_countries = []

PERSONAS = {
    "Capital Appreciation": {
        "primary_objective": "capital_appreciation",
        "visa_required": "optional",
        "citizenship_required": "no",
        "budget_usd": 1000000,
        "risk_appetite": "moderate",
        "ownership_structure": "any",
    },

    "Yield / Cash Flow": {
        "primary_objective": "yield_cash_flow",
        "visa_required": "optional",
        "citizenship_required": "no",
        "budget_usd": 600000,
        "risk_appetite": "opportunistic",
        "ownership_structure": "any",
    },

    "Capital Preservation": {
        "primary_objective": "capital_preservation",
        "visa_required": "optional",
        "citizenship_required": "no",
        "budget_usd": 1500000,
        "risk_appetite": "conservative",
        "ownership_structure": "freehold_only",
    },

    "Investment Diversification": {
        "primary_objective": "investment_diversification",
        "visa_required": "optional",
        "citizenship_required": "no",
        "budget_usd": 1200000,
        "risk_appetite": "moderate",
        "ownership_structure": "any",
    },

    "Residency / Citizenship": {
        "primary_objective": "residency_citizenship",
        "visa_required": "mandatory",
        "citizenship_required": "yes",
        "budget_usd": 1500000,
        "risk_appetite": "moderate",
        "ownership_structure": "freehold_only",
    },

    "Custom": None,
}

BUDGET_OPTIONS = [150000, 300000, 500000, 800000, 1000000, 1500000, 3000000, 5000000]

st.title("Country Filtering")
st.caption("Page 1 of 2 — Filter and rank countries based on investor profile")

preset = st.selectbox("Load a persona preset", options=list(PERSONAS.keys()), index=0)

if PERSONAS[preset] and st.button("Apply preset"):
    p = PERSONAS[preset]
    st.session_state["country_primary_objective"] = p["primary_objective"]
    st.session_state["country_visa_required"] = p["visa_required"]
    st.session_state["country_citizenship_required"] = p["citizenship_required"]
    budget = p["budget_usd"]
    st.session_state["country_budget_usd"] = budget if budget in BUDGET_OPTIONS else BUDGET_OPTIONS[0]
    st.session_state["country_risk_appetite"] = p["risk_appetite"]
    st.session_state["country_ownership_structure"] = p["ownership_structure"]
    st.rerun()

col_form, col_weights, col_results = st.columns([1, 1, 1.2])

with col_form:
    st.subheader("Investor Profile")

    primary_objective = st.selectbox(
    "Q1 — Primary Investment Objective",
    [
        "capital_appreciation", "yield_cash_flow", "capital_preservation",  "investment_diversification", "residency_citizenship",
    ],
    key="country_primary_objective",
)

    visa_required = st.radio(
        "Q2 — Visa / Residency Requirement",
        ["mandatory", "optional", "no"],
        key="country_visa_required",
    )

    citizenship_required = st.radio(
        "Q3 — Citizenship Requirement",
        ["yes", "optional", "no"],
        key="country_citizenship_required",
    )

    budget_usd = st.select_slider(
        "Q4 — Budget (USD)",
        options=BUDGET_OPTIONS,
        format_func=lambda x: f"${x:,}",
        key="country_budget_usd",
    )

    risk_appetite = st.radio(
        "Q5 — Risk Appetite",
        ["conservative", "moderate", "opportunistic"],
        key="country_risk_appetite",
    )

    ownership_structure = st.radio(
        "Q6 — Ownership Type",
        ["any", "freehold_only"],
        format_func=lambda x: {
            "any": "Any (freehold or leasehold)",
            "freehold_only": "Freehold only — eliminates countries that restrict foreign ownership to leasehold",
        }[x],
        key="country_ownership_structure",
    )

answers = {
    "primary_objective": primary_objective,
    "visa_required": visa_required,
    "citizenship_required": citizenship_required,
    "budget_usd": budget_usd,
    "risk_appetite": risk_appetite,
    "ownership_structure": ownership_structure,
}

ranked, eliminated, normalized_weights, weight_log = rank_countries(answers)

st.session_state.country_answers = answers
st.session_state.surviving_countries = [r["country"] for r in ranked]

with col_weights:
    st.subheader("Determinant Weights")
    st.caption("How investor answers reshape the country scoring weights")

    rows = []
    for determinant, baseline in COUNTRY_BASELINE_WEIGHTS.items():
        final = normalized_weights.get(determinant, 0)
        delta = round(final - baseline, 1)
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        rows.append({
            "Determinant": determinant.replace("_", " ").title(),
            "Baseline": f"{baseline}%",
            "Final": f"{final}%",
            "Δ": delta_str,
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, use_container_width=True)

    with st.expander("📋 Why these weights changed"):
        _, _, weight_log = compute_country_weights(answers)

        if not weight_log:
            st.caption("No shifts applied — using baseline weights.")
        else:
            for entry in weight_log:
                tier = entry.get("tier", "")
                det = entry.get("determinant", "").replace("_", " ").title()
                raw = entry.get("raw_shift", 0)
                adj = entry.get("adjusted_shift", 0)
                before = entry.get("before", 0)
                after = entry.get("after", 0)

                sign = "+" if raw > 0 else ""
                color = "🟢" if raw > 0 else "🔴"

                st.markdown(
                    f"{color} **{det}** ({tier}) — "
                    f"Raw shift: {sign}{raw} → "
                    f"Adjusted: {sign}{round(adj, 2)} → "
                    f"{round(before, 1)}% → **{round(after, 1)}%**"
                )




with col_results:
    st.subheader("Ranked Countries")
    st.caption(f"{len(ranked)} of {len(COUNTRIES)} countries survived hard filters")

    for idx, item in enumerate(ranked, 1):
        with st.container(border=True):
            top = st.columns([1, 4, 2])
            with top[0]:
                st.markdown(f"### #{idx}")
            with top[1]:
                st.markdown(f"**{item['country']}**")
                country_meta = COUNTRIES[item["country"]]
                freehold_label = "✅ Freehold" if country_meta.get("foreign_freehold_allowed") else "⚠️ Leasehold only"
                st.caption(f"Region: {country_meta['region']} · {freehold_label}")
            with top[2]:
                score = item["score"]
                color = "#22c55e" if score > 70 else "#f59e0b" if score > 50 else "#a0a0a0"
                st.markdown(
                    f"<h3 style='color:{color};text-align:right;margin:0'>{score}</h3>",
                    unsafe_allow_html=True,
                )

            with st.expander("Score breakdown"):
                country_data = country_meta
                raw_data = country_data.get("raw_values", {})
                raw_lookup = {
                    "political_stability_index": ("political_stability_index_raw", "WGI -2.5 to +2.5"),
                    "corruption_perception_index": ("corruption_perception_index_raw", "CPI 0-100"),
                    "currency_volatility": ("currency_volatility_pct", "% stdev"),
                    "interest_rate_direction": ("interest_rate_direction_pp", "pp change"),
                    "foreign_buyer_market_share": ("foreign_buyer_market_share_pct", "% of market"),
                    "property_taxation_for_foreigners": (None, "qualitative"),
                }
                for determinant, contribution in item["breakdown"].items():
                    weight = normalized_weights[determinant]
                    raw_score = country_data["scores"][determinant]
                    raw_key, unit = raw_lookup.get(determinant, (None, ""))
                    raw_str = (
                        f" — raw: {raw_data.get(raw_key)} ({unit})"
                        if raw_key
                        else f" — {unit}"
                    )
                    st.caption(
                        f"**{determinant.replace('_', ' ').title()}**: {contribution} pts"
                        f"  ({raw_score}/10 × {weight}%){raw_str}"
                    )
                tax = raw_data.get("tax_summary")
                if tax:
                    st.caption(f"💰 Tax: {tax}")

    if eliminated:
        with st.expander(f"❌ Eliminated countries ({len(eliminated)})"):
            for e in eliminated:
                st.caption(f"**{e['country']}** — {e['reason']}")

st.markdown("---")
st.info(
    f"✅ **{len(ranked)} countries** are ready for city-level filtering. "
    "Navigate to **City Filtering** in the sidebar to continue."
)
