import streamlit as st
from src.sheets import get_params, save_params
from src.config import TAX_BRACKETS, BITUACH_LEUMI_LOW_CEILING, BITUACH_LEUMI_HIGH_CEILING

st.title("⚙️ הגדרות")

tab_personal, tab_tax = st.tabs(["👤 פרמטרים אישיים", "📊 מדרגות מס (קבועים)"])

# ── פרמטרים אישיים ───────────────────────────────────────────────
with tab_personal:
    with st.spinner("טוען פרמטרים..."):
        params = get_params()

    with st.form("params_form"):
        st.subheader("שכר ותעריף")
        col1, col2 = st.columns(2)
        with col1:
            hourly_rate = st.number_input(
                "תעריף שעתי (₪)",
                min_value=0.0, step=1.0,
                value=float(params.get("תעריף שעתי", 60)),
                key="s_hourly_rate"
            )
        with col2:
            credit_points = st.number_input(
                "נקודות זיכוי מס",
                min_value=0.0, step=0.25,
                value=float(params.get("נקודות זיכוי", 2.25)),
                help="תושב ישראל = 2.25 נקודות בברירת מחדל",
                key="s_credit_points"
            )

        st.subheader("פנסיה")
        col1, col2 = st.columns(2)
        with col1:
            pension_emp = st.number_input(
                "הפרשת עובד לפנסיה (%)",
                min_value=0.0, max_value=100.0, step=0.5,
                value=float(params.get("פנסיה עובד %", 6)),
                key="s_pension_emp"
            )
        with col2:
            pension_er = st.number_input(
                "הפרשת מעביד לפנסיה (%)",
                min_value=0.0, max_value=100.0, step=0.5,
                value=float(params.get("פנסיה מעביד %", 6.5)),
                key="s_pension_er"
            )

        st.subheader("קרן השתלמות")
        col1, col2 = st.columns(2)
        with col1:
            training_emp = st.number_input(
                "הפרשת עובד לקרן השתלמות (%)",
                min_value=0.0, max_value=100.0, step=0.5,
                value=float(params.get("קרן השתלמות עובד %", 2.5)),
                key="s_training_emp"
            )
        with col2:
            training_er = st.number_input(
                "הפרשת מעביד לקרן השתלמות (%)",
                min_value=0.0, max_value=100.0, step=0.5,
                value=float(params.get("קרן השתלמות מעביד %", 7.5)),
                key="s_training_er"
            )

        st.subheader("ניכויים ותוספות")
        col1, col2, col3 = st.columns(3)
        with col1:
            health = st.number_input(
                "ביטוח בריאות (₪/חודש)",
                min_value=0.0, step=10.0,
                value=float(params.get("ביטוח בריאות ₪", 0)),
                key="s_health"
            )
        with col2:
            travel = st.number_input(
                "החזר נסיעות (₪/יום)",
                min_value=0.0, step=0.1,
                value=float(params.get("נסיעות ליום ₪", 0)),
                key="s_travel"
            )
        with col3:
            meals = st.number_input(
                "החזר ארוחות (₪/יום)",
                min_value=0.0, step=0.1,
                value=float(params.get("ארוחות ליום ₪", 0)),
                key="s_meals"
            )

        saved = st.form_submit_button("💾 שמור פרמטרים", use_container_width=True, type="primary")

    if saved:
        new_params = {
            "תעריף שעתי":           hourly_rate,
            "נקודות זיכוי":          credit_points,
            "פנסיה עובד %":          pension_emp,
            "פנסיה מעביד %":         pension_er,
            "קרן השתלמות עובד %":    training_emp,
            "קרן השתלמות מעביד %":   training_er,
            "ביטוח בריאות ₪":       health,
            "נסיעות ליום ₪":        travel,
            "ארוחות ליום ₪":        meals,
        }
        with st.spinner("שומר..."):
            save_params(new_params)
        st.success("הפרמטרים נשמרו בהצלחה")

# ── מדרגות מס (קבועים) ───────────────────────────────────────────
with tab_tax:
    st.subheader("מדרגות מס הכנסה 2025")
    st.caption("מוגדרות בחוק — מתעדכנות אחת לשנה")

    rows = []
    prev = 0
    for ceiling, rate in TAX_BRACKETS:
        if ceiling == float("inf"):
            bracket = f"מעל ₪{prev:,.0f}"
        else:
            bracket = f"₪{prev + 1:,.0f} – ₪{ceiling:,.0f}"
        rows.append({"מדרגה": bracket, "שיעור מס": f"{int(rate * 100)}%"})
        prev = ceiling

    st.table(rows)

    st.subheader("ביטוח לאומי 2025")
    st.caption("חלק עובד בלבד")
    st.table([
        {"הכנסה חודשית": f"עד ₪{BITUACH_LEUMI_LOW_CEILING:,.0f}",                                        "שיעור": "0.4%"},
        {"הכנסה חודשית": f"₪{BITUACH_LEUMI_LOW_CEILING + 1:,.0f} – ₪{BITUACH_LEUMI_HIGH_CEILING:,.0f}", "שיעור": "7%"},
        {"הכנסה חודשית": f"מעל ₪{BITUACH_LEUMI_HIGH_CEILING:,.0f}",                                      "שיעור": "פטור"},
    ])
