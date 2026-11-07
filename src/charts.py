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
import textwrap

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


# Characters per line before a title or a note wraps. Plotly can't re-wrap text when a chart gets narrower, so
# these are a compromise: no cut-off on laptops and tablets; on a narrow phone a long title can still be cut,
# which is why every chart on the website also has its takeaway as normal (wrapping) text above it
TITLE_WIDTH, NOTE_WIDTH = 70, 110


def wrap(text, width):
    """Break long chart text into lines (Plotly does not wrap titles or annotations by itself)."""
    return "<br>".join(textwrap.wrap(text, width)) or text


def apply_style(fig, title):
    """Give every chart the same look and a finding-style title (wrapped so it is never cut off)."""
    title_lines = wrap(title, TITLE_WIDTH).count("<br>") + 1
    fig.update_layout(
        title=wrap(title, TITLE_WIDTH),
        template="simple_white",
        font=dict(size=13),
        margin=dict(l=40, r=20, t=40 + 24 * title_lines, b=40),
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
    return note_below(fig, "Fixed window: New Construction buildings completed Jan 2023 – Jun 2025, "
                           "12 months either side. Year and housing-type filters do not apply.", y=-0.22)


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WINDOW_END = "2026-06-30"


def note_below(fig, text, y=-0.2):
    """Grey note under a chart (filters that don't apply, definitions, 'correlation is not causation'),
    wrapped into lines and anchored at its top, with room for it in the bottom margin."""
    lines = wrap(text, NOTE_WIDTH)
    fig.add_annotation(text=lines, xref="paper", yref="paper", x=0, y=y, xanchor="left", yanchor="top",
                       align="left", showarrow=False, font=dict(size=11, color="grey"))
    needed = 90 + 16 * (lines.count("<br>") + 1)
    fig.update_layout(margin=dict(b=max(fig.layout.margin.b or 0, needed)))   # never shrink a larger margin
    return fig


def no_data(name, message):
    """The empty figure a chart returns when the filters leave nothing to show (contract rule)."""
    fig = placeholder(name)
    fig.layout.annotations[0].text = message
    return fig


def equal_groups(values, labels):
    """Split a Series into len(labels) equal-sized, ordered groups by value. Assigned by rank position
    (ties broken by index order), so the result never depends on how a pandas version places qcut's edges."""
    position = values.rank(method="first").astype(int).to_numpy() - 1          # 0 .. n-1
    codes = position * len(labels) // len(values)
    return pd.Series(pd.Categorical.from_codes(codes, categories=labels, ordered=True), index=values.index)


def zip_housing_groups(data, filters, n_groups, labels, use=("borough", "year")):
    """Split ZIPs into equal-sized groups by affordable units completed (the housing-type filter picks
    the units column). Many ZIPs have 0 units, so ties are broken by ZIP order to keep the groups equal."""
    units = units_column(filters)
    per_zip = apply_filters(data["zip_year"], filters, use=use).groupby("zip")[units].sum()
    if len(per_zip) < n_groups:
        return pd.Series(dtype="category"), per_zip
    return equal_groups(per_zip, labels[:n_groups]), per_zip


def q3_hour_shares(data, filters):
    """Q3 data: for the top quarter of ZIPs by affordable units ("high-housing") and for all other ZIPs,
    the share of each group's serious harm that falls in each weekday x hour cell (crashes with a known hour)."""
    groups, _ = zip_housing_groups(data, filters, 4, ["Q1", "Q2", "Q3", "Q4"])
    crashes = apply_filters(data["crashes"], filters, use=("borough", "year"))
    crashes = crashes[crashes["hour"].notna() & crashes["zip"].isin(groups.index)]
    harm = harm_column(filters)
    crashes = crashes.assign(high=crashes["zip"].map(groups == "Q4").astype(bool),
                             weight=crashes[harm].astype(float), hour=crashes["hour"].astype(int))
    shares, totals = {}, {}
    for high, part in crashes.groupby("high"):
        cells = part.pivot_table(index="weekday", columns="hour", values="weight", aggfunc="sum", fill_value=0)
        cells = cells.reindex(index=WEEKDAYS, columns=range(24), fill_value=0)
        totals[high] = part["weight"].sum()
        shares[high] = cells / max(totals[high], 1) * 100
    return shares, totals, harm


def q3_night_share(shares, high):
    """Share of a group's harm between 22:00 and 05:59."""
    return float(shares[high][[22, 23, 0, 1, 2, 3, 4, 5]].to_numpy().sum())


def q3_when_crashes_happen(data, filters):
    """Q3 · Ali Issa · hour x weekday heatmap.
    Tables: crashes, zip_year. Filters: borough, year, housing_type, severity."""
    shares, totals, harm = q3_hour_shares(data, filters)
    if len(shares) < 2 or min(totals.values()) == 0:
        return no_data("Q3 When crashes happen", "Not enough crashes with a known hour for these filters")
    difference = shares[True] - shares[False]
    limit = float(np.abs(difference.to_numpy()).max())
    fig = go.Figure(go.Heatmap(
        z=difference.to_numpy(), x=list(range(24)), y=WEEKDAYS, colorscale="RdBu_r", zmid=0, zmin=-limit, zmax=limit,
        customdata=np.stack([shares[True].to_numpy(), shares[False].to_numpy()], axis=-1),
        colorbar=dict(title="points"),
        hovertemplate="%{y} %{x}:00<br>High-housing ZIPs: %{customdata[0]:.2f}%<br>Other ZIPs: %{customdata[1]:.2f}%"
                      "<br>Difference: %{z:+.2f} points<extra></extra>"))
    night_high, night_other = q3_night_share(shares, True), q3_night_share(shares, False)
    more = "larger" if night_high > night_other else "smaller"
    label = HARM_LABELS[harm].split(" (")[0]
    title = (f"High-housing ZIPs have a {more} share of their {label} late at night "
             f"(22:00–05:59: {night_high:.1f}% vs {night_other:.1f}% in other ZIPs)")
    fig.update_xaxes(title="hour of the day", dtick=2)
    fig.update_yaxes(autorange="reversed")
    fig = apply_style(fig, title)
    return note_below(fig, "Each cell: share of the group's harm in that hour, high-housing ZIPs (top quarter by affordable "
                           "units) minus other ZIPs; red = more common in high-housing ZIPs. Crashes logged at 00:00 "
                           "(time unknown) are left out.")


def q4_repeat_shares(data, filters):
    """Q4 data: share of serious harm at repeat-danger spots (lookback above 0) per year 2022-2025,
    for ZIPs split into thirds by affordable units completed over the whole window."""
    groups, _ = zip_housing_groups(data, filters, 3, ["Low", "Medium", "High"], use=("borough",))
    crashes = apply_filters(data["crashes"], filters, use=("borough",))
    crashes = crashes[crashes["zip"].isin(groups.index) & crashes["repeat_location"].notna()
                      & crashes["year"].between(2022, 2025)]
    weight = crashes[harm_column(filters)].astype(float)
    crashes = crashes.assign(third=crashes["zip"].map(groups), weight=weight,
                             repeat_weight=weight * crashes["repeat_location"].astype(float))
    table = (crashes.groupby(["third", "year"], observed=True)
                    .agg(weight=("weight", "sum"), repeat_weight=("repeat_weight", "sum"), crashes=("crash_id", "size"))
                    .reset_index())
    table["share"] = table["repeat_weight"] / table["weight"].where(table["weight"] > 0) * 100
    return table


def q4_left_unfixed(data, filters):
    """Q4 · Ali Issa · line by housing tercile.
    Tables: crashes, zip_year. Filters: borough, housing_type, severity."""
    table = q4_repeat_shares(data, filters)
    if table.empty or table["share"].isna().all():
        return no_data("Q4 Repeat danger spots", "Not enough crashes with a lookback value for these filters")
    fig = go.Figure()
    for third, colour, width in [("Low", "#C7C7C7", 2), ("Medium", "#8C8C8C", 2), ("High", ACCENT, 3)]:
        part = table[table["third"] == third]
        fig.add_trace(go.Scatter(
            x=part["year"], y=part["share"], mode="lines+markers", name=f"{third} affordable housing",
            line=dict(color=colour, width=width), customdata=part["crashes"],
            hovertemplate="%{x}: %{y:.1f}% at repeat-danger spots<br>%{customdata} crashes<extra>" + third + "</extra>"))
    high = table[table["third"] == "High"].set_index("year")["share"]
    others = table[table["third"] != "High"].groupby("year")[["repeat_weight", "weight"]].sum()
    others_share = others["repeat_weight"] / others["weight"] * 100
    always_higher = bool((high > others_share.reindex(high.index)).all())
    first, last = high.index.min(), high.index.max()
    trend = ("is not falling" if high[last] >= high[first] - 0.5 else "falls")
    if always_higher:
        title = (f"ZIPs with the most new affordable housing have the highest share of harm at known danger spots "
                 f"every year, and it {trend} ({high[first]:.1f}% in {first}, {high[last]:.1f}% in {last})")
    else:
        title = (f"Share of harm at known danger spots, by affordable-housing third "
                 f"(high: {high[first]:.1f}% in {first}, {high[last]:.1f}% in {last})")
    fig.update_xaxes(title="year", dtick=1)
    fig.update_yaxes(title="share of serious harm at repeat-danger spots (%)", rangemode="tozero")
    fig = apply_style(fig, title)
    return note_below(fig, "Repeat-danger spot = similar severe crashes at the same place in the 3 years before. "
                           "Only crashes with a lookback value (missing for part of 2023–2024). ZIP thirds by affordable "
                           "units completed Jan 2022 – Jun 2026. The year filter does not apply (the chart shows all years).")


Q5_GROUPS = ["Fewest units", "Second", "Third", "Most units"]


def rate_interval(deaths, crashes):
    """Deaths per 100 crashes with an approximate 95% interval (deaths treated as a Poisson count)."""
    rate = deaths / crashes * 100
    half = 1.96 * np.sqrt(deaths) / crashes * 100
    return rate, max(rate - half, 0), rate + half


def q5_fatality_rates(data, filters):
    """Q5 data: deaths per 100 serious crashes for ZIP quarters by affordable units, with all crashes
    and without highway crashes (D12)."""
    groups, _ = zip_housing_groups(data, filters, 4, Q5_GROUPS)
    crashes = apply_filters(data["crashes"], filters, use=("borough", "year"))
    crashes = crashes[crashes["zip"].isin(groups.index)].assign(quarter=lambda d: d["zip"].map(groups))
    rows = []
    for subset, part in [("All serious crashes", crashes), ("Without highway crashes", crashes[~crashes["is_highway"]])]:
        for quarter, group in part.groupby("quarter", observed=True):
            deaths, n = float(group["fatalities"].sum()), len(group)
            if n:
                rate, low, high = rate_interval(deaths, n)
                rows.append({"subset": subset, "quarter": quarter, "deaths": deaths, "crashes": n,
                             "rate": rate, "low": low, "high": high})
    return pd.DataFrame(rows)


def q5_how_deadly(data, filters):
    """Q5 · Mostafa Ayman · bar with confidence intervals.
    Tables: crashes, zip_year. Filters: borough, year, housing_type."""
    table = q5_fatality_rates(data, filters)
    if table.empty:
        return no_data("Q5 How deadly crashes are", "No serious crashes for these filters")
    fig = go.Figure()
    for subset, colour in [("All serious crashes", GREY), ("Without highway crashes", ACCENT)]:
        part = table[table["subset"] == subset]
        fig.add_trace(go.Bar(
            x=part["quarter"], y=part["rate"], name=subset, marker_color=colour,
            error_y=dict(type="data", symmetric=False, array=part["high"] - part["rate"],
                         arrayminus=part["rate"] - part["low"], color="black", thickness=1),
            customdata=part[["deaths", "crashes", "low", "high"]],
            hovertemplate="%{x}: %{y:.1f} deaths per 100 serious crashes<br>95% interval %{customdata[2]:.1f}–"
                          "%{customdata[3]:.1f}<br>%{customdata[0]:.0f} deaths in %{customdata[1]:,} crashes"
                          "<extra>" + subset + "</extra>"))
    street = table[table["subset"] == "Without highway crashes"].set_index("quarter")
    most = street.loc["Most units"] if "Most units" in street.index else None
    if most is not None:
        rest = street.drop(index="Most units")
        rest_rate, rest_low, rest_high = rate_interval(rest["deaths"].sum(), max(rest["crashes"].sum(), 1))
        # Compare with the other three quarters pooled; "more"/"less" only when the two 95% intervals don't overlap
        overlap = rest_low <= most["high"] and rest_high >= most["low"]
        word = "about as" if overlap else ("more" if most["rate"] > rest_rate else "less")
        title = (f"On city streets, serious crashes are {word} deadly in the ZIPs with the most new affordable housing "
                 f"({most['rate']:.1f} deaths per 100) as in the other ZIPs ({rest_rate:.1f})")
        if word in ("more", "less"):
            title = title.replace(" as in the other", " than in the other")
    else:
        title = "Deaths per 100 serious crashes, by affordable-housing quarter of ZIPs"
    fig.update_layout(barmode="group", legend_title_text="")
    fig.update_xaxes(title="ZIPs in four equal groups by affordable units completed (Jan 2022 – Jun 2026)")
    fig.update_yaxes(title="deaths per 100 serious crashes", rangemode="tozero")
    fig = apply_style(fig, title)
    return note_below(fig, "Black lines: approximate 95% intervals (deaths as a Poisson count). Highway crashes are "
                           "deadlier and mostly have no ZIP, so the street-only bars are the fair comparison (D12). "
                           "The severity filter does not apply (the chart is about deaths).")


Q6_MIN_UNITS, Q6_MAX_YEARS = 100, 3      # D11; and the 3-year cap on "under construction" (D63)


def q6_construction_status(data, filters, max_years=Q6_MAX_YEARS):
    """Q6 data: every ZIP-month flagged "under construction" when a New Construction building of 100+ total units
    in that ZIP is between its project start and its completion. No completion date: active until the end of the
    window, but never longer than 3 years after the start. Only ZIPs with both kinds of months are kept."""
    buildings = data["buildings"]
    sites = buildings[(buildings["construction_type"] == "New Construction") & buildings["zip"].notna()
                      & (buildings["total_units"] >= Q6_MIN_UNITS)].drop_duplicates("building_id")
    sites = apply_filters(sites, filters, use=("borough",))
    end = sites["completion_date"].fillna(pd.Timestamp(WINDOW_END))
    latest = sites["project_start"] + pd.DateOffset(years=max_years)
    end = end.where(end <= latest, latest)
    sites = sites.assign(start_month=sites["project_start"].dt.to_period("M").dt.to_timestamp(), end_date=end)

    zip_month = apply_filters(data["zip_month"], filters, use=("borough", "year"))
    pairs = zip_month[["zip", "month"]].merge(sites[["zip", "start_month", "end_date"]], on="zip")
    pairs["active"] = (pairs["month"] >= pairs["start_month"]) & (pairs["month"] <= pairs["end_date"])
    active = pairs.groupby(["zip", "month"])["active"].any()
    months = zip_month.merge(active.rename("under_construction").reset_index(), on=["zip", "month"], how="left")
    months["under_construction"] = months["under_construction"].astype("boolean").fillna(False).astype(bool)
    both = months.groupby("zip")["under_construction"].transform(lambda s: s.any() and not s.all())
    return months[both]


def q6_summary(months):
    """Average monthly serious harm per ZIP, under construction vs not: first per ZIP, then averaged over ZIPs
    (so every ZIP counts once and is compared with itself), by borough and for all of NYC."""
    per_zip = months.groupby(["borough", "zip", "under_construction"])["serious_harm"].mean().unstack().dropna()
    months_count = months.groupby(["borough", "under_construction"]).size().unstack(fill_value=0)
    rows = []
    for borough, part in [("All NYC", per_zip)] + [(b, per_zip.loc[b]) for b in BOROUGHS if b in per_zip.index.get_level_values(0)]:
        count = months_count.sum() if borough == "All NYC" else months_count.loc[borough]
        for status in (False, True):
            rows.append({"borough": borough, "under_construction": status, "harm": part[status].mean(),
                         "zips": len(part), "zip_months": int(count.get(status, 0)),
                         "share_zips_higher": float((part[True] > part[False]).mean())})
    return pd.DataFrame(rows)


def q6_during_construction(data, filters):
    """Q6 · Mostafa Ayman · grouped bar.
    Tables: buildings, zip_month. Filters: borough, year. New Construction only."""
    months = q6_construction_status(data, filters)
    if months.empty:
        return no_data("Q6 Danger during construction", "No ZIPs with both construction and non-construction months")
    summary = q6_summary(months)
    fig = go.Figure()
    for status, name, colour in [(False, "No large site under construction", GREY),
                                 (True, "Large affordable building under construction", ACCENT)]:
        part = summary[summary["under_construction"] == status]
        fig.add_trace(go.Bar(
            x=part["borough"], y=part["harm"], name=name, marker_color=colour,
            customdata=part[["zips", "zip_months"]],
            hovertemplate="%{x}: %{y:.2f} serious harm per ZIP per month<br>%{customdata[0]} ZIPs, "
                          "%{customdata[1]:,} ZIP-months<extra>" + name + "</extra>"))
    nyc = summary[summary["borough"] == "All NYC"].set_index("under_construction")
    during, other = nyc.loc[True, "harm"], nyc.loc[False, "harm"]
    if abs(during - other) < 0.1:
        title = (f"Streets are no more dangerous while a large affordable building is going up "
                 f"({during:.2f} vs {other:.2f} serious harm per ZIP per month)")
    else:
        title = (f"Serious harm is {'higher' if during > other else 'lower'} while a large affordable building is going up "
                 f"({during:.2f} vs {other:.2f} per ZIP per month)")
    fig.update_layout(barmode="group", legend_title_text="")
    fig.update_yaxes(title="average serious harm per ZIP per month", rangemode="tozero")
    fig = apply_style(fig, title)
    return note_below(fig, f"New Construction buildings with {Q6_MIN_UNITS}+ total units, from project start to completion "
                           f"(at most {Q6_MAX_YEARS} years). Each ZIP is compared with its own other months; only ZIPs with "
                           "both kinds of months. The housing-type and severity filters do not apply.")


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
    return note_below(fig, f"{len(table)} ZIPs with ≥{Q7_MIN_UNITS} New Construction units by end {Q7_START_YEAR} and "
                           f"≥{Q7_MIN_CRASHES} serious crashes in {Q7_START_YEAR} · dashed lines = medians · correlation "
                           "is not causation · fixed years: year, housing-type and severity filters do not apply")


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
    return apply_filters(existing_buildings(data), filters, use=("borough", "housing_type"))


def existing_buildings(data):
    """Located affordable buildings completed by 30 Jun 2026, one row per building: the same set and the
    same order of steps as notebook 8.3 (one row per building_id first, its latest project; then completed)."""
    buildings = data["buildings"][data["buildings"]["has_location"]]
    buildings = buildings.sort_values("project_start").drop_duplicates("building_id", keep="last")
    return buildings[buildings["completion_date"] <= Q8_WINDOW_END]


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
        height=640, legend=dict(orientation="h", y=-0.08, x=0), margin=dict(l=40, r=20))
    fig.update_xaxes(title=harm_label, rangemode="tozero", row=1, col=2)
    return note_below(fig, "Street crashes only (no highways) · corridor = street + borough · buildings completed by "
                           "Jun 2026 · hover a bar for repeat-danger share and nearby units", y=-0.16)


