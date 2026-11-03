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
| `buildings` | one cleaned affordable building | building_id, project_id, zip, borough, lat, lon, construction_type, project_start, completion_date, all_counted_units, total_units, income-tier, bedroom and tenure unit columns | Q2, Q6, Q8, Q9, Q10, Q11 |
| `crashes` | one cleaned SIRTA crash | crash_id, crash_datetime, year, hour, weekday, zip, borough, lat, lon, street, severe_injuries, fatalities, serious_harm, is_highway, repeat_location | Q3, Q4, Q5, Q8 |
| `zip_year` | ZIP x year | zip, borough, year, units_all, units_new_construction, units_preservation, n_crashes, severe_injuries, fatalities, serious_harm, n_repeat_crashes | Q1, Q3, Q4, Q5, Q7, Q9, Q10 |
| `zip_month` | ZIP x month | same as zip_year, plus month | Q2, Q6 |
| `borough_year` | borough x year | borough, year, units_all, units_new_construction, units_preservation, severe_injuries, fatalities, serious_harm | Q12 |
| `building_crash_counts` | one building | building_id, crashes_100m, crashes_250m | Q11 |

## Definitions
- serious_harm = severe_injuries + fatalities
- units_all = units_new_construction + units_preservation
- Severity filter: "All" → serious_harm, "Severe injury" → severe_injuries, "Fatal" → fatalities
- Housing-type filter: "All" → units_all, "New Construction" → units_new_construction, "Preservation" → units_preservation
