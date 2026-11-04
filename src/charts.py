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
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    # Severity switches the crash measure, not the rows (decision D30)
    "severity": ["All", "Severe injuries", "Deaths"],
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
    """Crash measure picked by the severity filter (decision D30).

    The filter changes WHAT is counted (people harmed), not which crashes
    are kept. Charts that count crashes should sum this column instead.
    """
    return {
        "All": "serious_harm",
        "Severe injuries": "severe_injuries",
        "Deaths": "fatalities",
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

HARM_LABELS = {"serious_harm": "serious harm (severe injuries + deaths)",
               "severe_injuries": "severe injuries", "fatalities": "deaths"}
UNIT_LABELS = {"units_all": "affordable units completed",
               "units_new_construction": "New Construction affordable units completed",
               "units_preservation": "Preservation affordable units completed"}


Q1_DEFAULT_TYPE = "New Construction"     # Q1 is defined on New Construction


def q1_housing_type(filters):
    """Q1 follows the housing-type filter, but "All" (the website default) means New Construction."""
    chosen = filters.get("housing_type", "All")
    return Q1_DEFAULT_TYPE if chosen == "All" else chosen


def q1_zip_totals(data, filters):
    """Q1 data: one row per ZIP with units completed and harm, summed over the chosen years.

    Every ZIP in zip_year is kept, so a ZIP with crashes but no new housing counts as 0 units.
    """
    units = units_column({"housing_type": q1_housing_type(filters)})
    harm = harm_column(filters)
    rows = apply_filters(data["zip_year"], filters, use=("borough", "year"))
    per_zip = rows.groupby(["zip", "borough"], as_index=False)[[units, harm, "n_crashes"]].sum()
    return per_zip, units, harm


def spearman(x, y):
    """Spearman correlation as the Pearson correlation of ranks (no scipy needed on the website)."""
    return x.rank().corr(y.rank())


def q1_top_quarter(per_zip, units, harm):
    """Share of all units and of all harm in the quarter of ZIPs with the most units."""
    n_top = -(-len(per_zip) // 4)                       # a quarter of the ZIPs, rounded up
    top = per_zip.nlargest(n_top, units)
    return {"zips": n_top, "units_share": top[units].sum() / max(per_zip[units].sum(), 1),
            "harm_share": top[harm].sum() / max(per_zip[harm].sum(), 1)}


def q1_housing_vs_danger(data, filters):
    """Q1 · Mohamed Nazmy · scatter (required cross-domain chart).
    Tables: zip_year. Filters: borough, year, housing_type, severity."""
    per_zip, units, harm = q1_zip_totals(data, filters)
    rho = spearman(per_zip[units], per_zip[harm]) if len(per_zip) >= 3 else float("nan")
    if pd.isna(rho):
        fig = placeholder("Q1 Housing vs danger by ZIP")
        fig.layout.annotations[0].text = "Not enough ZIPs with data for these filters"
        return fig

    fig = go.Figure()
    for borough in BOROUGHS:
        part = per_zip[per_zip["borough"] == borough]
        fig.add_trace(go.Scatter(
            x=part[units], y=part[harm], mode="markers", name=borough,
            marker=dict(size=8, opacity=0.75, line=dict(width=0.5, color="white")),
            customdata=part[["zip", "n_crashes"]],
            hovertemplate="ZIP %{customdata[0]}<br>Units: %{x:,}<br>Harm: %{y:,}"
                          "<br>Serious crashes: %{customdata[1]:,}<extra>" + borough + "</extra>"))

    # Straight-line trend (least squares), only as a visual guide; the Spearman rho is the measure
    slope, intercept = np.polyfit(per_zip[units].astype(float), per_zip[harm].astype(float), 1)
    x_line = np.array([0, per_zip[units].max()])
    fig.add_trace(go.Scatter(x=x_line, y=intercept + slope * x_line, mode="lines", name="Trend",
                             line=dict(color="black", dash="dash", width=1.5), hoverinfo="skip"))

    top = q1_top_quarter(per_zip, units, harm)
    kind = "preserved" if q1_housing_type(filters) == "Preservation" else "new"
    title = (f"The quarter of ZIPs that got the most {kind} affordable units ({top['units_share']:.0%} of them) "
             f"also had {top['harm_share']:.0%} of the {HARM_LABELS[harm].split(' (')[0]}")
    type_note = (" · Housing type: New Construction (Q1's default)"
                 if filters.get("housing_type", "All") == "All" else "")
    fig.add_annotation(text=f"{len(per_zip)} ZIPs · Spearman ρ = {rho:.2f} · correlation is not causation{type_note}",
                       xref="paper", yref="paper", x=1, y=1.02, showarrow=False, xanchor="right",
                       font=dict(size=11, color="grey"))
    fig.update_xaxes(title=UNIT_LABELS[units], rangemode="tozero")
    fig.update_yaxes(title=HARM_LABELS[harm], rangemode="tozero")
    fig.update_layout(legend_title_text="Borough")
    return apply_style(fig, title)


# Q2 settings: completions early and late enough that 12 months before and after stay inside the window
Q2_FIRST, Q2_LAST = "2023-01-01", "2025-06-30"
Q2_BINS = [(-12, -10), (-9, -7), (-6, -4), (-3, -1), (1, 3), (4, 6), (7, 9), (10, 12)]
SIZE_GROUPS = ["Small (<50)", "Medium (50-199)", "Large (200+)"]


def q2_event_months(data, filters):
    """Q2 data: serious harm in each building's ZIP for the 12 months before and after completion,
    plus the same calendar months in ZIPs where no building was completed in the window (baseline).

    One row per building x month relative to completion (-12..+12; 0 = completion month).
    """
    buildings = data["buildings"]
    events = buildings[(buildings["construction_type"] == "New Construction") & buildings["zip"].notna()
                       & buildings["completion_date"].between(Q2_FIRST, Q2_LAST)]
    events = apply_filters(events, filters, use=("borough",)).drop_duplicates("building_id")
    events = events.assign(completion_month=events["completion_date"].dt.to_period("M"))

    zip_month = apply_filters(data["zip_month"], filters, use=("borough",))
    harm = zip_month.assign(period=zip_month["month"].dt.to_period("M"))[["zip", "period", "serious_harm"]]

    # Baseline ZIPs: no affordable building (any type) completed anywhere in the window
    units_per_zip = zip_month.groupby("zip")["units_all"].sum()
    no_completion = units_per_zip.index[units_per_zip == 0]
    baseline_by_month = (harm[harm["zip"].isin(no_completion)]
                         .groupby("period")["serious_harm"].mean().rename("baseline_harm"))

    offsets = pd.DataFrame({"rel_month": range(-12, 13)})
    rows = events[["building_id", "zip", "size_group", "total_units", "completion_month"]].merge(offsets, how="cross")
    rows["period"] = rows["completion_month"] + rows["rel_month"]
    rows = (rows.merge(harm, on=["zip", "period"], how="left")
                .merge(baseline_by_month, left_on="period", right_index=True, how="left"))
    return rows, len(no_completion)


def q2_bin_means(rows):
    """Average monthly serious harm per ZIP in each 3-month bin, by size group and for the baseline."""
    rows = rows[rows["rel_month"] != 0].copy()
    rows["bin_mid"] = 0.0
    for low, high in Q2_BINS:
        rows.loc[rows["rel_month"].between(low, high), "bin_mid"] = (low + high) / 2
    groups = (rows.groupby(["size_group", "bin_mid"], observed=True)
                  .agg(harm=("serious_harm", "mean"), buildings=("building_id", "nunique")).reset_index())
    baseline = rows.groupby("bin_mid").agg(harm=("baseline_harm", "mean")).reset_index()
    return groups, baseline


def q2_before_after(rows):
    """Mean monthly harm in the 12 months before vs after completion, by size group and baseline."""
    side = np.where(rows["rel_month"] < 0, "before", np.where(rows["rel_month"] > 0, "after", None))
    rows = rows.assign(side=side, size_group=rows["size_group"].astype(str)).dropna(subset=["side"])
    table = rows.pivot_table(index="size_group", columns="side", values="serious_harm", aggfunc="mean")
    table = table.reindex([group for group in SIZE_GROUPS if group in table.index])
    base = rows.groupby("side")["baseline_harm"].mean()
    table.loc["Baseline (no completion)"] = base
    table["buildings"] = rows.groupby("size_group")["building_id"].nunique()
    table["change"] = table["after"] - table["before"]
    table["change_vs_baseline"] = table["change"] - (base["after"] - base["before"])
    return table[["buildings", "before", "after", "change", "change_vs_baseline"]]


def q2_after_opening(data, filters):
    """Q2 · Mohamed Nazmy · event-study line by building size.
    Tables: buildings, zip_month. Filters: borough. New Construction only."""
    rows, _ = q2_event_months(data, filters)
    if rows.empty:
        fig = placeholder("Q2 Before/after a building opens")
        fig.layout.annotations[0].text = "No New Construction completions for these filters"
        return fig
    groups, baseline = q2_bin_means(rows)
    table = q2_before_after(rows)

    fig = go.Figure()
    colours = {"Small (<50)": "#C7C7C7", "Medium (50-199)": "#8C8C8C", "Large (200+)": ACCENT}
    for group in SIZE_GROUPS:
        part = groups[groups["size_group"] == group]
        if part.empty:
            continue
        fig.add_trace(go.Scatter(
            x=part["bin_mid"], y=part["harm"], mode="lines+markers", name=f"{group}",
            line=dict(color=colours[group], width=3 if group.startswith("Large") else 2),
            customdata=part["buildings"],
            hovertemplate="%{y:.2f} per ZIP-month<br>%{customdata} buildings<extra>" + group + "</extra>"))
    fig.add_trace(go.Scatter(x=baseline["bin_mid"], y=baseline["harm"], mode="lines", name="ZIPs with no completion",
                             line=dict(color="black", dash="dash", width=1.5),
                             hovertemplate="%{y:.2f} per ZIP-month<extra>Baseline</extra>"))
    fig.add_vline(x=0, line=dict(color="grey", dash="dot"))
    fig.add_annotation(x=0, y=1.02, yref="paper", text="building completed", showarrow=False,
                       font=dict(size=11, color="grey"))

    large = table.loc["Large (200+)"] if "Large (200+)" in table.index else None
    if large is not None and not pd.isna(large["change"]):
        base_change = table.loc["Baseline (no completion)", "change"]
        verb = ("barely changes" if abs(large["change"]) < 0.1
                else "rises" if large["change"] > 0 else "falls")
        title = (f"After a large affordable building opens, serious harm in its ZIP {verb} "
                 f"({large['change']:+.2f} per month; ZIPs with no completion: {base_change:+.2f})")
    else:
        title = "Serious harm in a ZIP before and after an affordable building opens"
    fig.update_xaxes(title="months from building completion (3-month bins)",
                     tickvals=[-11, -8, -5, -2, 2, 5, 8, 11],
                     ticktext=["-12 to -10", "-9 to -7", "-6 to -4", "-3 to -1",
                               "+1 to +3", "+4 to +6", "+7 to +9", "+10 to +12"])
    fig.update_yaxes(title="average serious harm per ZIP per month", rangemode="tozero")
    fig.update_layout(legend_title_text="Building size (total units)")
    fig = apply_style(fig, title)
    # Fixed window: the year and housing-type filters don't apply, so say so on the chart
    fig.add_annotation(text="Fixed window: New Construction buildings completed Jan 2023 – Jun 2025, "
                            "12 months either side. Year and housing-type filters do not apply.",
                       xref="paper", yref="paper", x=0, y=-0.22, xanchor="left", showarrow=False,
                       font=dict(size=11, color="grey"))
    fig.update_layout(margin=dict(b=100))
    return fig


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


# Q7 settings: change from the end of 2022 to the end of 2025 (full years only; 2026 is half a year)
Q7_START_YEAR, Q7_END_YEAR = 2022, 2025
Q7_MIN_UNITS, Q7_MIN_CRASHES = 50, 5     # minimum baselines, so a % change never rests on a handful


def q7_zip_changes(data, filters, min_units=Q7_MIN_UNITS, min_crashes=Q7_MIN_CRASHES):
    """Q7 data: one row per ZIP with
    - housing growth: % increase in New Construction affordable units completed since 2014,
      counted at the end of 2022 and at the end of 2025 (buildings table, all years);
    - harm change: % change in serious harm from 2022 to 2025 (zip_year).
    Only ZIPs with at least min_units units by end 2022 and min_crashes serious crashes in 2022."""
    buildings = data["buildings"]
    new = buildings[(buildings["construction_type"] == "New Construction") & buildings["zip"].notna()
                    & buildings["completion_date"].notna()]
    cumulative = {year: new[new["completion_date"].dt.year <= year].groupby("zip")["all_counted_units"].sum()
                  for year in (Q7_START_YEAR, Q7_END_YEAR)}

    zip_year = apply_filters(data["zip_year"], filters, use=("borough",))
    two_years = zip_year[zip_year["year"].isin([Q7_START_YEAR, Q7_END_YEAR])]
    wide = two_years.pivot_table(index=["zip", "borough"], columns="year",
                                 values=["serious_harm", "n_crashes"], aggfunc="sum")
    table = pd.DataFrame({"harm_start": wide[("serious_harm", Q7_START_YEAR)],
                          "harm_end": wide[("serious_harm", Q7_END_YEAR)],
                          "crashes_start": wide[("n_crashes", Q7_START_YEAR)],
                          "crashes_end": wide[("n_crashes", Q7_END_YEAR)]}).reset_index()
    for label, year in [("units_start", Q7_START_YEAR), ("units_end", Q7_END_YEAR)]:
        table[label] = table["zip"].map(cumulative[year]).astype(float).fillna(0)

    kept = table[(table["units_start"] >= min_units) & (table["crashes_start"] >= min_crashes)].copy()
    kept["housing_growth_pct"] = (kept["units_end"] / kept["units_start"] - 1) * 100
    kept["harm_change_pct"] = (kept["harm_end"] / kept["harm_start"] - 1) * 100
    return kept, len(table)


def q7_quadrants(table):
    """Number of ZIPs in each quadrant around the two medians."""
    fast = table["housing_growth_pct"] > table["housing_growth_pct"].median()
    worse = table["harm_change_pct"] > table["harm_change_pct"].median()
    return {"fast_worse": int((fast & worse).sum()), "fast_better": int((fast & ~worse).sum()),
            "slow_worse": int((~fast & worse).sum()), "slow_better": int((~fast & ~worse).sum())}


def q7_growth_vs_change(data, filters):
    """Q7 · Baraa Tantawy · quadrant scatter.
    Tables: buildings, zip_year. Filters: borough. New Construction only, fixed years 2022 -> 2025."""
    table, _ = q7_zip_changes(data, filters)
    if len(table) < 5:
        fig = placeholder("Q7 Housing growth vs crash change")
        fig.layout.annotations[0].text = "Fewer than 5 ZIPs pass the minimum baselines for this borough"
        return fig
    rho = spearman(table["housing_growth_pct"], table["harm_change_pct"])
    mid_x, mid_y = table["housing_growth_pct"].median(), table["harm_change_pct"].median()

    fig = go.Figure()
    for borough in BOROUGHS:
        part = table[table["borough"] == borough]
        fig.add_trace(go.Scatter(
            x=part["housing_growth_pct"], y=part["harm_change_pct"], mode="markers", name=borough,
            marker=dict(size=9, opacity=0.8, line=dict(width=0.5, color="white")),
            customdata=part[["zip", "units_start", "units_end", "harm_start", "harm_end"]],
            hovertemplate="ZIP %{customdata[0]}<br>New Construction units: %{customdata[1]:,.0f} → "
                          "%{customdata[2]:,.0f} (%{x:+.0f}%)<br>Serious harm: %{customdata[3]} → "
                          "%{customdata[4]} (%{y:+.0f}%)<extra>" + borough + "</extra>"))
    # Median lines split the ZIPs into four equal-sized halves on each axis
    fig.add_vline(x=mid_x, line=dict(color="grey", dash="dash"))
    fig.add_hline(y=mid_y, line=dict(color="grey", dash="dash"))
    quadrants = q7_quadrants(table)
    for text, x, y, xanchor, yanchor in [
            (f"faster growth, harm up more: {quadrants['fast_worse']} ZIPs", 1, 1, "right", "top"),
            (f"faster growth, harm up less: {quadrants['fast_better']} ZIPs", 1, 0, "right", "bottom"),
            (f"slower growth, harm up more: {quadrants['slow_worse']} ZIPs", 0, 1, "left", "top"),
            (f"slower growth, harm up less: {quadrants['slow_better']} ZIPs", 0, 0, "left", "bottom")]:
        fig.add_annotation(text=text, xref="paper", yref="paper", x=x, y=y, xanchor=xanchor, yanchor=yanchor,
                           showarrow=False, font=dict(size=11, color="grey"))

    if abs(rho) < 0.2:
        title = (f"ZIPs that added new affordable homes fastest saw serious harm change no differently "
                 f"from the rest (ρ = {rho:.2f})")
    else:
        title = (f"ZIPs that added new affordable homes fastest saw serious harm "
                 f"{'rise' if rho > 0 else 'fall'} more (ρ = {rho:.2f})")
    fig.update_xaxes(title=f"growth in New Construction affordable units, end {Q7_START_YEAR} → end {Q7_END_YEAR} (%)",
                     rangemode="tozero")
    fig.update_yaxes(title=f"change in serious harm, {Q7_START_YEAR} → {Q7_END_YEAR} (%)", zeroline=True)
    fig.update_layout(legend_title_text="Borough")
    fig = apply_style(fig, title)
    fig.add_annotation(text=(f"{len(table)} ZIPs with ≥{Q7_MIN_UNITS} New Construction units by end {Q7_START_YEAR} and "
                             f"≥{Q7_MIN_CRASHES} serious crashes in {Q7_START_YEAR} · dashed lines = medians · "
                             "correlation is not causation · fixed years: year, housing-type and severity filters do not apply"),
                       xref="paper", yref="paper", x=0, y=-0.2, xanchor="left", showarrow=False,
                       font=dict(size=11, color="grey"))
    fig.update_layout(margin=dict(b=100))
    return fig


# Q8 settings
Q8_RADIUS_M = 250
Q8_TOP = 10
Q8_WINDOW_END = "2026-06-30"
NEAR_COLUMN = {"All": "near_building_250m", "New Construction": "near_new_construction_250m",
               "Preservation": "near_preservation_250m"}   # precomputed in notebook 8.3


def haversine_m(lat1, lon1, lat2, lon2):
    """Distance in metres along the Earth's surface; numpy arrays broadcast (e.g. crashes x buildings)."""
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6_371_000 * np.arcsin(np.sqrt(a))


def q8_buildings(data, filters):
    """The affordable buildings the 250 m flags were computed from: located, completed by 30 Jun 2026,
    one row per building (its latest project), of the chosen housing type and borough."""
    buildings = data["buildings"]
    buildings = buildings[buildings["has_location"] & (buildings["completion_date"] <= Q8_WINDOW_END)]
    buildings = buildings.sort_values("project_start").drop_duplicates("building_id", keep="last")
    return apply_filters(buildings, filters, use=("borough", "housing_type"))


def q8_corridors(data, filters):
    """Q8 data: street crashes (no highways, D15) within 250 m of an affordable building of the chosen type,
    grouped into corridors (street + borough, because e.g. Broadway runs through several boroughs)."""
    crashes = apply_filters(data["crashes"], filters, use=("borough", "year"))
    near = crashes[NEAR_COLUMN[filters.get("housing_type", "All")]].fillna(False).astype(bool)
    near = crashes[near & ~crashes["is_highway"] & crashes["street"].notna()].copy()
    near["corridor"] = near["street"].str.title() + " (" + near["borough"] + ")"
    harm = harm_column(filters)
    corridors = (near.groupby("corridor")
                     .agg(crashes=("crash_id", "size"), harm=(harm, "sum"), deaths=("fatalities", "sum"),
                          repeat_share=("repeat_location", "mean"))
                     .sort_values(["harm", "crashes"], ascending=False))
    return near, corridors, harm


def q8_units_near(corridor_crashes, buildings):
    """Buildings, and their affordable units, within 250 m of any crash on one corridor."""
    if corridor_crashes.empty or buildings.empty:
        return 0, 0
    distance = haversine_m(corridor_crashes["lat"].to_numpy()[:, None], corridor_crashes["lon"].to_numpy()[:, None],
                           buildings["lat"].to_numpy()[None, :], buildings["lon"].to_numpy()[None, :])
    close = (distance <= Q8_RADIUS_M).any(axis=0)
    return int(close.sum()), int(buildings.loc[close, "all_counted_units"].fillna(0).sum())


def q8_top_corridors(data, filters):
    """Top corridors with the buildings and units near each, and the share of harm they hold."""
    near, corridors, harm = q8_corridors(data, filters)
    buildings = q8_buildings(data, filters)
    top = corridors.head(Q8_TOP).copy()
    nearby = [q8_units_near(near[near["corridor"] == name], buildings) for name in top.index]
    top["buildings_near"] = [count for count, _ in nearby]
    top["units_near"] = [units for _, units in nearby]
    share = top["harm"].sum() / max(corridors["harm"].sum(), 1)
    return near, corridors, top, buildings, harm, share


def q8_dangerous_corridors(data, filters):
    """Q8 · Baraa Tantawy · map + top-10 bar.
    Tables: crashes, buildings. Filters: borough, year, housing_type, severity."""
    near, corridors, top, buildings, harm, share = q8_top_corridors(data, filters)
    if corridors.empty or top["harm"].sum() == 0:
        fig = placeholder("Q8 Dangerous corridors")
        fig.layout.annotations[0].text = "No serious crashes near affordable housing for these filters"
        return fig
    harm_label = HARM_LABELS[harm].split(" (")[0]

    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.2,
                        specs=[[{"type": "map"}, {"type": "xy"}]],
                        subplot_titles=("Street crashes within 250 m of affordable housing",
                                        f"Top {len(top)} corridors by {harm_label}"))
    # Map: buildings (blue, sized by total units), other crashes (grey), top corridors (accent colour)
    fig.add_trace(go.Scattermap(
        lat=buildings["lat"], lon=buildings["lon"], mode="markers", name="Affordable building",
        marker=dict(size=np.clip(np.sqrt(buildings["total_units"].astype(float)), 3, 16), color="#4C6A92", opacity=0.3),
        text=buildings["number"].fillna("") + " " + buildings["street"].fillna("") + " · "
             + buildings["total_units"].astype(str) + " units",
        hovertemplate="%{text}<extra>Affordable building</extra>"), row=1, col=1)
    on_top = near["corridor"].isin(top.index)
    for part, name, colour, size in [(near[~on_top], "Other street crash", GREY, 5),
                                     (near[on_top], f"Crash on a top-{len(top)} corridor", ACCENT, 7)]:
        fig.add_trace(go.Scattermap(
            lat=part["lat"], lon=part["lon"], mode="markers", name=name,
            marker=dict(size=size, color=colour, opacity=0.8), text=part["corridor"],
            hovertemplate="%{text}<extra>" + name + "</extra>"), row=1, col=1)

    bars = top.iloc[::-1]          # largest at the top of the bar chart
    fig.add_trace(go.Bar(
        x=bars["harm"], y=bars.index, orientation="h", name=harm_label, showlegend=False,
        marker_color=ACCENT, text=bars["harm"], textposition="outside",
        customdata=np.stack([bars["crashes"], bars["deaths"], bars["repeat_share"].astype(float) * 100,
                             bars["buildings_near"], bars["units_near"]], axis=1),
        hovertemplate="%{y}<br>" + harm_label + ": %{x}<br>Serious crashes: %{customdata[0]:.0f} · deaths: "
                      "%{customdata[1]:.0f}<br>At repeat-danger spots: %{customdata[2]:.0f}%<br>Affordable buildings "
                      "within 250 m: %{customdata[3]:.0f} (%{customdata[4]:,.0f} units)<extra></extra>"), row=1, col=2)

    title = (f"The {len(top)} worst corridors near affordable housing hold only {share:.0%} of the {harm_label} "
             f"there; the rest is spread over {len(corridors) - len(top):,} other streets")
    fig = apply_style(fig, title)
    fig.update_layout(
        map=dict(style="carto-positron", zoom=9.6 if filters.get("borough", "All") == "All" else 10.8,
                 center=dict(lat=float(near["lat"].mean()), lon=float(near["lon"].mean()))),
        height=620, legend=dict(orientation="h", y=-0.08, x=0), margin=dict(l=40, r=20, t=90, b=90))
    fig.update_xaxes(title=harm_label, rangemode="tozero", row=1, col=2)
    fig.add_annotation(text=("Street crashes only (no highways) · corridor = street + borough · buildings completed by "
                             "Jun 2026 · hover a bar for repeat-danger share and nearby units"),
                       xref="paper", yref="paper", x=0, y=-0.16, xanchor="left", showarrow=False,
                       font=dict(size=11, color="grey"))
    return fig


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