INCOME_TIERS = {"units_extremely_low": "Extremely low income", "units_very_low": "Very low income",
                "units_low": "Low income", "units_moderate": "Moderate income", "units_middle": "Middle income",
                "units_other_income": "Other income (e.g. super's unit)"}
CRASH_METRICS = {"serious_harm": "Serious harm", "fatalities": "Deaths", "n_repeat_crashes": "Crashes at repeat-danger spots"}


def q9_feature_table(data, filters):
    """Q9 data: one row per ZIP with the make-up of the affordable units completed in the window
    (shares by income tier, bedroom size, tenure, construction type, plus total units as a size reference)
    and the ZIP's crash measures over the same period."""
    buildings = data["buildings"]
    done = buildings[buildings["completed_in_window"] & buildings["zip"].notna()]
    done = apply_filters(done, filters, use=("borough", "housing_type"))
    year = filters.get("year", "All")
    if year != "All":
        done = done[done["completion_year"] == year]
    unit_cols = list(INCOME_TIERS) + ["units_studio", "units_1br", "units_2br", "units_3br", "units_4br",
                                       "units_5br", "units_6br_plus", "units_rental", "units_homeownership"]
    per_zip = done.groupby("zip")[unit_cols + ["all_counted_units"]].sum().astype(float)
    per_zip["nc_units"] = done[done["construction_type"] == "New Construction"].groupby("zip")["all_counted_units"].sum()
    per_zip = per_zip[per_zip["all_counted_units"] > 0].fillna(0)
    total = per_zip["all_counted_units"]

    features = pd.DataFrame(index=per_zip.index)
    for col, label in INCOME_TIERS.items():
        features[label] = per_zip[col] / total
    features["Studios"] = per_zip["units_studio"] / total
    features["1 bedroom"] = per_zip["units_1br"] / total
    features["2 bedrooms"] = per_zip["units_2br"] / total
    features["3+ bedrooms"] = per_zip[["units_3br", "units_4br", "units_5br", "units_6br_plus"]].sum(axis=1) / total
    tenure = per_zip["units_rental"] + per_zip["units_homeownership"]
    features["Rental (vs homeownership)"] = per_zip["units_rental"] / tenure.where(tenure > 0)
    if filters.get("housing_type", "All") == "All":     # with one type chosen, this share is always 0 or 1
        features["New Construction (vs Preservation)"] = per_zip["nc_units"] / total
    features["Total affordable units (size, for reference)"] = total

    crashes = apply_filters(data["zip_year"], filters, use=("borough", "year")).groupby("zip")[list(CRASH_METRICS)].sum()
    return features.join(crashes, how="inner")


