import streamlit as st

st.set_page_config(
    page_title="Pangaea Advisory",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp { background-color: #0A0A0A; }
.metric-card {
    background: #111111;
    border: 1px solid #222222;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏛️ Pangaea Advisory")
st.caption("Multi-layer recommendation engine — Country, City, Project")

st.markdown("""
### How it works

**Page 1 — Country Filtering**
Answer 6 questions about budget, visa, citizenship, risk, and geography.
Watch determinant weights shift and countries get ranked live.

**Page 2 — City Filtering**
Within the surviving countries from Page 1, answer 5 more questions
about lifestyle, family, and preferences. See cities ranked with
full explainability.

---

Use the sidebar to navigate.

The selections you make on Page 1 are automatically passed to Page 2 —
no need to re-enter anything.
""")
