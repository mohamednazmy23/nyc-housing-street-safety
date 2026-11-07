# Requirements Tracker

Source: *Project Milestone 1* description (deadline 9 Nov 2026) and *Dataset Catalog*.
Status: ✅ done · 🟡 partial · ❌ missing · ➖ not applicable.
Owners come from the *NYC DEV Team Tasks* plan.

Last updated: 2026-11-07 (final pass)

## Datasets

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R1 | Exactly one housing + one transportation dataset from NYC Open Data | ✅ | H2 Affordable Housing Production by Building (`hg8x-zxpr`) + T4 SIRTA (`xeqp-qz8h`) | Whole team |
| R2 | Each dataset has at least 9 columns | ✅ | 41 and 23 columns (`.shape` in notebook sections 4 and 5) | Mohamed Nazmy (housing), Ali Issa (SIRTA) |
| R3 | At least one meaningful integration attribute | ✅ | ZIP, borough, lat/long | Whole team |
| R4 | Feasibility check if a dataset is outside the catalog | ➖ | Both datasets are in the catalog (H2, T4) | — |
| R5 | Large datasets: justify any filtered sample | ✅ | No sampling; reason in notebook section 2 ("Size") | Mohamed Nazmy |

## Team and questions

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R6 | Team of 4–6 | ✅ | 6 members | — |
| R7 | 2 research questions per member (12 total), cross-domain | ✅ | Research Questions doc, Q1–Q12 | Each member |
| R8 | 1 visualization per question (12 total) | ✅ | All 12 in `src/charts.py` and notebook 10.1–10.12, each with finding and limitations; all tested on 324 filter combinations | Each member |
| R9 | Each member's contributions clearly documented | ✅ | Notebook Contributions table; README team table; `docs/contributions_log.md` (C1–C45) | Whole team |

## Notebook

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R10 | Dataset overview for both | ✅ | Sections 2, 4 (housing), 5 (SIRTA) | Mohamed Nazmy, Ali Issa |
| R11 | EDA with descriptive statistics and initial plots | ✅ | Section 4 (housing), section 5 (SIRTA: 3 plots, 5.x summary of 14 issues) | Mohamed Nazmy, Ali Issa |
| R12 | Cleaning: missing values, drop vs impute justified | ✅ | Housing 6.1; SIRTA 7.1 | Mostafa Alaa, Ali Issa |
| R13 | Cleaning: outliers detected and handled (IQR, domain rules) | ✅ | Housing 6.2; SIRTA 7.2 | Mostafa Alaa, Ali Issa |
| R14 | Cleaning: inconsistent data checked | ✅ | Housing 6.3; SIRTA 7.3 | Mostafa Alaa, Ali Issa |
| R15 | Cleaning: formats standardized (dates, strings, categories, geo IDs) | ✅ | Housing 6.4; SIRTA 7.4 | Mostafa Alaa, Ali Issa |
| R16 | Cleaning: duplicates removed | ✅ | Housing 6.5 (none found); SIRTA 7.5 (1 repeated ID resolved) | Mostafa Alaa, Ali Issa |
| R17 | Integration documented: join key, granularity and aggregation justified | ✅ | Section 8 (keys, ZIP fill tested, levels, distance join), D49–D52 | Moustafa Maged |
| R18 | Post-integration cleaning: join NaNs, redundant columns, dtype mismatches | ✅ | Section 9.1–9.3 (NaNs → 0, 17 checks, type fixes), D53 | Moustafa Maged |
| R19 | Visualizations that validate cleaning steps | ✅ | 6.6 and 7.6: missing-cells charts (raw vs clean) and usable-rows charts | Mostafa Alaa, Ali Issa |
| R20 | Descriptive markdown: justify decisions, alternatives, how insights were reached | ✅ | Every section 1–12: explanation after each code cell, decisions with alternatives, summary tables, findings and limitations | Each owner |
| R21 | Prompt log of every AI prompt used | ✅ | Notebook 12.3: one row per task, in task order, every member (rows 1–21) | Each member |
| R22 | Dataset links in notebook | ✅ | Sections 2 and 12.1 | Mohamed Nazmy |
| R23 | Clean code: descriptive names, modular functions | ✅ | `src/` and `app/`: one data function + one chart function per question, shared helpers; no unused imports (read-through 7 Nov) | Everyone |
| R24 | Comments on complex logic (outliers, joins) | ✅ | Outlier rules, ZIP fill, BallTree joins, equal groups, search rules and deployment all commented | Everyone |
| R25 | Notebook runs top to bottom | ✅ | Final run 7 Nov: 88 code cells, no errors, outputs saved (Python 3.12) | Mohamed Nazmy |

## Website

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R26 | Multiple dropdown filters | ✅ | 4 dropdowns in the pinned filter bar (`app/app.py`): borough, year, housing type, crash measure | Baraa Tantawy |
| R27 | Search mode that sets filters from typed text | ✅ | `src/search.py` (on Enter); e.g. "Brooklyn 2022 new buildings" sets borough, year and housing type; "citywide" resets borough; ignored words and extra values reported; `tests/test_search.py` | Baraa Tantawy |
| R28 | "Generate Report" button updates all charts | ✅ | One callback redraws all 12 charts (about 1 s); Enter in the search box does the same | Baraa Tantawy |
| R29 | Variety of interactive chart types (hover, zoom, filters) | ✅ | Scatter (Q1, Q7), line (Q2, Q4), heatmap (Q3, Q9), bar (Q5, Q6, Q10), stacked bar (Q11), map + bar (Q8), animated bubble (Q12); hover on all; zoom on all; filters per the Story table | Each member |
| R30 | At least one chart showing both domains together | ✅ | Q1 scatter (housing units vs serious harm per ZIP) and Q8 map (crashes and buildings together) | Mohamed Nazmy, Baraa Tantawy |
| R31 | Story section: question, key findings, limitations, benefit to NYC | ✅ | Website hero, 5 acts with panels, headline findings, limits, impact table (`app/story.py`); notebook sections 1 and 11 | Mostafa Ayman |
| R32 | Real-time response, user-friendly, consistent layout | ✅ | Live site: every report in 1.6–3.4 s, one style, pinned filters, mobile layout | Baraa Tantawy, Mostafa Ayman |
| R33 | Deployed on a free platform and fully tested | ✅ | Vercel: https://nyc-housing-street-safety.vercel.app; tested live (page, scripts, Generate Report, search, Reset, narrow filters), D74 | Baraa Tantawy |

## Repo and submission

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R34 | All code, notebook and website files in a GitHub repo | ✅ | Notebook, `src/`, `app/`, processed data, tests and logs on `main` | Whole team |
| R35 | README: setup, deployment, each member's contribution | ✅ | `README.md`: findings, data, repository, setup, notebook, website, tests, deployment, team and contributions | Mostafa Ayman |
| R36 | Story quality: clear question, honest limits, no unsupported causal claims | ✅ | Notebook sections 1 and 11, website story; "correlation is not causation" on scatter charts; limitations under every question | Mostafa Ayman, everyone |
| R37 | One email to ICS503Data@gmail.com: member IDs, repo link, deploy link, dataset links | ❌ | Everything collected (IDs, repo, live site, datasets); to send | Baraa Tantawy |
| R38 | Everything in the repo before 9 Nov 2026 | ✅ | Notebook, website, data, tests, README and logs on `main` (7 Nov) | Whole team |