def q9_correlations(table):
    """Spearman correlation of every housing feature with every crash measure, and the number of ZIPs used."""
    features = [col for col in table.columns if col not in CRASH_METRICS]
    rho = pd.DataFrame({CRASH_METRICS[m]: [spearman(table[f], table[m]) for f in features] for m in CRASH_METRICS},
                       index=features)
    n = pd.Series({f: int(table[f].notna().sum()) for f in features})
    return rho, n


def q9_housing_features(data, filters):
    """Q9 · Mostafa Alaa · correlation heatmap.
    Tables: buildings, zip_year. Filters: borough, year, housing_type."""
    table = q9_feature_table(data, filters)
    if len(table) < 10:
        return no_data("Q9 Housing features vs crashes", "Fewer than 10 ZIPs with completed units for these filters")
    rho, n = q9_correlations(table)
    values = rho.to_numpy(dtype=float)
    fig = go.Figure(go.Heatmap(
        z=values, x=list(rho.columns), y=list(rho.index), colorscale="RdBu_r", zmid=0, zmin=-1, zmax=1,
        text=np.round(values, 2), texttemplate="%{text}", colorbar=dict(title="Spearman ρ"),
        customdata=np.repeat(n.to_numpy()[:, None], len(rho.columns), axis=1),
        hovertemplate="%{y} vs %{x}<br>ρ = %{z:.2f} over %{customdata} ZIPs<extra></extra>"))
    size_row = "Total affordable units (size, for reference)"
    mix = rho.drop(index=size_row)["Serious harm"]
    strongest = mix.abs().max()
    title = (f"How much housing a ZIP gets tracks its serious harm (ρ = {rho.loc[size_row, 'Serious harm']:.2f}); "
             f"what kind of housing it gets barely does (every share |ρ| ≤ {strongest:.2f})")
    fig.update_yaxes(autorange="reversed")
    fig = apply_style(fig, title)
    fig.update_layout(height=620, margin=dict(l=280))
    return note_below(fig, f"{len(table)} ZIPs with affordable units completed Jan 2022 – Jun 2026. Rows: share of a ZIP's "
                           "affordable units (last row: total units). Correlation is not causation.", y=-0.12)


