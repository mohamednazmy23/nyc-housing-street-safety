# Data Work Notes

Written to paste straight into notebook markdown cells.
Numbers here come only from code we actually ran.

Last updated: 2026-11-04

## Status

| Step | Status | Notebook section |
| --- | --- | --- |
| Housing overview + EDA | ✅ (Mohamed Nazmy, 3 Nov) | 4 (summary table 4.x) |
| SIRTA overview + EDA | ✅ (Ali Issa, 4 Nov) | 5 (summary table 5.x) |
| Housing cleaning | ✅ (Mostafa Alaa, 4 Nov) | 6 (summary table 6.x) |
| SIRTA cleaning | ❌ | 7 |
| Integration | ❌ | 8 |
| Post-integration cleaning + export | ❌ | 9 |

## Dataset overview (verified in code, 4 Nov 2026)

| | Housing | Transportation |
| --- | --- | --- |
| Dataset | [Affordable Housing Production by Building](https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data) | [SIRTA](https://data.cityofnewyork.us/Transportation/Serious-Injury-Response-Tracking-Analysis-Program-/xeqp-qz8h/about_data) |
| ID | `hg8x-zxpr` | `xeqp-qz8h` |
| Rows × columns | 9,551 × 41 | 13,754 × 23 (13,310 crash rows; 13,309 distinct crashes) |
| Date range | Building completions 3 Jan 2014 – 21 Aug 2026 | Crashes 1 Jan 2022 – 30 Jun 2026 |
| Geo fields | Postcode, Borough, Latitude/Longitude | ZipCode, Crash Borough, Latitude/Longitude, On Street, Cross Street |
| Time fields | Project Start Date, Building Completion Date | Crash Date, Crash Time |

## Steps

### Housing overview and EDA (Mohamed Nazmy, 3 Nov 2026)
See notebook section 4 and its 4.x summary table (13 issues). Not repeated here.

### SIRTA overview and EDA (Ali Issa, 4 Nov 2026)

**What and how:** full download with Listing 1; `.shape`, column list, missing-value table; checks on the rows with no Collision ID; borough vs police precinct; date and time parsing (`%m/%d/%Y`, `%H:%M`); counts at 00:00 against nearby minutes; injury counts with `describe`, IQR fences and domain rules; lookback columns; ZIP and coordinate coverage overall and by year; ZIP values; NYC bounding box; duplicate rows and Collision IDs; street-name spellings and highway-type names. Plots: crashes by hour, crashes per month, ZIP/coordinate coverage by year.

**Why:** cleaning (section 7) and integration (section 8) need to know what is broken before fixing it. Every fix in 7 points back to an issue number in 5.x.

**Before (raw) numbers, all from code output:**

| Check | Result |
| --- | --- |
| Rows with no Collision ID | 444 (3.2%). Only Community Board, Council District, Census Tract, NTA (444) and BIN/BBL (433) are filled. 3 are identical |
| Crash rows | 13,310; one Collision ID (4597666) used twice → 13,309 distinct crashes |
| Borough missing (crash rows) | 55, all police precinct 116; precinct ranges per borough do not overlap (Manhattan 1–34, Bronx 40–52, Brooklyn 60–94, Queens 100–115, Staten Island 120–123) |
| Dates | All parse; 1 Jan 2022 – 30 Jun 2026. Per year: 2,879 · 3,016 · 3,116 · 2,947 · 1,352 (2026, Jan–Jun) |
| Times | All parse with `%H:%M`; 656 written `H:MM`. 227 at 00:00 vs 11 at 00:01, 36 at 01:00 |
| Injury counts | No negatives; every crash has ≥ 1 severe injury or death. Max 19 non-severe, 7 severe, 5 deaths. IQR fences 0 / 1 / 0 flag 2,172 / 824 / 1,047 crashes |
| Severe-injury lookback | Missing for 1,393 crashes: 766 in 2023, 627 in 2024, none in other years |
| All-injury lookback | Max 296 (Verrazano Bridge Upper) |
| ZIP | Missing for 5,238 crash rows (39.4%); 4,091 of them have coordinates, 1,147 have neither. ZIP filled: 16.3% (2022), 68.1% (2023), 70.0% (2024), 80.3% (2025), 74.0% (2026) |
| ZIP values | 187 distinct; 10000–11694. 44 crashes have ZIP 10000 (not a postal ZIP): only 6 have coordinates, and those fall in the Central Park area; 2 name park drives (West Drive, East Drive); the rest have no location |
| Coordinates | 0 outside the NYC box; filled 89.0% (2022), 81.5%, 66.2%, 88.1%, 87.6% |
| Highway | Marker filled for 1,052 crashes, 1,049 of them without ZIP. Up to 679 more crashes on highway-type names without a marker; the word search also catches residential streets (Eastern Parkway, Ocean Parkway, Kings Highway: at least 123 crashes), so the real number is lower |
| Street names | 2,952 distinct; mixed AVE/AVENUE, ST/STREET, BLVD/BOULEVARD, PKWY/PARKWAY, EXPY/EXPRESSWAY; typos (e.g. AVNEUE); 84 crashes with non-upper-case names; 1 with a double space. `ST` = Street as the last word (1,130 crashes), Saint as the first word (20) |
| Duplicates | 3 rows are exact copies of another row, all among the 444 empty rows; no crash row repeated in full |
| Seasons and hours | Crashes peak at 17:00–18:00 (849, 834), fewest at 05:00 (266); more crashes May–October than January–February |

**How we saw it:** the missing-value table showed 444 rows missing together; the hour chart showed the midnight spike; the coverage bar chart showed the 2022 ZIP gap.

**Alternatives considered:**
- IQR for injury outliers → rejected: with medians of 0–1 it flags every multi-victim crash. Domain rules used instead.
- Highway flag from a word search on street names → rejected: catches residential streets (Eastern Parkway, Ocean Parkway, Kings Highway). Suggest marker + a written list of limited-access roads.
- Filling missing lookback with 0 → rejected: 0 means "not a repeat location", which we don't know.

**Main consequence:** without filling ZIPs from coordinates, 2022 would have ZIPs for only 16.3% of crashes, which would break Q7 and Q10 (both use 2022 as the baseline).

### Housing pre-integration cleaning (Mostafa Alaa, 4 Nov 2026)

**What and how:** works on a copy of `df_housing`; result `housing_clean` (9,551 rows × 38 columns, data-dictionary names). Decisions D34–D41; full table in notebook 6.x. Count completions with `completed_in_window`, not `is_completed`.

**Checks that settled the open questions from the handoff (section 19, item 18):**

| Question | Answer from code |
| --- | --- |
| Do empty bedroom and tenure cells mean 0, like income tiers? | Yes: all three groups add up to All Counted Units in 9,522 of 9,522 rows with a total; no cell is ever written as 0 |
| The 9 non-confidential rows without location? | 8 New Construction, not completed; 1 single-unit preservation home (2019) |
| Missing Building ID = confidential rows? | Yes, exactly the 1,949 confidential rows |
| 2026 completions after 30 Jun? | 16 buildings |

**Other numbers from code output:**

| Check | Result |
| --- | --- |
| `----` placeholders | 1,949 rows (3,898 cells), exactly the confidential rows → missing |
| Empty breakdown cells filled with 0 | 106,280 |
| Missing All Counted Units | 29; breakdowns all 0; 18 completed, 1 in the window; 2,525 Total Units |
| Missing completion date | 1,666; 1,653 also no project completion; start years 2023–2026: 1,341; started before 2022: 243 (before 2020: 124; New Construction 100+ units: 14 — Q6 caveat) |
| IQR fence / above | 72 units / 1,249 buildings; 0 domain-rule breaks |
| Size groups (Total Units) | 7,309 small · 1,698 medium · 544 large |
| Completed before start | 20 (1 in the window); 0 completed after project completion; 166 complete while project isn't |
| Buildings in several projects | 123 buildings, 247 rows (107 Preservation twice, 13 New Construction twice); 2 completed twice in the window: 2864/2886 Atlantic Ave (two addresses) and 1184 River Ave (250 units in both phases, may be double-counted) |
| Placeholder BINs | 482 (3000000: 177, 2000000: 153, 4000000: 90, 1000000: 43, 5000000: 19) |
| Coordinate pairs | median 21 m apart (north–south), max 1,129 m; Latitude only: 86 rows |
| Duplicates | 0 full, 0 project + building, 0 confidential look-alikes |
| Before → after | rows 9,551 → 9,551; columns 41 → 38; affordable units 320,946 → 320,946. Missing cells: 16 breakdown columns → 0; number/street 0 → 1,949 (placeholders exposed); others unchanged (bar chart in 6.6) |
| Completed in window / after it | 3,415 / 16 (Jul–Aug 2026) |
| Usable buildings | 9,551 borough · 7,593 with ZIP · 2,599 completed in window · 1,670 New Construction |
| Units completed 1 Jan 2022 – 30 Jun 2026 | 115,547 (114,249 in buildings with a ZIP): 58,687 New Construction + 56,860 Preservation. Matches the hook's "about 115,500", but the hook should say "completed or preserved", or use 58,687 for newly built homes |

**Alternatives considered:** see the "Alternatives rejected" lines in each 6.x markdown cell and D34–D41.
