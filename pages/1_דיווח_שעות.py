import streamlit as st
from datetime import date, datetime, timedelta
from src.sheets import get_all_hours, add_hour_entry, delete_hour_entry, update_hour_entry

st.title("📝 דיווח שעות")

# ── כפתור כניסה / יציאה מהירה ────────────────────────────────────
if "clock_in_time" not in st.session_state:
    st.session_state.clock_in_time = None

LOCATIONS = ["משרד 🏢", "בית 🏠", "היברידי 🔀"]

if "clock_in_time" not in st.session_state:
    st.session_state.clock_in_time = None
if "editing_row" not in st.session_state:
    st.session_state.editing_row = None
if "quick_location" not in st.session_state:
    st.session_state.quick_location = LOCATIONS[0]
if "quick_office_hours" not in st.session_state:
    st.session_state.quick_office_hours = 4.0

if st.session_state.clock_in_time is None:
    quick_loc = st.radio("מיקום עבודה", LOCATIONS, horizontal=True, key="quick_loc_radio")
    st.session_state.quick_location = quick_loc
    if st.button("⏰ כניסה מהירה", use_container_width=True, type="primary"):
        st.session_state.clock_in_time = datetime.now()
        st.rerun()
else:
    clock_in = st.session_state.clock_in_time
    elapsed = datetime.now() - clock_in
    hours_elapsed = elapsed.total_seconds() / 3600
    st.info(f"במשמרת מאז {clock_in.strftime('%H:%M')} — {hours_elapsed:.1f} שעות עד כה")
    loc_label = st.session_state.quick_location
    if "היברידי" in loc_label:
        quick_office_h = st.number_input(
            "שעות במשרד (מתוך המשמרת)", min_value=0.5, max_value=24.0, step=0.5,
            value=st.session_state.quick_office_hours, key="quick_oh"
        )
        st.session_state.quick_office_hours = quick_office_h
    if st.button("⏹️ יציאה", use_container_width=True, type="secondary"):
        rounded = max(0.5, round(hours_elapsed * 2) / 2)
        loc_clean = loc_label.split()[0]
        office_h = st.session_state.quick_office_hours if "היברידי" in loc_label else 0.0
        with st.spinner("שומר..."):
            add_hour_entry(clock_in.strftime("%Y-%m-%d"), rounded, "כניסה מהירה",
                           location=loc_clean, office_hours=office_h)
        st.session_state.clock_in_time = None
        st.success(f"נשמר — {rounded:g} שעות ({loc_clean})")
        st.rerun()

st.divider()

# ── הוספת דיווח חדש ──────────────────────────────────────────────
st.subheader("הוספת יום עבודה")
tab_hours, tab_clock, tab_absence = st.tabs(["⏱️ לפי מספר שעות", "🕐 לפי שעות כניסה ויציאה", "🏖️ היעדרות"])