DANGER_GROUPS = ["Safest fifth", "Second", "Third", "Fourth", "Most dangerous fifth"]
Q10_START_YEARS = [2023, 2024, 2025]


def q10_projects_by_danger(data, filters):
    """Q10 data: ZIPs ranked by their serious harm in 2022 and split into five equal groups; then the affordable
    projects started 2023-2025 (or in the chosen year) counted by the group of their building's ZIP.
    A project with buildings in two ZIPs counts once in each."""
    zip_year = apply_filters(data["zip_year"], filters, use=("borough",))
    harm_2022 = zip_year[zip_year["year"] == 2022].groupby("zip")["serious_harm"].sum()
    if len(harm_2022) < 5:
        return pd.DataFrame(), None
    groups = equal_groups(harm_2022, DANGER_GROUPS)
    year = filters.get("year", "All")
    years = [year] if year in Q10_START_YEARS else Q10_START_YEARS
    buildings = apply_filters(data["buildings"], filters, use=("borough", "housing_type"))
    started = buildings[buildings["zip"].isin(groups.index) & buildings["project_start"].dt.year.isin(years)]
    started = started.assign(group=started["zip"].map(groups))
    projects = started.drop_duplicates(["project_id", "zip"])
    table = pd.DataFrame({
        "projects": projects.groupby("group", observed=False).size(),
        "units": started.groupby("group", observed=False)["all_counted_units"].sum().astype(float),
        "harm_2022_min": harm_2022.groupby(groups, observed=False).min(),
        "harm_2022_max": harm_2022.groupby(groups, observed=False).max(),
        "zips": groups.value_counts().reindex(DANGER_GROUPS)}).reindex(DANGER_GROUPS)
    table["project_share"] = table["projects"] / max(table["projects"].sum(), 1) * 100
    table["unit_share"] = table["units"] / max(table["units"].sum(), 1) * 100
    return table, years


