# Contributions Log

Only work that is done goes here. "TO CONFIRM" = author not stated yet.

Last updated: 2026-11-04 (C6–C12 restored from `HANDOFF_for_Baraa.md`, section 14)

## Completed work

| ID | Date | Who | What | Why | How | Where |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 2026-11-02, revised 2026-11-03 | Mohamed Nazmy | Research Questions doc: 12 questions, shared definitions, integration plan per question, join keys used/rejected, change log | Brief requires 2 cross-domain questions per member with one chart each | Wrote each question with why it matters, integration and visualization; merged/replaced overlapping questions (see D5–D7) | `NYC DEV Project – Research Questions.md` |
| C2 | 2026-11-03 | Baraa Tantawy | Questions Summary doc: short version of the 12 questions | Quick reference for the team | Condensed the Research Questions doc | `NYC DEV Project – Questions Summary.md` |
| C3 | 2026-11-03 | Baraa Tantawy | Story doc: big idea, title, hook, 5-act arc, chart title templates, hypotheses, filter proposal, team checklist | Brief requires a story section and a clear "so what" | Applied Lab 5 storytelling rules | `NYC DEV Project – Story` (Claude Doc / PDF) |
| C4 | TO CONFIRM | Baraa Tantawy | Team Tasks plan: roles, question owners, order of work | Brief requires clear member contributions | — | `NYC DEV Team Tasks.pdf` |
| C5 | 2026-11-03 | Mohamed Nazmy | GitHub repo `nyc-housing-street-safety` (public), with README (title + one-line description) and Python `.gitignore` | Brief requires all code, notebook and website files in a GitHub repo | Created on GitHub with README and Python `.gitignore` template; initial commit `a04fa9b` | https://github.com/mohamednazmy23/nyc-housing-street-safety |
| C6 | 2026-11-03 | Mohamed Nazmy | Folder structure, `requirements.txt`, the 4 logs | Shared layout for the team (D20) | — | commit `cb6cbfc` |
| C7 | 2026-11-03 | Mohamed Nazmy | AI prompt log started | Brief requires the prompts used in every step | — | Location TO CONFIRM |
| C8 | 2026-11-03 | Mohamed Nazmy | Notebook skeleton, setup cell, section 2 (datasets), section 4 (housing overview + EDA) | Brief requires dataset overview and EDA | Listing 1 loading; missing values, categories, dates, IQR, duplicates, 4.x issue summary | commit `73dc61a`, `notebooks/nyc_dev_project.ipynb` |
| C9 | 2026-11-03 | Mohamed Nazmy | Notebook appendix 12.1–12.3 (dataset links, definitions, prompt-log headers) | Brief requires dataset links and prompt log | — | commit `f234864` |
| C10 | TO CONFIRM | Baraa Tantawy | Team rules posted to the group (contents TO CONFIRM) | — | — | Group chat |
| C11 | 2026-11-03 / 2026-11-04 | Mohamed Nazmy | `src/charts.py` contract (12 stubs, filters, style, `CHARTS` registry) + `docs/data_dictionary.md`; later `units_column` helper, `units_all`, "always return a figure" rule | One shared chart file for notebook and website (D18, D31) | — | commits `7ab0454`, `453f706` |
| C12 | 2026-11-04 | Mohamed Nazmy | Handoff file for Baraa (drafted with Claude) | Pass the work on | — | `HANDOFF_for_Baraa.md` |
| C13 | 2026-11-04 | Baraa Tantawy | Decisions D28–D30 (Vercel, no population data, severity filter as measure switch); restored D20–D27 in the repo log; severity labels in `charts.py` and data dictionary | Repo log was behind the handoff; filter meaning had to be fixed before charts are written | Pull request #1 (merged) | `docs/decision_log.md`, `src/charts.py`, `docs/data_dictionary.md` |
| C14 | 2026-11-04 | Baraa Tantawy | Python 3.12 venv; exact package versions; website requirements split from notebook requirements (D32) | Same versions for everyone and for Vercel; keep Vercel install small | `requirements.txt` = website (dash, pandas, numpy, plotly); `requirements-dev.txt` = website + scikit-learn, scipy, jupyter | `requirements.txt`, `requirements-dev.txt` |

## Assigned work (plan, not done yet)

From the Team Tasks plan. Moves to "Completed work" when finished.

| Member | Role | Tasks | Questions |
| --- | --- | --- | --- |
| Mohamed Nazmy | Notebook lead | Repo + notebook setup; housing overview + EDA; merge sections; markdown consistency; AI prompt log | Q1, Q2 |
| Mostafa Alaa | Housing cleaning | Housing pre-integration cleaning (dates, units, confidential rows, duplicates, outliers), justified in markdown | Q9, Q10 |
| Ali Issa | SIRTA | SIRTA overview + EDA; cleaning (empty rows, borough fill, 00:00 times, outliers) | Q3, Q4 |
| Moustafa Maged | Integration | Fill missing ZIPs; joined tables (ZIP×year, ZIP×month, borough×year); building-level spatial join; post-integration cleaning; export CSVs | Q11, Q12 |
| Baraa Tantawy | Website core | Dash layout, dropdowns, search, Generate Report; plug in 12 charts; deploy on Vercel (D28) | Q7, Q8 |
| Mostafa Ayman | Story + presentation | Website story text; chart style; README; 10-second test | Q5, Q6 |
