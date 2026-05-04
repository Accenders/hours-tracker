import streamlit as st

st.markdown("<h1 style='text-align:center'>⏱️ מערכת דיווח שעות</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>בחר עמוד מהתפריט מימין</p>", unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_דיווח_שעות.py", label="📝 דיווח שעות", use_container_width=True)
with col2:
    st.page_link("pages/2_תמונה_נוכחית.py", label="💰 תמונה נוכחית", use_container_width=True)
with col3:
    st.page_link("pages/3_סימולטור.py", label="🔢 סימולטור", use_container_width=True)
