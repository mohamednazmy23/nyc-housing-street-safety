# Data Dictionary (proposal, to confirm with Moustafa Maged)

Shared tables in `data/processed/`. Chart functions receive them as `data["<table>"]`.

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
| `crashes` | one cleaned SIRTA crash | crash_id, crash_datetime, year, hour, weekday, zip, borough, lat, lon, street, severe_injuries, fatalities, serious_harm, is_highway, repeat_location | Q3, Q4, Q5, Q8 |
| `zip_year` | ZIP x year | zip, borough, year, units_all, units_new_construction, units_preservation, n_crashes, severe_injuries, fatalities, serious_harm, n_repeat_crashes | Q1, Q3, Q4, Q5, Q7, Q9, Q10 |
| `zip_month` | ZIP x month | same as zip_year, plus month | Q2, Q6 |
| `borough_year` | borough x year | borough, year, units_all, units_new_construction, units_preservation, severe_injuries, fatalities, serious_harm | Q12 |
| `building_crash_counts` | one building | building_id, crashes_100m, crashes_250m | Q11 |

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
| is_confidential, has_location, is_completed, completed_before_start, in_several_projects | bool | Flags; for Q8/Q11 use one row per building_id |

## Definitions
- serious_harm = severe_injuries + fatalities
- units_all = units_new_construction + units_preservation
- Severity filter (switches the measure, not the rows; decision D30): "All" → serious_harm, "Severe injuries" → severe_injuries, "Deaths" → fatalities
- Housing-type filter: "All" → units_all, "New Construction" → units_new_construction, "Preservation" → units_preservation
