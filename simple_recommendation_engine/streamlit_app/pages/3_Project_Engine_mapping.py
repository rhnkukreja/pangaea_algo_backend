import streamlit as st
import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    ),
)

import pandas as pd

from project_engine import (
    rank_projects,
    PROJECTS,
    PROJECT_BASELINE_WEIGHTS,
)

st.set_page_config(
    page_title="Project Engine Mapping",
    layout="wide",
)

# =========================================================
# VALIDATION
# =========================================================

if (
    "surviving_countries" not in st.session_state
    or not st.session_state.surviving_countries
):
    st.warning(
        "⚠️ Please complete Country Filtering first."
    )
    st.stop()

# =========================================================
# PAGE HEADER
# =========================================================

st.title("Project Engine Mapping")

st.caption(
    "Page 3 of 3 — Dynamic project ranking "
    "using the Cascading Archetype Model"
)

# =========================================================
# BUDGET OPTIONS
# =========================================================

BUDGET_OPTIONS = [
    150000,
    300000,
    500000,
    800000,
    1000000,
    1500000,
    3000000,
    5000000,
    10000000,
]

# =========================================================
# LAYOUT
# =========================================================

col_form, col_weights, col_results = st.columns(
    [1, 1, 1.2]
)

# =========================================================
# INVESTOR PROFILE
# =========================================================

with col_form:

    st.subheader("Investor Profile")

    budget = st.select_slider(
        "Budget (USD)",
        options=BUDGET_OPTIONS,
        format_func=lambda x: f"${x:,}",
        value=800000,
        key="project_budget",
    )

    ready_to_move = st.radio(
        "Ready To Move Required?",
        ["yes", "no"],
        format_func=lambda x: {
            "yes": "Yes",
            "no": "No",
        }[x],
    )

    ownership_required = st.radio(
        "Ownership Requirement",
        ["freehold", "any"],
        format_func=lambda x: {
            "freehold": "Freehold Only",
            "any": "Any",
        }[x],
    )

    property_type = st.selectbox(
        "Property Type",
        [
            "Apartment",
            "Villa",
            "Managed",
            "Branded",
        ],
    )

    st.markdown("---")

    usage_intent = st.selectbox(
        "Usage Intent",
        [
            "pure_investment",
            "investment_occasional_use",
            "primary_relocation",
        ],
        format_func=lambda x: {
            "pure_investment": "Pure Investment",
            "investment_occasional_use":
                "Investment + Occasional Use",
            "primary_relocation":
                "Primary Relocation",
        }[x],
    )

    holding_period = st.radio(
        "Holding Period",
        [
            "short_term",
            "medium_term",
            "long_term",
        ],
        format_func=lambda x: {
            "short_term": "Short (<3 years)",
            "medium_term": "Medium (3–7 years)",
            "long_term": "Long (>7 years)",
        }[x],
    )

    liquidity_preference = st.radio(
        "Liquidity Preference",
        [
            "high_resale",
            "long_lockin",
        ],
        format_func=lambda x: {
            "high_resale":
                "High Resale Liquidity",

            "long_lockin":
                "Long Lock-in Acceptable",
        }[x],
    )

    risk_appetite = st.radio(
        "Risk Appetite",
        [
            "conservative",
            "opportunistic",
        ],
        format_func=lambda x: x.title(),
    )

    investor_experience = st.radio(
        "Investor Experience",
        [
            "first_purchase",
            "experienced",
        ],
        format_func=lambda x: {
            "first_purchase":
                "First International Purchase",

            "experienced":
                "Experienced Investor",
        }[x],
    )

    prestige_sensitivity = st.radio(
        "Prestige / Brand Sensitivity",
        [
            "high",
            "low",
        ],
        format_func=lambda x: x.title(),
    )

    proximity_preferences = st.radio(
        "Proximity Preference",
        [
            "airport_cbd_leisure",
            "schools_hospitals",
        ],
        format_func=lambda x: {
            "airport_cbd_leisure":
                "Airport / CBD / Leisure",

            "schools_hospitals":
                "Schools / Hospitals",
        }[x],
    )

    family_composition = st.radio(
        "Family Composition",
        [
            "single_couple",
            "family_multi_gen",
        ],
        format_func=lambda x: {
            "single_couple":
                "Single / Couple",

            "family_multi_gen":
                "Family / Multi-generational",
        }[x],
    )

