import streamlit as st
from src.ui import set_rtl

st.set_page_config(page_title="דיווח שעות", page_icon="⏱️", layout="centered")
set_rtl()

pg = st.navigation({
    "תפריט ראשי": [
        st.Page("pages/0_בית.py",            title="🏠 בית",           default=True),
        st.Page("pages/1_דיווח_שעות.py",     title="📝 דיווח שעות"),
        st.Page("pages/2_תמונה_נוכחית.py",   title="💰 תמונה נוכחית"),
        st.Page("pages/3_סימולטור.py",        title="🔢 סימולטור"),
        st.Page("pages/4_הגדרות.py",          title="⚙️ הגדרות"),
    ]
})
pg.run()
