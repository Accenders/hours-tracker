import streamlit as st

RTL_CSS = """
<style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    .stApp {
        direction: rtl;
    }
    section[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"] {
        direction: rtl;
        text-align: right;
    }
    .stMarkdown, .stMarkdown p,
    [data-testid="stText"],
    [data-testid="stCaption"],
    [data-testid="stHeading"] {
        direction: rtl;
        text-align: right;
    }
    .stTextInput > label,
    .stNumberInput > label,
    .stDateInput > label,
    .stSelectbox > label,
    .stTextArea > label,
    .stCheckbox > label,
    .stRadio > label {
        direction: rtl;
        text-align: right;
    }
    .stAlert, .stSuccess, .stInfo, .stWarning, .stError {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricLabel"] {
        direction: rtl;
        text-align: right;
    }
    .stDataFrame, table {
        direction: rtl;
    }
    button[kind="primary"], button[kind="secondary"] {
        direction: rtl;
    }
    .stForm {
        direction: rtl;
    }
    [data-testid="stPageLink"] {
        direction: rtl;
        text-align: right;
    }
    [data-testid="stSidebarNavSectionHeader"] span {
        display: none;
    }
    [data-testid="stSidebarNavSectionHeader"]::before {
        content: "תפריט ראשי";
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
    }
</style>
"""

def set_rtl():
    st.markdown(RTL_CSS, unsafe_allow_html=True)
