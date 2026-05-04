import gspread
from google.oauth2.service_account import Credentials
from src.config import CREDENTIALS_PATH, SHEET_NAME, SHEET_HOURS, SHEET_PARAMS, SHEET_SUMMARY

DEFAULT_PARAMS = {
    "תעריף שעתי": 60,
    "נקודות זיכוי": 2.25,
    "פנסיה עובד %": 6,
    "פנסיה מעביד %": 6.5,
    "קרן השתלמות עובד %": 2.5,
    "קרן השתלמות מעביד %": 7.5,
    "ביטוח בריאות ₪": 0,
    "נסיעות ליום ₪": 0,
    "ארוחות ליום ₪": 0,
}

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def get_client():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    return gspread.authorize(creds)

def get_spreadsheet():
    return get_client().open(SHEET_NAME)

def ensure_sheets_exist():
    """יוצר את הגיליונות הדרושים אם עדיין לא קיימים."""
    ss = get_spreadsheet()
    existing = [ws.title for ws in ss.worksheets()]

    required = {
        SHEET_HOURS:   ["תאריך", "שעות", "הערות", "מיקום", "שעות_משרד", "סוג"],
        SHEET_PARAMS:  ["פרמטר", "ערך"],
        SHEET_SUMMARY: ["חודש", "שעות", "ברוטו", "מס_הכנסה", "ביטוח_לאומי",
                        "פנסיה_עובד", "קרן_השתלמות_עובד", "ביטוח_בריאות",
                        "נסיעות", "ארוחות", "נטו"],
    }

    for name, headers in required.items():
        if name not in existing:
            ws = ss.add_worksheet(title=name, rows=1000, cols=len(headers))
            ws.append_row(headers)

    # מחיקת גיליון ברירת המחדל "Sheet1" אם קיים ויש לנו לפחות גיליון אחד
    if "Sheet1" in existing and len(existing) > 1:
        ss.del_worksheet(ss.worksheet("Sheet1"))


def get_params() -> dict:
    ws = get_spreadsheet().worksheet(SHEET_PARAMS)
    rows = ws.get_all_values()
    params = dict(DEFAULT_PARAMS)
    for row in rows[1:]:
        if len(row) >= 2 and row[0]:
            try:
                params[row[0]] = float(row[1])
            except ValueError:
                pass
    return params


def save_params(params: dict):
    ws = get_spreadsheet().worksheet(SHEET_PARAMS)
    ws.clear()
    ws.append_row(["פרמטר", "ערך"])
    for key, value in params.items():
        ws.append_row([key, value])


def get_all_hours() -> list:
    ws = get_spreadsheet().worksheet(SHEET_HOURS)
    rows = ws.get_all_values()
    result = []
    for i, row in enumerate(rows[1:], start=2):
        if len(row) >= 2 and row[0] and row[1]:
            try:
                office_hours_raw = row[4] if len(row) > 4 and row[4] else "0"
                result.append({
                    "row_index": i,
                    "date": row[0],
                    "hours": float(row[1]),
                    "notes": row[2] if len(row) > 2 else "",
                    "location": row[3] if len(row) > 3 and row[3] else "משרד",
                    "office_hours": float(office_hours_raw),
                    "entry_type": row[5] if len(row) > 5 and row[5] else "עבודה",
                })
            except ValueError:
                pass
    return result


def add_hour_entry(date_str: str, hours: float, notes: str = "",
                   location: str = "משרד", office_hours: float = 0.0,
                   entry_type: str = "עבודה"):
    ws = get_spreadsheet().worksheet(SHEET_HOURS)
    ws.append_row([date_str, hours, notes, location, office_hours, entry_type])


def delete_hour_entry(row_index: int):
    ws = get_spreadsheet().worksheet(SHEET_HOURS)
    ws.delete_rows(row_index)
