# Decision Log

Changes to earlier decisions are new entries that point to the old one ("Replaces D#"). Nothing is deleted.
"TO CONFIRM" = not stated in our documents yet. "—" in "Who decided" = not recorded, by team choice.

Last updated: 2026-11-03

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

## Open decisions (not made yet)

| Topic | Options | Raised in |
| --- | --- | --- |
| Filter list | Borough, Year, Housing type, Crash severity + search box (proposal) | Story doc |
| Year filter for fixed-window charts (Q2, Q7, Q12) | Ignore the filter, or show a note | Story doc |
| Framework and host | Dash + Render (proposal) | Story doc |
| Population per ZIP (Census ACS) as reference data | Ask TA | Research Questions doc, Story doc |
| Final title and 2–3 headline findings | After charts run | Story doc |
