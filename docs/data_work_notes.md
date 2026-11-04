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
| SIRTA cleaning | ✅ (Ali Issa, 4 Nov) | 7 (summary table 7.x) |
| Integration | ✅ (Moustafa Maged, 4 Nov) | 8 |
| Post-integration cleaning + export | ✅ (Moustafa Maged, 4 Nov) | 9 (summary table 8–9) |

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

### SIRTA pre-integration cleaning (Ali Issa, 4 Nov 2026)

**What and how:** works on a copy of `df_transport`; result `crashes_clean` (13,309 rows × 22 columns, data-dictionary names). Decisions D42–D48; full table in notebook 7.x.

| Check | Result (from code output) |
| --- | --- |
| Empty rows | 444 dropped; none had any crash field |
| Borough | Precinct ranges agree in 13,255 of 13,255 crashes; 55 filled (all precinct 116 → Queens) |
| Street | On Street missing for 2,592; Address fills 2,577 (the two are never filled together); 15 left without a street; 0 address streets reduced to a street-type word |
| Unknown time | 227 crashes at 00:00 → hour missing, `time_unknown` |
| Lookback | 1,393 missing, kept missing; `repeat_location` missing too |
| ZIP | 5,238 missing before dedupe (4,091 with coordinates, left for section 8); 5,237 after |
| Domain rules | 0 broken; harm per crash: 12,351 × 1, 752 × 2, 143 × 3, 47 × 4, 17 × 5–7 |
| Street names | 2,952 → 2,057 spellings among crashes with On Street; 2,319 names in total |
| Highway | Marker 1,052; limited-access list 1,422; both 1,031; total 1,443 (+391); 0 of 189 residential-parkway crashes flagged; 42 unflagged names with a highway-type word, all local roads |
| Repeated ID 4597666 | Other Jan 2023 IDs 4,594,367–4,610,898; other Jan 2026 IDs 4,868,827–4,884,702 → kept 13 Jan 2023, fatalities 1 |
| Before → after | rows 13,754 → 13,309; columns 23 → 22; borough missing 499 → 0; street missing 3,036 → 15; severe injuries 13,463 → 13,462; deaths 1,102 → 1,102 |
| Usable crashes | 13,309 borough · 12,163 with a ZIP after section 8 (8,072 now) · 10,868 with coordinates · 9,854 non-highway with coordinates (Q8, Q11) · 13,082 with hour (Q3) · 11,916 with lookback (Q4) |
| Story hook | 13,309 crashes ✓; deaths 1,102. The hook's 1,101 equals the first raw row per Collision ID (printed in 7.6); it may also come from an earlier export |

**Alternatives considered:** see the "Alternatives rejected" lines in each 7.x markdown cell and D42–D48.

### Integration and post-integration cleaning (Moustafa Maged, 4 Nov 2026)

**What and how:** join keys checked; missing crash ZIPs filled from the nearest located point; three aggregated tables on full grids; distance join; NaNs, columns and types cleaned; six tables exported. Decisions D49–D53; summary table in notebook 8–9.

| Check | Result (from code output) |
| --- | --- |
| ZIPs | housing 158, crashes 187, both 155; only housing: 10044, 10158, 10303; only crashes: 32 |
| ZIP-fill test (6,771 crashes with a known postal ZIP; own row skipped; 980 share exact coordinates) | 93.0% right; 97.3% (0–50 m), 92.8% (50–100), 88.3% (100–200), 86.8% (200–500), 72.6% (over 500). ZIP 10000 not used as a reference |
| ZIP fill | 4,091 candidates; 3,817 filled (median 84 m); 274 too far (102 highway); 11,889 of 13,309 crashes with a ZIP; by year 87.7% · 88.0% · 86.0% · 94.2% · 92.7% |
| Border ZIPs | 6 ZIPs in two boroughs; 14 crashes differ from their ZIP's borough |
| Tables | zip_year 950 rows; zip_month 10,260; borough_year 25; building_crash_counts 7,470 |
| Distance join | 9,854 street crashes; buildings with a serious crash within 100 m: 51.2% of the 5,873 completed by June 2026 (50.4% of all 7,470); within 250 m: 95.2% (94.7%); 5,705 street crashes within 250 m of a completed building (exact distance; 'near any' = 'near either type'); `near_building_250m` unknown for 2,441 crashes without coordinates |
| Join NaNs | zip_year: 469 cells without units, 72 without crashes → 0; none left |
| ZIP-table coverage | 98.9% of units completed in the window (114,249 of 115,547); 88.8% of serious harm (12,930 of 14,564) |
| Consistency | 17 of 17 checks True; no `_x`/`_y` columns |
| Export | 6 CSVs, about 4.7 MB; all identical after reload with `src/data_loader.py` |