with tab_hours:
    entry_loc = st.radio("מיקום", LOCATIONS, horizontal=True, key="form_hours_loc")
    with st.form("add_by_hours", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("תאריך", value=date.today(), format="DD/MM/YYYY")
        with col2:
            entry_hours = st.number_input("שעות", min_value=0.5, max_value=24.0, step=0.5, value=8.0)
        entry_office_h = 0.0
        if "היברידי" in entry_loc:
            entry_office_h = st.number_input(
                "שעות במשרד", min_value=0.5, max_value=24.0, step=0.5, value=4.0, key="form_hours_oh"
            )
        entry_notes = st.text_input("הערות (אופציונלי)")
        submitted = st.form_submit_button("הוסף ✅", use_container_width=True)
    if submitted:
        loc_clean = entry_loc.split()[0]
        with st.spinner("שומר..."):
            add_hour_entry(entry_date.strftime("%Y-%m-%d"), entry_hours, entry_notes,
                           location=loc_clean, office_hours=entry_office_h)
        st.success(f"נשמר — {entry_date.strftime('%d/%m/%Y')} | {entry_hours:g} שעות ({loc_clean})")
        st.rerun()

with tab_clock:
    clock_loc = st.radio("מיקום", LOCATIONS, horizontal=True, key="form_clock_loc")
    with st.form("add_by_clock", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            clock_date = st.date_input("תאריך", value=date.today(), format="DD/MM/YYYY", key="clock_date")
        with col2:
            start_str = st.text_input("שעת כניסה", placeholder="נא להזין", key="clock_start")
        with col3:
            end_str = st.text_input("שעת יציאה", placeholder="נא להזין", key="clock_end")
        clock_office_h = 0.0
        if "היברידי" in clock_loc:
            clock_office_h = st.number_input(
                "שעות במשרד", min_value=0.5, max_value=24.0, step=0.5, value=4.0, key="form_clock_oh"
            )
        clock_notes = st.text_input("הערות (אופציונלי)", key="clock_notes")
        submitted2 = st.form_submit_button("הוסף ✅", use_container_width=True)
    if submitted2:
        def parse_time(s):
            for fmt in ("%H:%M", "%H%M"):
                try:
                    return datetime.strptime(s.strip(), fmt).time()
                except ValueError:
                    pass
            return None

        t_start = parse_time(start_str)
        t_end = parse_time(end_str)
        if t_start is None or t_end is None:
            st.error("פורמט שעה לא תקין — הזן בפורמט HH:MM למשל 08:37")
        else:
            dt_start = datetime.combine(clock_date, t_start)
            dt_end = datetime.combine(clock_date, t_end)
            if dt_end <= dt_start:
                dt_end += timedelta(days=1)
            hours_diff = (dt_end - dt_start).total_seconds() / 3600
            rounded = max(0.5, round(hours_diff * 2) / 2)
            loc_clean = clock_loc.split()[0]
            with st.spinner("שומר..."):
                add_hour_entry(
                    clock_date.strftime("%Y-%m-%d"), rounded,
                    clock_notes or f"{t_start.strftime('%H:%M')}–{t_end.strftime('%H:%M')}",
                    location=loc_clean, office_hours=clock_office_h,
                )
            st.success(f"נשמר — {clock_date.strftime('%d/%m/%Y')} | {rounded:g} שעות ({loc_clean})")
            st.rerun()

with tab_absence:
    ABSENCE_TYPES = {"חופש 🏖️": "חופש", "מחלה 🤒": "מחלה", "חג ✡️": "חג"}
    with st.form("add_absence", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            abs_date = st.date_input("תאריך", value=date.today(), format="DD/MM/YYYY", key="abs_date")
        with col2:
            abs_hours = st.number_input("שעות", min_value=0.5, max_value=24.0, step=0.5, value=8.0, key="abs_hours")
        abs_type_label = st.radio("סוג היעדרות", list(ABSENCE_TYPES.keys()), horizontal=True, key="abs_type")
        abs_notes = st.text_input("הערות (אופציונלי)", key="abs_notes")
        submitted_abs = st.form_submit_button("הוסף ✅", use_container_width=True)
    if submitted_abs:
        abs_type = ABSENCE_TYPES[abs_type_label]
        with st.spinner("שומר..."):
            add_hour_entry(abs_date.strftime("%Y-%m-%d"), abs_hours, abs_notes,
                           location="—", office_hours=0.0, entry_type=abs_type)
        st.success(f"נשמר — {abs_date.strftime('%d/%m/%Y')} | {abs_type} | {abs_hours:g} שעות")
        st.rerun()

st.divider()

# ── רשימת הדיווחים ───────────────────────────────────────────────
st.subheader("דיווחים קיימים")

with st.spinner("טוען נתונים..."):
    entries = get_all_hours()

if not entries:
    st.info("אין דיווחים עדיין — הוסף יום עבודה למעלה.")
else:
    total_hours = sum(e["hours"] for e in entries)
    st.metric("סה\"כ שעות מדווחות", f"{total_hours:g}")

    LOC_ICON = {"משרד": "🏢", "בית": "🏠", "היברידי": "🔀"}
    TYPE_ICON = {"עבודה": "", "חופש": "🏖️", "מחלה": "🤒", "חג": "✡️"}

    ABSENCE_LABELS = {"חופש": "חופש 🏖️", "מחלה": "מחלה 🤒", "חג": "חג ✡️"}
    ABSENCE_TYPES_REV = {v: k for k, v in ABSENCE_LABELS.items()}
    LOC_MAP = {"משרד": "משרד 🏢", "בית": "בית 🏠", "היברידי": "היברידי 🔀"}

    for entry in sorted(entries, key=lambda x: x["date"], reverse=True):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 1, 1])
        with col1:
            try:
                y, m, d = entry["date"].split("-")
                display_date = f"{d}/{m}/{y}"
            except Exception:
                display_date = entry["date"]
            st.write(f"📅 {display_date}")
        with col2:
            st.write(f"⏱️ {entry['hours']:g} שע'")
        with col3:
            etype = entry.get("entry_type", "עבודה")
            if etype != "עבודה":
                st.write(f"{TYPE_ICON.get(etype, '')} {etype}")
            else:
                loc = entry.get("location", "משרד")
                label = f"{LOC_ICON.get(loc, '')} {loc}"
                if loc == "היברידי" and entry.get("office_hours", 0) > 0:
                    label += f" ({entry['office_hours']:g}ש')"
                st.write(label)
        with col4:
            st.write(entry["notes"] if entry["notes"] else "—")
        with col5:
            if st.button("✏️", key=f"edit_{entry['row_index']}"):
                st.session_state.editing_row = (
                    None if st.session_state.editing_row == entry["row_index"]
                    else entry["row_index"]
                )
                st.rerun()
        with col6:
            if st.button("🗑️", key=f"del_{entry['row_index']}"):
                with st.spinner("מוחק..."):
                    delete_hour_entry(entry["row_index"])
                if st.session_state.editing_row == entry["row_index"]:
                    st.session_state.editing_row = None
                st.rerun()

        if st.session_state.editing_row == entry["row_index"]:
            with st.container(border=True):
                st.caption("✏️ עריכת דיווח")
                etype = entry.get("entry_type", "עבודה")
                ecol1, ecol2 = st.columns(2)
                with ecol1:
                    try:
                        current_date = date.fromisoformat(entry["date"])
                    except Exception:
                        current_date = date.today()
                    edit_date = st.date_input("תאריך", value=current_date,
                                              format="DD/MM/YYYY", key=f"ed_date_{entry['row_index']}")
                with ecol2:
                    edit_hours = st.number_input("שעות", min_value=0.5, max_value=24.0, step=0.5,
                                                 value=float(entry["hours"]), key=f"ed_hours_{entry['row_index']}")
                if etype == "עבודה":
                    current_loc_label = LOC_MAP.get(entry.get("location", "משרד"), "משרד 🏢")
                    loc_index = LOCATIONS.index(current_loc_label) if current_loc_label in LOCATIONS else 0
                    edit_loc = st.radio("מיקום", LOCATIONS, index=loc_index,
                                        horizontal=True, key=f"ed_loc_{entry['row_index']}")
                    edit_office_h = 0.0
                    if "היברידי" in edit_loc:
                        edit_office_h = st.number_input(
                            "שעות במשרד", min_value=0.5, max_value=24.0, step=0.5,
                            value=max(0.5, float(entry.get("office_hours", 4.0))),
                            key=f"ed_oh_{entry['row_index']}")
                    edit_entry_type = "עבודה"
                    edit_loc_clean = edit_loc.split()[0]
                else:
                    abs_labels = list(ABSENCE_LABELS.values())
                    current_abs_label = ABSENCE_LABELS.get(etype, "חופש 🏖️")
                    abs_index = abs_labels.index(current_abs_label) if current_abs_label in abs_labels else 0
                    edit_abs = st.radio("סוג היעדרות", abs_labels, index=abs_index,
                                        horizontal=True, key=f"ed_abs_{entry['row_index']}")
                    edit_entry_type = ABSENCE_TYPES_REV[edit_abs]
                    edit_office_h = 0.0
                    edit_loc_clean = "—"
                edit_notes = st.text_input("הערות", value=entry.get("notes", ""),
                                           key=f"ed_notes_{entry['row_index']}")
                save_col, cancel_col = st.columns(2)
                with save_col:
                    if st.button("💾 שמור", key=f"save_{entry['row_index']}",
                                 use_container_width=True, type="primary"):
                        with st.spinner("שומר..."):
                            update_hour_entry(entry["row_index"],
                                              edit_date.strftime("%Y-%m-%d"),
                                              edit_hours, edit_notes,
                                              edit_loc_clean, edit_office_h, edit_entry_type)
                        st.session_state.editing_row = None
                        st.rerun()
                with cancel_col:
                    if st.button("❌ בטל", key=f"cancel_{entry['row_index']}",
                                 use_container_width=True):
                        st.session_state.editing_row = None
                        st.rerun()