# =========================================================
# ANSWERS
# =========================================================

project_answers = {

    "budget": budget,

    "ready_to_move": ready_to_move,

    "ownership_required": ownership_required,

    "property_type": property_type,

    "usage_intent": usage_intent,

    "holding_period": holding_period,

    "liquidity_preference":
        liquidity_preference,

    "risk_appetite": risk_appetite,

    "investor_experience":
        investor_experience,

    "prestige_sensitivity":
        prestige_sensitivity,

    "proximity_preferences":
        proximity_preferences,

    "family_composition":
        family_composition,
}

# =========================================================
# ENGINE EXECUTION
# =========================================================

(
    ranked_projects,
    eliminated_projects,
    normalized_weights,
    weight_log,
) = rank_projects(
    st.session_state.surviving_countries,
    project_answers,
)

# =========================================================
# WEIGHTS PANEL
# =========================================================

with col_weights:

    st.subheader("Determinant Weights")

    rows = []

    for determinant, baseline in (
        PROJECT_BASELINE_WEIGHTS.items()
    ):

        final = normalized_weights.get(
            determinant,
            0,
        )

        delta = round(final - baseline, 1)

        delta_str = (
            f"+{delta}"
            if delta > 0
            else str(delta)
        )

        rows.append({

            "Determinant":
                determinant.replace("_", " ").title(),

            "Baseline":
                f"{baseline}%",

            "Final":
                f"{final}%",

            "Δ":
                delta_str,
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    with st.expander(
        "📋 Why these weights changed"
    ):

        if not weight_log:

            st.caption(
                "No shifts applied — "
                "using baseline weights."
            )

        else:

            for entry in weight_log:

                tier = entry["tier"]

                det = (
                    entry["determinant"]
                    .replace("_", " ")
                    .title()
                )

                raw = entry["raw_shift"]

                adj = entry["adjusted_shift"]

                before = entry["before"]

                after = entry["after"]

                sign = "+" if raw > 0 else ""

                color = (
                    "🟢"
                    if raw > 0
                    else "🔴"
                )

                st.markdown(
                    f"{color} "
                    f"**{det}** ({tier}) — "
                    f"Raw: {sign}{raw} → "
                    f"Adjusted: "
                    f"{sign}{round(adj,2)} → "
                    f"{round(before,1)}% → "
                    f"**{round(after,1)}%**"
                )

# =========================================================
# RESULTS PANEL
# =========================================================

with col_results:

    st.subheader("Ranked Projects")

    st.caption(
        f"{len(ranked_projects)} "
        f"projects survived filtering"
    )

    for idx, item in enumerate(
        ranked_projects,
        1,
    ):

        with st.container(border=True):

            top = st.columns([1, 4, 2])

            with top[0]:

                st.markdown(f"### #{idx}")

            with top[1]:

                st.markdown(
                    f"**{item['project']}**"
                )

                st.caption(
                    f"{item['city']} · "
                    f"{item['country']}"
                )

            with top[2]:

                score = item["score"]

                if score > 70:
                    color = "#22c55e"

                elif score > 50:
                    color = "#f59e0b"

                else:
                    color = "#a0a0a0"

                st.markdown(
                    f"<h3 style='color:{color};"
                    f"text-align:right;"
                    f"margin:0'>{score}</h3>",
                    unsafe_allow_html=True,
                )

            with st.expander(
                "Score breakdown"
            ):

                for (
                    determinant,
                    contribution,
                ) in item["breakdown"].items():

                    weight = (
                        normalized_weights[
                            determinant
                        ]
                    )

                    raw_score = (
                        PROJECTS[
                            item["project"]
                        ]["scores"][
                            determinant
                        ]
                    )

                    st.caption(
                        f"**"
                        f"{determinant.replace('_',' ').title()}"
                        f"**: "
                        f"{contribution} pts "
                        f"(raw score "
                        f"{raw_score}/10 × "
                        f"{weight}% weight)"
                    )

    if eliminated_projects:

        with st.expander(
            f"❌ Eliminated Projects "
            f"({len(eliminated_projects)})"
        ):

            for item in eliminated_projects:

                st.caption(
                    f"**{item['project']}** — "
                    f"{item['reason']}"
                )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.success(
    "✅ Project Engine Mapping Complete"
)