### Research questions: Q1, Q2 (Mohamed Nazmy, 4 Nov) and Q7, Q8 (Baraa Tantawy, 5 Nov)

| Question | Key numbers (from code output) |
| --- | --- |
| Q1 housing vs danger by ZIP | 190 ZIPs; top quarter (48) got 87.7% of 57,877 New Construction units and had 41.2% of 12,930 serious harm; Spearman ρ 0.67 (0.48 among the 127 ZIPs with units; 0.64 all types; 0.53 deaths); by borough 0.25–0.66 |
| Q2 before/after completion | 925 buildings in 107 ZIPs; change per ZIP-month: small +0.07, medium +0.02, large −0.03; baseline (52 ZIPs) +0.07 |
| Q7 growth vs change | 87 ZIPs pass baselines; growth median 55% (0–327%); harm change median +7% (−78% to +183%); ρ −0.02 (crash counts −0.05; other baselines −0.06 to 0.06); quadrants 23 / 20 / 20 / 24; ZIP coverage 87.7% → 94.2% makes ZIP-table harm rise 12.0% vs 4.4% in all crashes |
| Q8 corridors near housing | 5,698 street crashes within 250 m with a street name (58%; 7 of 5,705 have none), 6,059 serious harm, 1,448 corridors; top 10 hold 9.6% (top 10% hold 48.7%); top: Atlantic Ave 71, Eastern Pkwy 67, Jerome Ave 65, Grand Concourse 60 (units within 250 m: Grand Concourse 9,415, Jerome 9,325, Atlantic 8,801, building set as 8.3); 7 of 10 also in the city-wide top 10; repeat share 11.9% (top 10) vs 7.6%; NC-only top 10 10.7%, Preservation-only 12.5% |

### Research questions: Q3–Q6, Q9–Q12 (5 Nov)

| Question | Key numbers (from code output) |
| --- | --- |
| Q3 timing (Ali Issa) | Night 22:00–05:59: 25.4% of harm in high-housing ZIPs vs 22.6% (+2.8; random ZIP sets reach it in 4.2% of 2,000 draws); weekend 29.9 vs 27.8; morning rush 9.7 vs 10.8; evening 35.4 vs 35.7 |
| Q4 repeat spots (Ali Issa) | High third 8.5% (2022) → 10.4 → 7.3 → 8.9% (2025); low 7.5 → 8.4, medium 4.0 → 6.5 (no third falls); four years 8.7% vs 6.1% low, 5.3% medium |
| Q5 deadliness (Mostafa Ayman) | Street crashes, deaths per 100: 5.54 / 7.95 / 5.60 / 5.61 (fewest → most units); most-units 5.6 vs others pooled 6.4 (intervals overlap); street 7.3 vs highway 16.6; 4 zero-unit ZIPs in the second quarter by tie-break |
| Q6 construction (Mostafa Ayman) | 72 ZIPs; 1.46 vs 1.46 per ZIP-month; 54% of ZIPs higher during construction; no cap 1.40 vs 1.36; season-adjusted 0.20 vs 0.22; month-year-adjusted 0.18 vs 0.23 (construction months 61% in 2024–2025 vs 48%) |
| Q9 housing mix (Mostafa Alaa) | 138 ZIPs; total units ρ 0.40 with harm (0.46 repeat crashes); strongest share 3+ bedrooms 0.24; rental −0.12; shares correlate with size up to 0.63 |
| Q10 danger before (Mostafa Alaa) | 1,416 project-ZIPs started 2023–2025: 0.6 / 8.1 / 8.9 / 20.9 / 61.4% (safest → most dangerous fifth); units 52.1% in the most dangerous fifth; that fifth had 44.5% of 2022 harm and 49.6% of 2014–2021 units; 508 confidential projects not placed |
| Q11 doorstep (Moustafa Maged) | 5,873 buildings: 51.2% with a crash within 100 m (95.2% within 250 m); Manhattan 62.8, Bronx 54.0, Brooklyn 49.3, Queens 30.7, Staten Island 28.6 |
| Q12 borough balance (Moustafa Maged) | Year-to-year spread (CV) units 0.28–1.07 vs harm 0.02–0.12; yearly changes ρ −0.10 (15); no borough with more units and less harm 2022 → 2025; four-year harm: Brooklyn 3,831, Queens 3,366, Manhattan 2,601, Bronx 2,584 (hypothesis half supported) |
