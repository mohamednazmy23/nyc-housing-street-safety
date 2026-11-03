"""Shared chart functions, used by both the notebook and the Dash website.

Contract (every chart function follows it):
- Signature: qN_name(data, filters) -> plotly Figure
- data: dict of the shared tables described in docs/data_dictionary.md,
  e.g. data["zip_year"], data["crashes"]
- filters: dict with the keys in DEFAULT_FILTERS; "All" means "no filter"
- A chart never reads files and never changes the tables it receives
- A chart always returns a figure, even when the filters leave no data
- Each owner edits only their own two functions
"""
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Shared style (Story doc: grey for context, one accent colour for the point).
# Colours are placeholders until Mostafa Ayman sets the final chart style.
# ---------------------------------------------------------------------------
GREY = "#B0B0B0"
ACCENT = "#D1495B"
BOROUGHS = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

# Filter values must match the website dropdowns exactly
FILTER_OPTIONS = {
    "borough": ["All"] + BOROUGHS,
    "year": ["All", 2022, 2023, 2024, 2025, 2026],
    "housing_type": ["All", "New Construction", "Preservation"],
    "severity": ["All", "Severe injury", "Fatal"],
}
DEFAULT_FILTERS = {key: "All" for key in FILTER_OPTIONS}


def apply_filters(df, filters, use=("borough", "year", "housing_type")):
    """Return the rows of df that match the chosen filters.

    Only the filters named in `use` are applied, and only when df has the
    matching column, so each chart decides which filters affect it.
    """
    columns = {"borough": "borough", "year": "year", "housing_type": "construction_type"}
    filtered = df
    for key in use:
        value = filters.get(key, "All")
        column = columns.get(key)
        if value != "All" and column in filtered.columns:
            filtered = filtered[filtered[column] == value]
    return filtered


def harm_column(filters):
    """Crash measure picked by the severity filter."""
    return {
        "All": "serious_harm",
        "Severe injury": "severe_injuries",
        "Fatal": "fatalities",
    }[filters.get("severity", "All")]


def units_column(filters):
    """Housing measure picked by the housing-type filter.

    The ZIP and borough tables split units into columns instead of having a
    construction_type column, so apply_filters can't filter them by type.
    """
    return {
        "All": "units_all",
        "New Construction": "units_new_construction",
        "Preservation": "units_preservation",
    }[filters.get("housing_type", "All")]


def apply_style(fig, title):
    """Give every chart the same look and a finding-style title."""
    fig.update_layout(
        title=title,
        template="simple_white",
        font=dict(size=13),
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig


def placeholder(name):
    """Empty figure shown until a chart is built."""
    fig = go.Figure()
    fig.add_annotation(text=f"{name}: chart not built yet", showarrow=False,
                       x=0.5, y=0.5, xref="paper", yref="paper")
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return apply_style(fig, name)


# ---------------------------------------------------------------------------
# The 12 charts. Each docstring lists: owner · chart type · tables · filters.
# Filters follow the "Page sections" table in the Story doc.
# ---------------------------------------------------------------------------

def q1_housing_vs_danger(data, filters):
    """Q1 · Mohamed Nazmy · scatter (required cross-domain chart).
    Tables: zip_year. Filters: borough, year, housing_type, severity."""
    return placeholder("Q1 Housing vs danger by ZIP")


def q2_after_opening(data, filters):
    """Q2 · Mohamed Nazmy · event-study line by building size.
    Tables: buildings, zip_month. Filters: borough. New Construction only."""
    return placeholder("Q2 Before/after a building opens")


def q3_when_crashes_happen(data, filters):
    """Q3 · Ali Issa · hour x weekday heatmap.
    Tables: crashes, zip_year. Filters: borough, year, housing_type, severity."""
    return placeholder("Q3 When crashes happen")


def q4_left_unfixed(data, filters):
    """Q4 · Ali Issa · line by housing tercile.
    Tables: crashes, zip_year. Filters: borough, housing_type, severity."""
    return placeholder("Q4 Repeat danger spots")


def q5_how_deadly(data, filters):
    """Q5 · Mostafa Ayman · bar with confidence intervals.
    Tables: crashes, zip_year. Filters: borough, year, housing_type."""
    return placeholder("Q5 How deadly crashes are")


def q6_during_construction(data, filters):
    """Q6 · Mostafa Ayman · grouped bar.
    Tables: buildings, zip_month. Filters: borough, year. New Construction only."""
    return placeholder("Q6 Danger during construction")


def q7_growth_vs_change(data, filters):
    """Q7 · Baraa Tantawy · quadrant scatter.
    Tables: zip_year. Filters: borough. New Construction only."""
    return placeholder("Q7 Housing growth vs crash change")


def q8_dangerous_corridors(data, filters):
    """Q8 · Baraa Tantawy · map + top-10 bar.
    Tables: crashes, buildings. Filters: borough, year, housing_type, severity."""
    return placeholder("Q8 Dangerous corridors")


def q9_housing_features(data, filters):
    """Q9 · Mostafa Alaa · correlation heatmap.
    Tables: buildings, zip_year. Filters: borough, year, housing_type."""
    return placeholder("Q9 Housing features vs crashes")


def q10_danger_before(data, filters):
    """Q10 · Mostafa Alaa · bar by 2022 danger quintile.
    Tables: buildings, zip_year. Filters: borough, year, housing_type."""
    return placeholder("Q10 Was the danger already there")


def q11_doorstep_danger(data, filters):
    """Q11 · Moustafa Maged · stacked bar by borough.
    Tables: buildings, building_crash_counts. Filters: borough, year, housing_type, severity."""
    return placeholder("Q11 Doorstep danger")


def q12_borough_balance(data, filters):
    """Q12 · Moustafa Maged · animated bubble.
    Tables: borough_year. Filters: severity (always shows all boroughs and years)."""
    return placeholder("Q12 Borough balance over time")


# The website's Generate Report button loops over this registry
CHARTS = {
    "q1": q1_housing_vs_danger,
    "q2": q2_after_opening,
    "q3": q3_when_crashes_happen,
    "q4": q4_left_unfixed,
    "q5": q5_how_deadly,
    "q6": q6_during_construction,
    "q7": q7_growth_vs_change,
    "q8": q8_dangerous_corridors,
    "q9": q9_housing_features,
    "q10": q10_danger_before,
    "q11": q11_doorstep_danger,
    "q12": q12_borough_balance,
}
