# Data Dictionary

Shared tables in `data/processed/`, exported by the notebook (section 9.4). Chart functions receive them as `data["<table>"]`.
Always load them with `from data_loader import load_tables` (`src/data_loader.py`), which sets the column types below.

## Formats (all tables)
- `zip`: 5-character text, e.g. "10451" (never a number)
- `borough`: Bronx, Brooklyn, Manhattan, Queens, Staten Island
- `construction_type`: New Construction, Preservation
- Dates: pandas datetime. `year`: integer. `month`: first day of the month (datetime)
- Analysis window: 2022-01-01 to 2026-06-30

## Tables

| Table | One row = | Columns | Used by |
|---|---|---|---|
| `buildings` | one cleaned affordable building record (a building in several projects has one row per project) | see "`buildings` columns" below | Q2, Q6, Q8, Q9, Q10, Q11 |
| `crashes` | one cleaned SIRTA crash | see "`crashes` columns" below | Q3, Q4, Q5, Q8 |
| `zip_year` | ZIP x year (190 ZIPs x 2022–2026 = 950 rows; every combination, 0 = nothing happened) | zip, borough, year, then the count columns below | Q1, Q3, Q4, Q5, Q7, Q9, Q10 |
| `zip_month` | ZIP x month (190 x 54 = 10,260 rows) | zip, borough, month, year, then the count columns below | Q2, Q6 |
| `borough_year` | borough x year (25 rows); includes records without a ZIP | borough, year, then the count columns below | Q12 |
| `building_crash_counts` | one located building (7,470 rows) | building_id, crashes_100m, crashes_250m (non-highway serious crashes within that distance, whole window) | Q11 |

**Count columns** (whole numbers, in `zip_year`, `zip_month`, `borough_year`): units_new_construction, units_preservation, units_all (affordable units completed inside the window), n_buildings_completed, n_crashes, severe_injuries, fatalities, serious_harm, n_repeat_crashes (lookback above 0), n_crashes_with_lookback (denominator for Q4's share), n_highway_crashes.

**ZIP tables cover** 98.9% of the units completed in the window and 88.8% of the serious harm; the rest has no ZIP and is only in `borough_year`. A ZIP in two boroughs takes the borough most of its records are in.

## `buildings` columns (set by housing cleaning, notebook section 6)

| Column | Type | Meaning |
|---|---|---|
| building_id, project_id | Int64 | IDs; building_id is missing for confidential rows |
| project_name, number, street | text | Address fields; missing for confidential rows |
| borough | text | Always filled |
| zip | text (5 characters) | Missing for 1,958 rows (no location) |
| lat, lon | float | Missing for the same 1,958 rows |
| construction_type | text | New Construction or Preservation |
| project_start, completion_date | datetime | completion_date missing = not completed yet |
| completion_year | Int64 | Year of completion_date |
| all_counted_units | Int64 | Affordable units; missing in 29 rows (unknown, not 0) |
| total_units | Int64 | Affordable + market-rate; never sum across rows of the same building |
| units_extremely_low, units_very_low, units_low, units_moderate, units_middle, units_other_income | Int64 | Units by income tier (0 = none) |
| units_studio, units_1br, units_2br, units_3br, units_4br, units_5br, units_6br_plus, units_unknown_br | Int64 | Units by bedroom size (0 = none) |
| units_rental, units_homeownership | Int64 | Units by tenure (0 = none) |
| size_group | category | Small (<50), Medium (50-199), Large (200+) by total_units |
| completed_in_window | bool | Completed 1 Jan 2022 – 30 Jun 2026. **Use this, not `is_completed`, to count completions** (16 buildings were completed in Jul–Aug 2026) |
| is_confidential, has_location, is_completed, completed_before_start, in_several_projects | bool | Flags. For Q8, Q11 and completion events (Q2, Q6) use one row per building_id |

## `crashes` columns (set by SIRTA cleaning, notebook section 7)

| Column | Type | Meaning |
|---|---|---|
| crash_id | Int64 | Collision ID; unique (13,309 crashes) |
| crash_datetime | datetime | Date and time of the crash (time 00:00 when unknown) |
| year | integer | Year of the crash |
| month | datetime | First day of the crash month |
| hour | Int64 | Hour 0–23; **missing when the time is unknown** (227 crashes) |
| weekday | text | Monday … Sunday |
| time_unknown | bool | Crash logged at 00:00 (time not recorded) |
| borough | text | Always filled (55 filled from the precinct) |
| borough_filled | bool | Borough taken from the precinct |
| zip | text (5 characters) | Filled in section 8 where possible; missing for 1,420 crashes (no coordinates, or no point within 500 m); 10000 = SIRTA's own code, Central Park area |
| lat, lon | float | Missing for 2,441 crashes (borough level only) |
| has_location | bool | Has coordinates |
| street | text | Clean street name (one spelling per street); missing for 15 crashes |
| street_from_address | bool | Street taken from Address |
| is_highway | bool | Highway marker filled or listed limited-access road (1,443 crashes). Leave out of Q8, Q11; Q5 with and without |
| severe_injuries, fatalities, serious_harm | Int64 | People harmed in the crash; serious_harm = severe_injuries + fatalities |
| lookback_severe | Int64 | Similar severe crashes at this location in the 3 years before; missing for 1,393 crashes (2023–2024) |
| repeat_location | boolean | lookback_severe > 0; missing where lookback_severe is missing |
| merged_duplicate | bool | The one crash kept from a repeated Collision ID (7.5) |
| zip_filled | bool | ZIP filled in section 8 from the nearest crash or building with a ZIP (3,817 crashes) |
| zip_match_m | float | Distance in metres to that nearest point (only for filled ZIPs; at most 500) |
| dist_nearest_building_m | float | Distance in metres to the nearest affordable building completed by 30 Jun 2026 |
| near_building_250m | bool | dist_nearest_building_m is 250 m or less (Q8) |

## Definitions
- serious_harm = severe_injuries + fatalities
- units_all = units_new_construction + units_preservation
- Severity filter (switches the measure, not the rows; decision D30): "All" → serious_harm, "Severe injuries" → severe_injuries, "Deaths" → fatalities
- Housing-type filter: "All" → units_all, "New Construction" → units_new_construction, "Preservation" → units_preservation