def q10_danger_before(data, filters):
    """Q10 · Mostafa Alaa · bar by 2022 danger quintile.
    Tables: buildings, zip_year. Filters: borough, year, housing_type."""
    table, years = q10_projects_by_danger(data, filters)
    if table.empty or table["projects"].sum() == 0:
        return no_data("Q10 Was the danger already there", "No affordable projects started for these filters")
    colours = [ACCENT if group == DANGER_GROUPS[-1] else GREY for group in DANGER_GROUPS]
    fig = go.Figure(go.Bar(
        x=DANGER_GROUPS, y=table["project_share"], marker_color=colours, text=table["project_share"].round(0),
        texttemplate="%{text:.0f}%", textposition="outside",
        customdata=table[["projects", "units", "unit_share", "harm_2022_min", "harm_2022_max", "zips"]],
        hovertemplate="%{x} (%{customdata[5]} ZIPs, 2022 serious harm %{customdata[3]:.0f}–%{customdata[4]:.0f})<br>"
                      "%{customdata[0]} new projects (%{y:.1f}%)<br>%{customdata[1]:,.0f} affordable units "
                      "(%{customdata[2]:.1f}%)<extra></extra>"))
    fig.add_hline(y=20, line=dict(color="black", dash="dash"),
                  annotation_text="20% = an even spread", annotation_position="top left")
    when = f"{years[0]}–{years[-1]}" if len(years) > 1 else str(years[0])
    title = (f"{table.loc[DANGER_GROUPS[-1], 'project_share']:.0f}% of the affordable projects started in {when} went to "
             f"the fifth of ZIPs that were most dangerous in 2022")
    fig.update_xaxes(title="ZIPs in five equal groups by serious harm in 2022")
    fig.update_yaxes(title="share of new affordable projects (%)", rangemode="tozero")
    fig = apply_style(fig, title)
    return note_below(fig, "Projects by start date (Project Start Date); confidential projects have no ZIP and are not "
                           "included. The year filter picks one start year (2023–2025); other years show all three. "
                           "Correlation is not causation.")


