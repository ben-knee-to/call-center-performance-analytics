# Call Center Performance Analytics

**Python · PostgreSQL · Power BI · Statistical Analysis**

An end-to-end customer-service analytics portfolio project examining **32,941 interactions** recorded during **October 2020** across **four call centres** and **four communication channels**. 


## Executive summary

| Metric | Result |
|---|---:|
| Interactions | 32,941 |
| Average contact duration | 25.02 minutes |
| Average CSAT (scored contacts only) | 5.55 / 10 |
| CSAT scores available | 12,271 (37.25%) |
| CSAT scores missing | 20,670 (62.75%) |
| Within-SLA share | 62.61% |
| Negative or very negative sentiment | 51.88% |
| Billing enquiries | 23,462 (71.22%) |

## Business questions

1. Which channels and centres handle the most contacts?
2. How do satisfaction and SLA performance compare across groups?
3. Which reasons account for the most customer demand?
4. Where is negative sentiment concentrated?
5. How complete and representative are recorded satisfaction scores?

## Findings

- **Billing drives volume:** 23,462 of 32,941 interactions (71.22%) concern billing. Investigate recurring issues and opportunities for clearer billing communication and self-service.
- **Customer experience is a priority:** 51.88% of contacts are labelled negative or very negative. This is a descriptive finding, not proof of the cause of dissatisfaction.
- **CSAT coverage is limited:** 62.75% of interactions have no recorded score. All reported CSAT averages exclude missing scores; investigate potential response bias before generalising to all customers.
- **Observed centre differences are modest:** Denver has the highest observed centre CSAT (~5.62/10) and Chicago the lowest (~5.48/10), but one-way ANOVA across centres was not significant (p = 0.4414).
- **Observed channel differences are modest:** Call-Center had the highest observed channel CSAT (~5.61/10), Email the lowest (~5.48/10); across-channel ANOVA p = 0.0523. This does not meet the conventional 0.05 threshold.
- **SLA interpretation:** 62.61% of records are explicitly marked `Within SLA`. The meaning of `Above SLA` and `Below SLA` requires confirmation; do not assume either category is compliant.

### Statistical comparisons

| Comparison | Method | p-value |
|---|---|---:|
| CSAT across centres | One-way ANOVA | 0.4414 |
| CSAT across channels | One-way ANOVA | 0.0523 |
| CSAT across reasons | One-way ANOVA | 0.2487 |
| SLA status across centres | Chi-square | 0.4060 |
| SLA status across channels | Chi-square | 0.4034 |
| Negative sentiment across centres | Chi-square | 0.5460 |

These are exploratory, unadjusted tests. Failure to reject a null hypothesis is **not** proof of equal performance. The analysis is observational and cannot establish causality.

## Workflow

```text
Local CSV (not committed)
  -> Python cleaning and validation
  -> CSV EDA tables, charts and statistical tests
  -> PostgreSQL staging.call_center
  -> analytics.call_center and reporting views
  -> Power BI dashboard (to be completed and validated)
```

## Repository structure

```text
call_center_analytics/
├── data/
│   ├── raw/                 # Place call_center.csv here locally (gitignored)
│   └── processed/           # Generated clean CSV (gitignored)
├── src/
│   ├── clean_data.py
│   ├── analyze.py
│   ├── final_insights.py
│   └── load_postgres.py
├── sql/
│   ├── 01_schema.sql
│   ├── 02_views.sql
│   └── 03_checks.sql
├── outputs/
│   ├── charts/
│   └── tables/
├── dashboards/             # Add validated PBIX and screenshots
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Reproduce locally (Windows / PyCharm)

1. Clone this repository and open its folder in PyCharm. Use Python 3.11 or 3.12.
2. Put the source CSV at `data/raw/call_center.csv`. Do **not** commit customer-level data.
3. In the PyCharm terminal (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/clean_data.py
python src/analyze.py
python src/final_insights.py
```

The scripts generate `data/processed/call_center_clean.csv`, aggregated tables in `outputs/tables/`, and six charts in `outputs/charts/`. Check the console for data-quality errors.

### PostgreSQL (optional until the database is available)

1. In pgAdmin, create database `call_center_analytics`.
2. Connect to that database and run `sql/01_schema.sql`.
3. Copy `.env.example` to `.env`, then replace the placeholder with your local PostgreSQL connection credentials. **Never commit `.env`.**
4. Run:

```powershell
python src/load_postgres.py
```

5. In pgAdmin, run `sql/02_views.sql` and `sql/03_checks.sql` in order. Confirm 32,941 rows, 32,941 unique IDs and 12,271 non-null CSAT values. The loader truncates and fully reloads the staging table; it is **not** incremental.

### Power BI (not included as a finished artifact)

Connect Power BI Desktop to the `call_center_analytics` PostgreSQL database and import `analytics.call_center`. Build the following pages: Executive Overview, Channel Performance, Customer Experience, Operational Performance, Geographic Analysis. Use interaction-level measures for slicer-responsive charts; SQL summary views can serve as reconciliation references. Save your validated report in `dashboards/`.

## KPI definitions and caveats

- **Contacts:** count of distinct `id` values.
- **Average CSAT:** mean of non-null `csat_score` (scale 1–10).
- **CSAT response rate:** non-null CSAT scores / all contacts.
- **Within-SLA rate:** records where `response_time = 'Within SLA'` / all contacts.
- **Negative sentiment rate:** `Negative` or `Very Negative` / all contacts.
- **Average duration:** mean `call_duration_in_minutes`.
- There are no agent IDs, resolution outcomes, or measured response times. Do not claim first-contact resolution, agent productivity, or response-time savings.
- Data covers one month in 2020; it is not evidence of current operational performance.

## Data privacy and provenance

The supplied dataset contains customer names. Raw and processed interaction-level CSV files are excluded from Git by default. Share only aggregated outputs and anonymised screenshots unless you have permission to publish the underlying data. Add the verified original dataset URL and licensing terms here before making the repository public.

## Portfolio outcome

This project demonstrates Python data cleaning, KPI engineering, exploratory visualisation, hypothesis testing, PostgreSQL schema/view design, and Power BI reporting preparation. See `outputs/tables/` and `outputs/charts/` for reproducible analysis results.
