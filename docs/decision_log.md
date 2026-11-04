# Decision Log

Changes to earlier decisions are new entries that point to the old one ("Replaces D#"). Nothing is deleted.
"TO CONFIRM" = not stated in our documents yet. "—" in "Who decided" = not recorded, by team choice.

Last updated: 2026-11-04 (D20–D27 restored from `HANDOFF_for_Baraa.md`, section 12)

| ID | Date | Decision | Why | Alternatives rejected (and why) | Who decided | Applies to |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | TO CONFIRM (by 2026-11-02) | Use H2 Affordable Housing Production by Building + T4 SIRTA | Both have ZIP, borough and lat/long, so they can be joined | TO CONFIRM | Whole team | Whole project |
| D2 | 2026-11-02 | Analysis window: 1 Jan 2022 – 30 Jun 2026 | Only period both datasets cover | — | — | All questions |
| D3 | 2026-11-02 | Main join key = ZIP. Borough for Q12. Lat/long spatial join for Q8, Q11 | ZIP exists in both and is fine-grained | NTA: 2010 codes in housing vs 2020 in SIRTA. Census tract: 2010 vs 2020. Council district / community board: mostly empty in SIRTA | — | Integration, all questions |
| D4 | 2026-11-02 | Shared definitions: serious harm = severe injuries + fatalities; serious crash = one SIRTA record; completed units = All Counted Units by Building Completion Date; building size = Total Units; full years = 2022–2025 | Same meaning in every question | — | — | All questions |
| D5 | 2026-11-02 | Merge old Q2 and old Q8 into new Q2 (12-month windows, by building size) | Both measured the same before/after change | Keep both: duplicate | — | Q2 |
| D6 | 2026-11-02 | Replace old Q5 with fatality-rate question | Old Q5 repeated Q12 at monthly level | — | — | Q5 |
| D7 | 2026-11-02 | New Q8: dangerous corridors map | Freed slot; adds a map no other chart had | — | — | Q8 |
| D8 | 2026-11-02 | Q4 joins on ZIP + year | Council district mostly empty in SIRTA | Council district (rejected, see D3) | — | Q4 |
| D9 | 2026-11-02 | Q9 joins on ZIP | 2010 vs 2020 tract versions don't match | Census tract (rejected, see D3) | — | Q9 |
| D10 | 2026-11-02 | Q6 uses New Construction only | Preservation is not construction | Include all types: would count non-building sites | — | Q6 |
| D11 | 2026-11-03 | Q6 limited to buildings with 100+ units (working decision, re-check on cleaned data). Builds on D10 | With all sizes, most ZIPs are always "under construction" and can't be compared with themselves | All sizes: no comparison possible | — | Q6 |
| D12 | 2026-11-03 | Add main story question; Q5 also runs without highway crashes | Ties the 12 questions together; highways skew fatality rates | — | — | Story, Q5 |
| D13 | 2026-11-03 | Remove limitations and numbers from question docs; each owner writes limitations after their chart runs | Data not yet cleaned or joined | Write limitations up front: would be guesses | — | All questions |
| D14 | 2026-11-03 | Cleaning rules move to notebook cleaning sections (draft in `clean_helpers.py`) | They belong with the cleaning code | Keep in question doc | — | Cleaning |
| D15 | TO CONFIRM | Exclude highway crashes from Q8 and Q11 | Residents don't walk on highways | — | TO CONFIRM | Q8, Q11 |
| D16 | TO CONFIRM | Q11 uses lat/long distance (100 m, also tested at 250 m) | Spatial distance works for all crashes with coordinates | BBL: few crashes carry one | TO CONFIRM | Q11 |
| D17 | TO CONFIRM (by 2026-11-03) | Story told as 5 acts (big picture → where → building's life → nature of danger → limits/impact) | Lab 5 storytelling: context → insight → action | — | TO CONFIRM | Website story |
| D18 | TO CONFIRM (by 2026-11-03) | Each chart is one function in shared `charts.py`, used by notebook and website | One source of truth for charts | — | TO CONFIRM | Notebook, website |
| D19 | 2026-11-03 | Repo named `nyc-housing-street-safety`, public on GitHub | TO CONFIRM | TO CONFIRM | Mohamed Nazmy | Repo, submission |
| D20 | 2026-11-03 | Repo layout: `app/`, `data/raw/`, `data/processed/`, `docs/`, `notebooks/`, `src/` | Raw and processed data kept apart; shared code in `src` | — | Mohamed Nazmy | Repo |
| D21 | 2026-11-03 | Logs edited in Mohamed's local folder; repo holds copies | TO CONFIRM | Edit in repo | Mohamed Nazmy | Logs |
| D22 | 2026-11-03 | Postpone `charts.py` contract until before others code (done in `7ab0454`) | Nobody else working yet | Send conventions now | Mohamed Nazmy | `src/charts.py` |
| D23 | 2026-11-03 | Setup cell = brief's Listing 1 as given (no raw snapshot) | TO CONFIRM | Extended cell + raw snapshot in `data/raw` | Mohamed Nazmy | Notebook setup |
| D24 | 2026-11-03 | Members add their sections directly to the shared notebook | TO CONFIRM | Mohamed merges all | TO CONFIRM | Notebook |
| D25 | 2026-11-03 | Q1/Q2 work waits for cleaning + integration | Needs joined tables | Start on dummy data | Mohamed Nazmy | Q1, Q2 |
| D26 | 2026-11-03 | Postpone TA population question (drafts ready). Replaced by D29 | TO CONFIRM | Send now | Mohamed Nazmy | Q1, Q10, Q12 |
| D27 | 2026-11-04 | Mohamed passes work to Baraa; which tasks move: TO CONFIRM | TO CONFIRM | — | Mohamed Nazmy | Whole project |
| D28 | 2026-11-04 | Website hosted on Vercel (not Render). Framework stays Dash | TO CONFIRM | Render (earlier proposal) | Baraa Tantawy | Website, deployment |
| D29 | 2026-11-04 | No population data. Do not ask the TA. ZIP size differences become a stated limitation. Replaces D26 | Keeps to "exactly one dataset per domain" | Add Census ACS population as reference data (needed TA approval) | Baraa Tantawy | Q1, Q10, Q12, story limits |
| D30 | 2026-11-04 | Severity dropdown switches the **measure**, not the rows: All = serious harm (severe injuries + deaths), "Severe injuries" = severe injuries only, "Deaths" = fatalities only. Charts that count crashes (e.g. Q3, Q4) sum the chosen measure instead | Counts people harmed, the same unit as D4; works on the ZIP tables that already have `severe_injuries` and `fatalities`; no extra columns or row filtering needed | Keep only crashes without / with a death: mixes up crashes and people, a crash with both a death and a severe injury is hard to place, needs new columns in every aggregated table | Baraa Tantawy (on Claude's recommendation) | `src/charts.py`, `docs/data_dictionary.md`, all charts using severity |
| D31 | 2026-11-04 | Housing-type filter on ZIP and borough tables switches the units column (`units_column` helper); `units_all` added to `zip_year`, `zip_month`, `borough_year`; `borough_year.units_completed` split into `units_all` / `units_new_construction` / `units_preservation`. Contract rule added: a chart always returns a figure, even with no data | Those tables have no `construction_type` column, so the filter did nothing on them | Add `construction_type` rows to the ZIP tables (doubles their size) | Mohamed Nazmy | `src/charts.py`, `docs/data_dictionary.md` (commit `453f706`) |
| D32 | 2026-11-04 | Python 3.12 for everyone; exact package versions pinned; `requirements.txt` holds only the website packages (dash 4.5.0, pandas 2.3.3, numpy 2.5.4, plotly 7.1.0); `requirements-dev.txt` adds scikit-learn 1.9.1, scipy 1.18.1, jupyter 1.1.1. gunicorn dropped | Same results on every laptop and on Vercel; Mohamed's EDA ran on Python 3.12; pandas 3 changes default behaviour; Vercel installs the root `requirements.txt` and has a size limit, so notebook-only tools stay out of it | Python 3.14 (newest; Vercel support not confirmed); no pinned versions (each laptop gets different versions); one combined file (jupyter + scikit-learn make the Vercel install much bigger); gunicorn (only needed for Render) | Baraa Tantawy | `requirements.txt`, `requirements-dev.txt`, setup steps in README |
| D33 | 2026-11-04 | Fix the Windows `SSL: CERTIFICATE_VERIFY_FAILED` download error with `pip-system-certs` (Windows only, in `requirements-dev.txt`). No change to the loading code | Python on Windows couldn't complete the certificate chain; the site's certificate is genuine. The package makes Python use the Windows certificate store, so checks stay on | Turn off certificate checks (unsafe); download the CSVs by hand into `data/raw` (an extra manual step for every member, and the notebook would no longer match the brief's loading code) | Baraa Tantawy | `requirements-dev.txt`, notebook section 3 |

## Open decisions (not made yet)

| Topic | Options | Raised in |
| --- | --- | --- |
| Filter list | Borough, Year, Housing type, Crash severity + search box (proposal) | Story doc |
| Year filter for fixed-window charts (Q2, Q7, Q12) | Ignore the filter, or show a note | Story doc |
| Year filter on `buildings` (no `year` column) | Owners define it, or add `completion_year` | charts.py contract |
| Q1 and the housing-type filter | Q1 owner decides | charts.py contract |
| Where logs are edited after the handoff | Repo `docs/` (suggested) | Handoff |
| Final title and 2–3 headline findings | After charts run | Story doc |