def q11_building_bands(data, filters, radius_column="crashes_100m"):
    """Q11 data: affordable buildings completed by 30 Jun 2026 (one row per building, as in 8.3) with the number of
    non-highway serious crashes within 100 m, grouped as 0 / 1 / 2+ per borough."""
    buildings = apply_filters(existing_buildings(data), filters, use=("borough", "housing_type"))
    year = filters.get("year", "All")
    if year != "All":
        buildings = buildings[buildings["completion_year"] == year]
    table = buildings.merge(data["building_crash_counts"], on="building_id")
    table["band"] = pd.cut(table[radius_column], [-1, 0, 1, np.inf], labels=["0", "1", "2+"])
    counts = pd.crosstab(table["borough"], table["band"]).reindex(columns=["0", "1", "2+"], fill_value=0)
    shares = counts.div(counts.sum(axis=1), axis=0) * 100
    order = (shares["1"] + shares["2+"]).sort_values(ascending=False).index
    return counts.loc[order], shares.loc[order], table


def q11_doorstep_danger(data, filters):
    """Q11 · Moustafa Maged · stacked bar by borough.
    Tables: buildings, building_crash_counts. Filters: borough, year, housing_type, severity."""
    counts, shares, table = q11_building_bands(data, filters)
    if table.empty:
        return no_data("Q11 Doorstep danger", "No completed affordable buildings for these filters")
    fig = go.Figure()
    for band, name, colour in [("0", "No serious crash", "#E3E3E3"), ("1", "1 serious crash", GREY),
                               ("2+", "2 or more", ACCENT)]:
        fig.add_trace(go.Bar(
            x=shares.index, y=shares[band], name=name, marker_color=colour, customdata=counts[band],
            hovertemplate="%{x}: %{y:.1f}% of buildings (%{customdata:,})<extra>" + name + "</extra>"))
    any_crash = shares["1"] + shares["2+"]
    overall = (table["crashes_100m"] > 0).mean() * 100
    if len(any_crash) > 1:
        title = (f"{overall:.0f}% of affordable buildings had a serious crash within 100 m (about a block): "
                 f"{any_crash.iloc[0]:.0f}% in {any_crash.index[0]}, {any_crash.iloc[-1]:.0f}% in {any_crash.index[-1]}")
    else:
        title = f"{overall:.0f}% of affordable buildings in {any_crash.index[0]} had a serious crash within 100 m (about a block)"
    fig.update_layout(barmode="stack", legend_title_text="Within 100 m, Jan 2022 – Jun 2026")
    fig.update_yaxes(title="share of affordable buildings (%)", range=[0, 100])
    fig = apply_style(fig, title)
    return note_below(fig, "Buildings completed by Jun 2026, one per building; street crashes only (no highways). Crashes "
                           "over the whole window, also before a building was finished. The year filter picks buildings "
                           "completed in that year; the severity filter does not apply (crashes are counted).")


