# Requirements Tracker

Source: *Project Milestone 1* description (deadline 9 Nov 2026) and *Dataset Catalog*.
Status: ✅ done · 🟡 partial · ❌ missing · ➖ not applicable.
Owners come from the *NYC DEV Team Tasks* plan.

Last updated: 2026-11-04 (after integration, notebook sections 8–9)

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
| R8 | 1 visualization per question (12 total) | 🟡 | Stubs in `src/charts.py`; no chart built yet | Each member |
| R9 | Each member's contributions clearly documented | 🟡 | `docs/contributions_log.md` up to date; notebook Contributions table and README still empty | Mohamed Nazmy (notebook table), Mostafa Ayman (README) |

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
| R20 | Descriptive markdown: justify decisions, alternatives, how insights were reached | 🟡 | Sections 2, 4, 5, 6, 7 done; rest empty | Each owner; Mohamed Nazmy (consistency) |
| R21 | Prompt log of every AI prompt used | 🟡 | Notebook 12.3: rows 1–11 in task order (one row per task), all members so far (Mohamed's from his own log, task-related prompts only). New rows needed for integration, charts, website, story | Mohamed Nazmy, each member |
| R22 | Dataset links in notebook | ✅ | Sections 2 and 12.1 | Mohamed Nazmy |
| R23 | Clean code: descriptive names, modular functions | 🟡 | `src/charts.py` structure; EDA cells use descriptive names | Everyone |
| R24 | Comments on complex logic (outliers, joins) | 🟡 | EDA, cleaning and integration cells commented (outlier rules, ZIP fill, BallTree joins); chart code not written yet | Everyone |
| R25 | Notebook runs top to bottom | 🟡 | Runs with no errors through section 9 (Python 3.12, 4 Nov; 64 code cells); section 10 (charts) still empty | Mohamed Nazmy |

## Website

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R26 | Multiple dropdown filters | 🟡 | `FILTER_OPTIONS` in `src/charts.py` (borough, year, housing type, severity) | Baraa Tantawy |
| R27 | Search mode that sets filters from typed text | 🟡 | Planned | Baraa Tantawy |
| R28 | "Generate Report" button updates all charts | 🟡 | `CHARTS` registry ready; app not built. **Missing = deduction** | Baraa Tantawy |
| R29 | Variety of interactive chart types (hover, zoom, filters) | 🟡 | 12 chart types planned | Each member |
| R30 | At least one chart showing both domains together | 🟡 | Q1 scatter planned (Q8 map as second) | Mohamed Nazmy |
| R31 | Story section: question, key findings, limitations, benefit to NYC | 🟡 | Story doc drafted; findings and limits pending | Mostafa Ayman |
| R32 | Real-time response, user-friendly, consistent layout | ❌ | — | Baraa Tantawy, Mostafa Ayman |
| R33 | Deployed on a free platform and fully tested | ❌ | Vercel (D28); website-only `requirements.txt` ready (D32) | Baraa Tantawy |

## Repo and submission

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R34 | All code, notebook and website files in a GitHub repo | 🟡 | Structure, notebook, `charts.py`, logs, processed data (`data/processed/`) and loader pushed; app missing | Whole team |
| R35 | README: setup, deployment, each member's contribution | ❌ | — | Mostafa Ayman |
| R36 | Story quality: clear question, honest limits, no unsupported causal claims | 🟡 | Story doc framework | Mostafa Ayman, everyone |
| R37 | One email to ICS503Data@gmail.com: member IDs, repo link, deploy link, dataset links | ❌ | Member IDs still TO CONFIRM | Baraa Tantawy |
| R38 | Everything in the repo before 9 Nov 2026 | ❌ | — | Whole team |
