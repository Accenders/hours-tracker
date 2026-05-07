# Project: Hours & Salary Reporting Platform

> Spec and progress tracking file. Updated each session to resume from the same point.
> Last updated: May 2026 — Session 7

---

## Project Description

A personal-use platform for logging daily work hours, calculating net/gross salary using full Israeli tax brackets, a dashboard with insights, monthly history, and a Claude bot for personal financial advice.

---

## Users & Access

- Single user (Yuval)
- Access from iPhone and computer (browser, can be saved as PWA)
- Storage: Google Sheets (synced to Google Drive)

## Git Workflow Rules

- **After every code change**, Claude automatically runs:
  ```
  git add <changed files>
  git commit -m "<short description of change>"
  ```
- Do NOT run `git push` unless explicitly requested.
- Commit message in Hebrew or English — short and focused.
- No need to ask for approval before each commit — this is the default in this project.

---

## Security Rules

- API keys, credentials files, and passwords — **never in chat and never in code**. Always in `.env` only.
- Claude will alert immediately if sensitive information is detected in the conversation and explain how to revoke it.

---

## Parameters (configured via settings page, saved in Google Sheets)

| Parameter | Default | Notes |
|---|---|---|
| Hourly rate | 60 | ₪ per hour |
| Tax credit points | 2.25 | Resident + employee. Each point = ₪242/month (2025) |
| Pension employee % | 6 | % of gross |
| Pension employer % | 6.5 | % of gross |
| Training fund employee % | 2.5 | % of gross |
| Training fund employer % | 7.5 | % of gross |
| Health insurance ₪ | 0 | Fixed ₪ per month (deduction) |
| Travel per day ₪ | 0 | ₪ per work day (addition) |
| Meals per day ₪ | 0 | ₪ per work day (addition) |

---

## Functionality

### 1. Hours Reporting ✅ Done
- Quick clock-in / clock-out button (measures actual time)
- Manual entry by number of hours
- Entry by start time and end time (auto-calculates)
- Date format DD/MM/YYYY
- List of all entries + inline edit (✏️) + delete
- Cumulative total hours

### 2. Current Snapshot (current month) ✅ Done
- Total hours reported so far
- Cumulative gross
- Deductions breakdown: income tax, national insurance, pension, training fund, health insurance
- Additions: travel + meals
- **Expected net to receive**
- **Total employer cost**

### 3. Simulator — Not yet built
- Enter additional (hypothetical) hours
- Display updated gross/net accordingly

### 4. Insights Dashboard (charts) — Not yet built
- Work hours by week/month
- Net and gross over months
- Deductions breakdown (Pie chart)
- Trends over time

### 5. History — Not yet built
- View previous months
- Month-to-month comparison
- Data stored in Google Sheets (one row per month)

### 6. Settings ✅ Done
- Personal parameters tab: edit and save to Google Sheets
- Tax brackets tab: view income tax and national insurance tables

### 7. Claude Bot (personal advice) — Not yet built
- Built-in chat interface in Streamlit
- Bot has access to data: hours, parameters, history
- Examples: "How many more hours do I need to reach ₪X net?", "What's the average of the last 3 months?"

---

## Income Tax Brackets — 2025

| Bracket | Monthly Income | Tax Rate |
|---|---|---|
| 1 | Up to ₪7,010 | 10% |
| 2 | ₪7,011 – ₪10,060 | 14% |
| 3 | ₪10,061 – ₪16,150 | 20% |
| 4 | ₪16,151 – ₪21,240 | 31% |
| 5 | ₪21,241 – ₪44,020 | 35% |
| 6 | ₪44,021 – ₪56,730 | 47% |
| 7 | Above ₪56,730 | 50% |

Tax credit point: ₪242/month (2025). Default: 2.25 points (resident + employee).

---

## National Insurance (Bituach Leumi) — 2025

| Monthly Income | Employee Rate |
|---|---|
| Up to ₪7,522 | 0.4% |
| Above ₪7,522 (up to ceiling) | 7% on the excess |
| Ceiling | ₪49,030/month |

---

## Technical Approach

| Layer | Technology | Reason |
|---|---|---|
| UI | Streamlit (Python) | Simple to build, works in browser from any device |
| Charts | Plotly (via Streamlit) | Interactive and appealing |
| Data storage | Google Sheets | Auto-sync, no infrastructure |
| Sheets access | `gspread` | Simple Python library |
| AI bot | Anthropic Claude API | Data-driven personal financial advice |
| Hosting | Streamlit Community Cloud | Free, accessible from anywhere |
| iPhone access | PWA (save to home screen) | Feels like an app without App Store |

---

## Current Folder Structure

```
hours-tracker/
├── .env                    ✅ API keys (Anthropic + Google)
├── .env.example            ✅
├── .gitignore              ✅ protects credentials.json and .env
├── requirements.txt        ✅
├── credentials.json        ✅ Service Account for Google access
├── spec.md                 ✅ this file
├── app.py                  ✅ main router — st.navigation() with "Main Menu"
├── pages/
│   ├── 0_בית.py            ✅ home page with quick navigation
│   ├── 1_דיווח_שעות.py     ✅ full — quick clock-in, by hours, by clock, absences, location, list + edit + delete
│   ├── 2_תמונה_נוכחית.py   ✅ full — metrics, deductions, additions, employer cost, reimbursable days by location
│   ├── 3_סימולטור.py        ⏳ placeholder only
│   └── 4_הגדרות.py          ✅ full — personal parameters + tax brackets
└── src/
    ├── __init__.py          ✅
    ├── config.py            ✅ tax brackets, national insurance, DEFAULT_PARAMS
    ├── sheets.py            ✅ Google connection + CRUD hours + parameters
    ├── calculations.py      ✅ calc_income_tax, calc_bituach_leumi, calc_salary
    └── ui.py                ✅ set_rtl() — global RTL CSS
```

