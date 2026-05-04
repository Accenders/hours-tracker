import streamlit as st
from datetime import datetime
from src.sheets import get_all_hours, get_params
from src.calculations import calc_salary

HEBREW_MONTHS = {
    1: "ינואר", 2: "פברואר", 3: "מרץ", 4: "אפריל",
    5: "מאי", 6: "יוני", 7: "יולי", 8: "אוגוסט",
    9: "ספטמבר", 10: "אוקטובר", 11: "נובמבר", 12: "דצמבר",
}


def fmt(amount: float) -> str:
    rounded = round(amount, 2)
    if rounded == int(rounded):
        return f"₪{int(rounded):,}"
    return f"₪{rounded:,.2f}"


now = datetime.now()
current_month_prefix = now.strftime("%Y-%m")
month_label = f"{HEBREW_MONTHS[now.month]} {now.year}"

st.title(f"💰 תמונה נוכחית — {month_label}")

with st.spinner("טוען נתונים..."):
    all_entries = get_all_hours()
    params = get_params()

month_entries = [e for e in all_entries if e["date"].startswith(current_month_prefix)]

if not month_entries:
    st.info(f"אין דיווחי שעות עדיין ל{month_label}. הוסף דיווח בעמוד 'דיווח שעות'.")
    st.stop()

total_hours = sum(e["hours"] for e in month_entries)
work_days = len({e["date"] for e in month_entries})

def is_work_entry(entry: dict) -> bool:
    return entry.get("entry_type", "עבודה") == "עבודה"

def is_reimbursable(entry: dict) -> bool:
    if not is_work_entry(entry):
        return False
    loc = entry.get("location", "משרד")
    if loc == "משרד":
        return True
    if loc == "היברידי":
        return entry.get("office_hours", 0) >= 4
    return False

reimbursable_days = len({e["date"] for e in month_entries if is_reimbursable(e)})
absence_counts = {"חופש": 0, "מחלה": 0, "חג": 0}
for e in month_entries:
    t = e.get("entry_type", "עבודה")
    if t in absence_counts:
        absence_counts[t] += 1

result = calc_salary(
    hours=total_hours,
    work_days=reimbursable_days,
    hourly_rate=params["תעריף שעתי"],
    credit_points=params["נקודות זיכוי"],
    pension_employee_pct=params["פנסיה עובד %"] / 100,
    pension_employer_pct=params["פנסיה מעביד %"] / 100,
    training_fund_employee_pct=params["קרן השתלמות עובד %"] / 100,
    training_fund_employer_pct=params["קרן השתלמות מעביד %"] / 100,
    health_insurance=params["ביטוח בריאות ₪"],
    travel_per_day=params["נסיעות ליום ₪"],
    meals_per_day=params["ארוחות ליום ₪"],
)

# ── סיכום עליון ──────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("שעות מדווחות", f"{total_hours:g}")
col2.metric("ברוטו", fmt(result["gross"]))
col3.metric("נטו צפוי לקבלה", fmt(result["net"]))

additions_note = f" + תוספות {fmt(result['total_additions'])}" if result["total_additions"] > 0 else ""
work_entries = [e for e in month_entries if is_work_entry(e)]
actual_work_days = len({e["date"] for e in work_entries})
home_days = actual_work_days - reimbursable_days
home_note = f" · {home_days} מהבית (ללא החזרים)" if home_days > 0 else ""

absence_parts = [f"{v} {k}" for k, v in absence_counts.items() if v > 0]
absence_note = " · היעדרויות: " + ", ".join(absence_parts) if absence_parts else ""

st.caption(
    f"מבוסס על {actual_work_days} ימי עבודה ו-{total_hours:g} שעות ב{month_label}  \n"
    f"{reimbursable_days} ימים עם זכאות להחזרים{home_note}{absence_note}  \n"
    f"נטו = ברוטו {fmt(result['gross'])} פחות ניכויים {fmt(result['total_deductions'])}{additions_note}"
)

st.divider()

# ── ניכויים ──────────────────────────────────────────────────────────
st.subheader("📉 ניכויים מהמשכורת")

deductions_data = {
    "מס הכנסה": result["income_tax"],
    "ביטוח לאומי": result["bituach_leumi"],
    f"פנסיה עובד ({params['פנסיה עובד %']:g}%)": result["pension_employee"],
    f"קרן השתלמות עובד ({params['קרן השתלמות עובד %']:g}%)": result["training_fund_employee"],
}
if result["health_insurance"] > 0:
    deductions_data["ביטוח בריאות"] = result["health_insurance"]

for label, amount in deductions_data.items():
    col_l, col_r = st.columns([3, 1])
    col_l.write(label)
    col_r.write(f"**{fmt(amount)}**")

st.write(f"**סה\"כ ניכויים: {fmt(result['total_deductions'])}**")

# ── תוספות ───────────────────────────────────────────────────────────
if result["total_additions"] > 0:
    st.divider()
    st.subheader("📈 תוספות")
    if result["travel"] > 0:
        col_l, col_r = st.columns([3, 1])
        col_l.write(f"נסיעות ({reimbursable_days} ימים × {fmt(params['נסיעות ליום ₪'])})")
        col_r.write(f"**{fmt(result['travel'])}**")
    if result["meals"] > 0:
        col_l, col_r = st.columns([3, 1])
        col_l.write(f"ארוחות ({reimbursable_days} ימים × {fmt(params['ארוחות ליום ₪'])})")
        col_r.write(f"**{fmt(result['meals'])}**")
    st.write(f"**סה\"כ תוספות: {fmt(result['total_additions'])}**")

# ── עלות מעביד ────────────────────────────────────────────────────────
st.divider()
st.subheader("🏢 עלות מעביד כוללת")

col_l, col_r = st.columns([3, 1])
col_l.write("ברוטו")
col_r.write(fmt(result["gross"]))

col_l, col_r = st.columns([3, 1])
col_l.write(f"פנסיה מעביד ({params['פנסיה מעביד %']:g}%)")
col_r.write(fmt(result["pension_employer"]))

col_l, col_r = st.columns([3, 1])
col_l.write(f"קרן השתלמות מעביד ({params['קרן השתלמות מעביד %']:g}%)")
col_r.write(fmt(result["training_fund_employer"]))

st.write(f"**סה\"כ עלות מעביד: {fmt(result['employer_cost'])}**")
