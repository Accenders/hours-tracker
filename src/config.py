import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "hours-tracker")

# שמות הגיליונות בתוך הספרדשיט
SHEET_HOURS = "שעות"
SHEET_PARAMS = "פרמטרים"
SHEET_SUMMARY = "סיכום חודשי"

# מדרגות מס הכנסה 2025 — (תקרה חודשית, שיעור)
TAX_BRACKETS = [
    (7_010,  0.10),
    (10_060, 0.14),
    (16_150, 0.20),
    (21_240, 0.31),
    (44_020, 0.35),
    (56_730, 0.47),
    (float("inf"), 0.50),
]

# ערך נקודת זיכוי חודשית (2025)
TAX_CREDIT_POINT_VALUE = 242

# ביטוח לאומי 2025
BITUACH_LEUMI_LOW_RATE = 0.004   # עד תקרה ראשונה
BITUACH_LEUMI_HIGH_RATE = 0.07   # מעל תקרה ראשונה
BITUACH_LEUMI_LOW_CEILING = 7_522
BITUACH_LEUMI_HIGH_CEILING = 49_030