Q12_YEARS = [2022, 2023, 2024, 2025]       # full years only (2026 is Jan-Jun)


def q12_borough_years(data, filters):
    """Q12 data: per borough and full year, affordable units completed, serious harm and cumulative units."""
    units, harm = units_column(filters), harm_column(filters)
    table = data["borough_year"]
    table = table[table["year"].isin(Q12_YEARS)].sort_values(["borough", "year"]).copy()
    table["units"], table["harm"] = table[units].astype(float), table[harm].astype(float)
    table["cumulative_units"] = table.groupby("borough")["units"].cumsum()
    return table, units, harm


def q12_borough_balance(data, filters):
    """Q12 · Moustafa Maged · animated bubble.
    Tables: borough_year. Filters: severity (always shows all boroughs and years)."""
    table, units, harm = q12_borough_years(data, filters)
    if table.empty:
        return no_data("Q12 Borough balance over time", "No data")
    colours = dict(zip(BOROUGHS, ["#4C6A92", "#D1495B", "#E09F3E", "#2E8B57", "#7F7F7F"]))
    sizeref = 2 * table["cumulative_units"].max() / 60 ** 2

    def bubbles(year):
        part = table[table["year"] == year]
        return [go.Scatter(
            x=[row["units"]], y=[row["harm"]], mode="markers+text", name=row["borough"], text=[row["borough"]],
            textposition="top center", showlegend=False, cliponaxis=False,   # labels may go past the axes
            marker=dict(size=[max(row["cumulative_units"], 1)], sizemode="area", sizeref=sizeref, sizemin=6,
                        color=colours[row["borough"]], opacity=0.85, line=dict(width=1, color="white")),
            customdata=[[row["cumulative_units"], year]],
            hovertemplate=row["borough"] + " %{customdata[1]}<br>Units completed: %{x:,.0f}<br>"
                          + HARM_LABELS[harm].split(" (")[0].capitalize() + ": %{y:,.0f}<br>Units since Jan 2022: "
                          "%{customdata[0]:,.0f}<extra></extra>") for _, row in part.iterrows()]

    trails = [go.Scatter(x=part["units"], y=part["harm"], mode="lines", hoverinfo="skip", showlegend=False,
                         line=dict(color=colours[b], width=1, dash="dot"), opacity=0.4)
              for b, part in table.groupby("borough")]
    first, last = Q12_YEARS[0], Q12_YEARS[-1]
    fig = go.Figure(data=trails + bubbles(first),
                    frames=[go.Frame(data=bubbles(year), traces=list(range(len(trails), len(trails) + 5)), name=str(year))
                            for year in Q12_YEARS])
    wide = table.pivot(index="borough", columns="year", values=["units", "harm"])
    better = [b for b in wide.index if wide.loc[b, ("units", last)] > wide.loc[b, ("units", first)]
              and wide.loc[b, ("harm", last)] < wide.loc[b, ("harm", first)]]
    label = HARM_LABELS[harm].split(" (")[0]
    if better:
        title = (f"Only {', '.join(better)} moved to more new homes and less {label} from {first} to {last}; "
                 "in the other boroughs both moved together or housing fell")
    else:
        title = (f"No borough moved to more affordable homes and less {label} from {first} to {last}: "
                 "housing output swings from year to year, harm barely moves")
    fig.update_layout(
        height=620,
        updatemenus=[dict(type="buttons", x=0, y=-0.2, xanchor="left", yanchor="top", showactive=False,
                          buttons=[dict(label="▶ Play", method="animate",
                                        args=[None, dict(frame=dict(duration=900, redraw=True), fromcurrent=True,
                                                         transition=dict(duration=400))]),
                                   dict(label="❚❚ Pause", method="animate",
                                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])])],
        sliders=[dict(active=0, x=0.15, y=-0.2, yanchor="top", len=0.85, currentvalue=dict(prefix="Year: "),
                      steps=[dict(label=str(year), method="animate",
                                  args=[[str(year)], dict(mode="immediate", frame=dict(duration=400, redraw=True))])
                             for year in Q12_YEARS])])
    fig.update_xaxes(title=f"{UNIT_LABELS[units]} in the year", range=[0, table["units"].max() * 1.15])
    fig.update_yaxes(title=f"{HARM_LABELS[harm]} in the year", range=[0, table["harm"].max() * 1.15])
    fig = apply_style(fig, title)
    fig.update_layout(margin=dict(b=230))     # room for the play buttons, the year slider and the note
    return note_below(fig, "Bubble size = affordable units completed since Jan 2022; dotted lines = each borough's path "
                           f"{first}–{last}. Full years only; all boroughs always shown (the borough and year filters do "
                           "not apply). Includes records without a ZIP.", y=-0.45)


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