---

## Progress Status

- [x] Initial spec — description, parameters, functionality
- [x] Technology selection — Streamlit + Google Sheets + Claude API
- [x] Define tax and national insurance brackets
- [x] Define folder structure
- [x] Create project folder — `/Users/yuvalmoradov/VSCode/hours-tracker/`
- [x] Set up Python environment — `.venv` + packages (`gspread`, `google-auth`, `python-dotenv`, `streamlit`, `plotly`)
- [x] `credentials.json` in place + `.gitignore` protecting it
- [x] Enable Google Sheets API + Google Drive API in Google Cloud Console
- [x] Write `src/config.py` — tax brackets + constants + DEFAULT_PARAMS
- [x] Write `src/sheets.py` — connection + create sheets + CRUD hours and parameters
- [x] Write `src/calculations.py` — tax, national insurance, net/gross calculations
- [x] Write `src/ui.py` — set_rtl() for global RTL styling
- [x] Build `app.py` — router with st.navigation() and "Main Menu" title
- [x] Build hours reporting page — quick clock-in + 2 tabs + delete + RTL
- [x] Build settings page — personal parameters + tax brackets view
- [x] Build current snapshot page — load parameters and hours, run calc_salary, display metrics/deductions/additions/employer cost
- [x] Add work location to each entry — office / home / hybrid (4+ hours = reimbursement eligibility)
- [x] Add absence days — vacation / sick / holiday (counted toward gross, not reimbursements, summary shown in current snapshot)
- [x] UI fixes — time fields free-text input, comprehensive RTL, accurate rounding, explicit keys in settings
- [x] Performance fix — `@st.cache_resource` on `get_client()` so Google auth runs once, not on every operation
- [x] Bug fix — location radio moved outside `st.form` so hybrid field shows/hides immediately on change
- [x] Edit entry — ✏️ button on each entry opens inline form with pre-filled fields; saves via `update_hour_entry()`
- [ ] **⏭️ CONTINUE FROM HERE: Simulator page**
  - Field: "How many additional hours?"
  - Calculate updated gross/net based on current_hours + hypothetical_hours
  - Comparison: before/after
- [ ] Build charts dashboard (Plotly)
- [ ] Build history page
- [ ] Connect Claude API — advice bot
- [x] Deploy to Streamlit Cloud — repo at github.com/Accenders/hours-tracker, hosted on Streamlit Community Cloud
- [x] iPhone access — save app URL to home screen as PWA
- [ ] Testing with real data

---

## Notes for Next Session

### Internal API — dict keys

`update_hour_entry(row_index, date_str, hours, notes, location, office_hours, entry_type)` — updates a row in-place in Google Sheets.

`get_all_hours()` returns a list of dicts with keys:
- `row_index`, `date` (YYYY-MM-DD), `hours`, `notes`
- `location` — "משרד" / "בית" / "היברידי" / "—" (absences)
- `office_hours` — float, relevant only for hybrid
- `entry_type` — "עבודה" / "חופש" / "מחלה" / "חג" (default: "עבודה")

`get_params()` returns a dict with Hebrew keys:
- "תעריף שעתי", "נקודות זיכוי", "פנסיה עובד %", "פנסיה מעביד %"
- "קרן השתלמות עובד %", "קרן השתלמות מעביד %"
- "ביטוח בריאות ₪", "נסיעות ליום ₪", "ארוחות ליום ₪"

`calc_salary()` receives: `hours`, `work_days` (reimbursable days only!), `hourly_rate` + all other parameters, and returns a full dict with: `gross`, `income_tax`, `bituach_leumi`, `pension_employee`, `training_fund_employee`, `health_insurance`, `travel`, `meals`, `total_deductions`, `total_additions`, `net`, `pension_employer`, `training_fund_employer`, `employer_cost`

### Important Business Rules
- **Travel/meal reimbursements**: work days only (not absences). Office=yes, Home=no, Hybrid=yes if ≥4 office hours
- **Vacation/sick/holiday**: all paid in full (hours × rate). Vacation+sick reduce quota, holiday does not
- **`work_days` in calc_salary**: pass `reimbursable_days`, not total work days

### Deployment
- GitHub repo: `github.com/Accenders/hours-tracker` (public)
- Hosted on Streamlit Community Cloud — auto-deploys on every `git push`
- Secrets (Google credentials) stored in Streamlit Cloud secrets manager, NOT in the repo
- To update the live app: make changes locally → `git push` → Streamlit rebuilds automatically (~1 min)

### Run Locally
```
cd /Users/yuvalmoradov/VSCode/hours-tracker && .venv/bin/streamlit run app.py --server.headless true
```
- RTL is activated via `app.py` only — no need to call it on every page
- Settings form keys start with `s_` (s_hourly_rate, s_meals, etc.) — must be preserved to avoid conflicts
- Local secrets file (gitignored): `.streamlit/secrets.toml`
