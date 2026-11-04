# Requirements Tracker

Source: *Project Milestone 1* description (deadline 9 Nov 2026) and *Dataset Catalog*.
Status: ✅ done · 🟡 partial · ❌ missing · ➖ not applicable.
Owners come from the *NYC DEV Team Tasks* plan.

Last updated: 2026-11-04 (after SIRTA EDA, notebook section 5)

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
| R12 | Cleaning: missing values, drop vs impute justified | ❌ | Sections 6.1, 7.1 empty | Mostafa Alaa, Ali Issa |
| R13 | Cleaning: outliers detected and handled (IQR, domain rules) | ❌ | Sections 6.2, 7.2 empty (EDA already shows IQR vs domain rules) | Mostafa Alaa, Ali Issa |
| R14 | Cleaning: inconsistent data checked | ❌ | Sections 6.3, 7.3 empty | Mostafa Alaa, Ali Issa |
| R15 | Cleaning: formats standardized (dates, strings, categories, geo IDs) | ❌ | Sections 6.4, 7.4 empty | Mostafa Alaa, Ali Issa |
| R16 | Cleaning: duplicates removed | ❌ | Sections 6.5, 7.5 empty | Mostafa Alaa, Ali Issa |
| R17 | Integration documented: join key, granularity and aggregation justified | 🟡 | Plan in section 2; section 8 empty | Moustafa Maged |
| R18 | Post-integration cleaning: join NaNs, redundant columns, dtype mismatches | ❌ | Section 9 empty. **Missing = deduction** | Moustafa Maged |
| R19 | Visualizations that validate cleaning steps | ❌ | Sections 6.6, 7.6 empty | Mostafa Alaa, Ali Issa |
| R20 | Descriptive markdown: justify decisions, alternatives, how insights were reached | 🟡 | Sections 2, 4, 5 done; rest empty | Each owner; Mohamed Nazmy (consistency) |
| R21 | Prompt log of every AI prompt used | 🟡 | Notebook 12.3: rows 1–4 (4 Nov). Mohamed's earlier prompts (C7) not added yet | Mohamed Nazmy, each member |
| R22 | Dataset links in notebook | ✅ | Sections 2 and 12.1 | Mohamed Nazmy |
| R23 | Clean code: descriptive names, modular functions | 🟡 | `src/charts.py` structure; EDA cells use descriptive names | Everyone |
| R24 | Comments on complex logic (outliers, joins) | 🟡 | EDA cells commented; joins not written yet | Everyone |
| R25 | Notebook runs top to bottom | 🟡 | Runs with no errors through section 5 (Python 3.12, 4 Nov); later sections still empty | Mohamed Nazmy |

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
| R34 | All code, notebook and website files in a GitHub repo | 🟡 | Structure, notebook, `charts.py`, logs pushed; app and processed data missing | Whole team |
| R35 | README: setup, deployment, each member's contribution | ❌ | — | Mostafa Ayman |
| R36 | Story quality: clear question, honest limits, no unsupported causal claims | 🟡 | Story doc framework | Mostafa Ayman, everyone |
| R37 | One email to ICS503Data@gmail.com: member IDs, repo link, deploy link, dataset links | ❌ | Member IDs still TO CONFIRM | Baraa Tantawy |
| R38 | Everything in the repo before 9 Nov 2026 | ❌ | — | Whole team |
