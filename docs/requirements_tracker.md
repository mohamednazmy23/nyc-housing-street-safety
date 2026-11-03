# Requirements Tracker

Source: *Project Milestone 1* description (deadline 9 Nov 2026) and *Dataset Catalog*.
Status: ✅ done · 🟡 partial · ❌ missing · ➖ not applicable.
Owners come from the *NYC DEV Team Tasks* plan.

Last updated: 2026-11-03

## Datasets

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R1 | Exactly one housing + one transportation dataset from NYC Open Data | ✅ | H2 Affordable Housing Production by Building (`hg8x-zxpr`) + T4 SIRTA (`xeqp-qz8h`) | Whole team |
| R2 | Each dataset has at least 9 columns | 🟡 | Expected yes; TO CONFIRM with `df.shape` in notebook | Mohamed Nazmy (housing), Ali Issa (SIRTA) |
| R3 | At least one meaningful integration attribute | ✅ | ZIP, borough, lat/long (Research Questions doc) | Whole team |
| R4 | Feasibility check if a dataset is outside the catalog | ➖ | Both datasets are in the catalog (H2, T4) | — |
| R5 | Large datasets: justify any filtered sample | 🟡 | Portal lists ~9.5k and ~13.8k rows, so full download likely; TO CONFIRM and state in notebook | Mohamed Nazmy, Ali Issa |

## Team and questions

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R6 | Team of 4–6 | ✅ | 6 members | — |
| R7 | 2 research questions per member (12 total), cross-domain | ✅ | Research Questions doc, Q1–Q12 | Each member |
| R8 | 1 visualization per question (12 total) | 🟡 | Chart types planned; no chart built yet | Each member |
| R9 | Each member's contributions clearly documented (questions, charts, cleaning, integration, website, other) | 🟡 | Team Tasks plan + `docs/contributions_log.md` started | Mohamed Nazmy (log), Mostafa Ayman (README) |

## Notebook

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R10 | Dataset overview for both (rows, columns, geo/time attributes, known issues, selection reasoning, aggregation plan) | ❌ | — | Mohamed Nazmy (housing), Ali Issa (SIRTA) |
| R11 | EDA with descriptive statistics and initial plots | ❌ | — | Mohamed Nazmy, Ali Issa |
| R12 | Cleaning: missing values, drop vs impute justified | ❌ | — | Mostafa Alaa, Ali Issa |
| R13 | Cleaning: outliers detected and handled (IQR, domain rules) | ❌ | — | Mostafa Alaa, Ali Issa |
| R14 | Cleaning: inconsistent data checked | ❌ | — | Mostafa Alaa, Ali Issa |
| R15 | Cleaning: formats standardized (dates, strings, categories, geo IDs) | ❌ | — | Mostafa Alaa, Ali Issa |
| R16 | Cleaning: duplicates removed | ❌ | — | Mostafa Alaa, Ali Issa |
| R17 | Integration documented: join key, granularity and aggregation justified | 🟡 | Planned in Research Questions doc; not built | Moustafa Maged |
| R18 | Post-integration cleaning: join NaNs, redundant columns, dtype mismatches | ❌ | — | Moustafa Maged |
| R19 | Visualizations that validate cleaning steps | ❌ | — | Cleaning owners |
| R20 | Descriptive markdown: justify decisions, alternatives, how insights were reached | ❌ | `docs/data_work_notes.md` will feed this | Mohamed Nazmy (consistency), each owner |
| R21 | Prompt log of every AI prompt used | ❌ | — | Mohamed Nazmy |
| R22 | Dataset links in notebook | 🟡 | Links in Research Questions doc; not yet in notebook | Mohamed Nazmy |
| R23 | Clean code: descriptive names, modular functions | ❌ | Plan: shared `charts.py` | Everyone |
| R24 | Comments on complex logic (outliers, joins) | ❌ | — | Everyone |
| R25 | Notebook runs top to bottom | ❌ | — | Mohamed Nazmy |

## Website

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R26 | Multiple dropdown filters | 🟡 | Proposed in Story doc (borough, year, housing type, severity); TO CONFIRM by team | Baraa Tantawy |
| R27 | Search mode that sets filters from typed text | 🟡 | Proposed in Story doc | Baraa Tantawy |
| R28 | "Generate Report" button updates all charts | 🟡 | Planned | Baraa Tantawy |
| R29 | Variety of interactive chart types (hover, zoom, filters) | 🟡 | 12 chart types planned | Each member |
| R30 | At least one chart showing both domains together | 🟡 | Q1 scatter planned (Q8 map as second) | Mohamed Nazmy |
| R31 | Story section: question, key findings, limitations, benefit to NYC | 🟡 | Story doc drafted; findings and limits pending | Mostafa Ayman |
| R32 | Real-time response, user-friendly, consistent layout | ❌ | — | Baraa Tantawy, Mostafa Ayman |
| R33 | Deployed on a free platform and fully tested | ❌ | Render planned | Baraa Tantawy |

## Repo and submission

| ID | Requirement | Status | Where | Owner |
| --- | --- | --- | --- | --- |
| R34 | All code, notebook and website files in a GitHub repo | 🟡 | Repo created (public): https://github.com/mohamednazmy23/nyc-housing-street-safety; folder structure not pushed yet | Mohamed Nazmy (setup) |
| R35 | README: setup, deployment, each member's contribution | ❌ | — | Mostafa Ayman |
| R36 | Story quality: clear question, honest limits, no unsupported causal claims | 🟡 | Story doc framework | Mostafa Ayman, everyone |
| R37 | One email to ICS503Data@gmail.com: member IDs, repo link, deploy link, dataset links | ❌ | — | Baraa Tantawy |
| R38 | Everything in the repo before 9 Nov 2026 | ❌ | — | Whole team |
