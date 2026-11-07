"""Homes on Dangerous Streets: the project website (Dash).

Run locally:   python app/app.py      then open http://127.0.0.1:8050
On Vercel:     api/index.py imports `server` from this file.

How it works: the six tables from data/processed/ are loaded once at start-up (src/data_loader.py). The filter bar
(4 dropdowns + search box) only sets filters; the Generate Report button (or Enter in the search box) redraws all
12 charts with them, through the shared chart functions in src/charts.py (the same ones the notebook uses).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "src"), str(HERE)]

from dash import Dash, Input, Output, State, ctx, dcc, html, no_update  # noqa: E402

import charts  # noqa: E402
import story  # noqa: E402
from data_loader import load_tables  # noqa: E402
from search import parse_search  # noqa: E402

DATA = load_tables()
FILTER_KEYS = list(charts.FILTER_OPTIONS)            # borough, year, housing_type, severity
FILTER_LABELS = {"borough": "Borough", "year": "Year", "housing_type": "Housing type", "severity": "Crash measure"}
OPTION_LABELS = {"severity": {"All": "Serious harm (all)"}, "year": {2026: "2026 (Jan–Jun)"}}
CHART_KEYS = list(charts.CHARTS)
GRAPH_CONFIG = {"displaylogo": False, "responsive": True,
                "modeBarButtonsToRemove": ["select2d", "lasso2d", "autoScale2d"]}


def hero_numbers(data):
    """The three hook numbers, computed from the same tables as the charts."""
    buildings, crashes = data["buildings"], data["crashes"]
    return {"units": int(buildings.loc[buildings["completed_in_window"], "all_counted_units"].sum()),
            "crashes": len(crashes), "deaths": int(crashes["fatalities"].sum())}


def describe(filters):
    """One line saying which filters the charts now use."""
    parts = [f"{FILTER_LABELS[key]}: {OPTION_LABELS.get(key, {}).get(value, value)}" for key, value in filters.items()]
    return "Showing · " + " · ".join(parts)


def build_figures(filters):
    """All 12 charts for one set of filters, through the shared chart functions."""
    return [charts.CHARTS[key](DATA, filters) for key in CHART_KEYS]


# The default view is built once at start-up and put straight into the page, so opening the page doesn't
# redraw all 12 charts; the callback below only runs on Generate Report, Enter in the search box, or Reset
DEFAULT_FIGURES = dict(zip(CHART_KEYS, build_figures(charts.DEFAULT_FILTERS)))


# ---------------------------------------------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------------------------------------------
def filter_dropdown(key):
    options = [{"label": str(OPTION_LABELS.get(key, {}).get(value, value)), "value": value}
               for value in charts.FILTER_OPTIONS[key]]
    return html.Div([html.Label(FILTER_LABELS[key], htmlFor=f"filter-{key}"),
                     dcc.Dropdown(id=f"filter-{key}", options=options, value="All", clearable=False,
                                  searchable=False)], className="filter")


def filter_bar():
    return html.Div([
        html.Div([filter_dropdown(key) for key in FILTER_KEYS], className="filters"),
        html.Div([
            html.Div([html.Label("Search", htmlFor="search"),
                      dcc.Input(id="search", type="text", debounce=False, n_submit=0,
                                placeholder='Type e.g. "Brooklyn 2022 new buildings" or "Bronx deaths", then Enter')],
                     className="filter search"),
            html.Button("Generate Report", id="generate", n_clicks=0, className="primary"),
            html.Button("Reset", id="reset", n_clicks=0, className="secondary"),
        ], className="actions"),
        html.Div(describe(charts.DEFAULT_FILTERS), id="status", className="status", role="status"),
    ], className="filter-bar", id="filter-bar")


def chart_card(key, heading, takeaway):
    return html.Article([
        html.H3(heading),
        html.P(takeaway, className="takeaway"),
        dcc.Loading(dcc.Graph(id=f"graph-{key}", figure=DEFAULT_FIGURES[key], config=GRAPH_CONFIG, className="graph"),
                    type="dot", color=charts.ACCENT),
        html.P(f"Question {key[1:].upper()} · notebook section 10.{key[1:]}", className="source"),
    ], className="chart-card", id=f"card-{key}")


def act_section(act):
    panel = html.Div([html.Div([html.H4(label), html.P(text)], className="panel-box")
                      for label, text in act["panel"].items()], className="panel")
    return html.Section([html.H2(act["title"]), html.P(act["intro"], className="intro"),
                         *[chart_card(*chart) for chart in act["charts"]], panel],
                        id=act["id"], className="act")


def act5_section():
    headlines = html.Div([html.Div([html.Span(big, className="headline-number"), html.P(text)], className="headline")
                          for big, text in story.HEADLINES], className="headlines")
    impact = html.Table([
        html.Thead(html.Tr([html.Th("Who"), html.Th("Based on"), html.Th("What they should do")])),
        html.Tbody([html.Tr([html.Td(who), html.Td(questions), html.Td(action)])
                    for who, questions, action in story.IMPACT])], className="impact")
    return html.Section([
        html.H2("Act 5 · So what?"),
        html.H3("Headline findings"), headlines,
        html.H3("What the data can't tell us"), dcc.Markdown("\n".join(f"- {limit}" for limit in story.LIMITS)),
        html.H3("Who can use this, and what they should do"), impact,
    ], id="act5", className="act")


def about_section():
    return html.Section([
        html.H2("About"),
        html.H3("Data"),
        html.Ul([html.Li(html.A(name, href=url, target="_blank", rel="noopener")) for name, url in story.DATASETS]),
        html.H3("Method"), html.P(story.METHOD),
    ], id="about", className="act")


def hero():
    numbers = hero_numbers(DATA)
    return html.Header([
        html.P(story.TITLE, className="kicker"),
        html.H1(story.FINDING_TITLE),
        html.P(story.SUBTITLE, className="subtitle"),
        html.Div([html.Div([html.Span(f"{numbers['units']:,}", className="big"),
                            html.Span("affordable homes completed or preserved")], className="stat"),
                  html.Div([html.Span(f"{numbers['crashes']:,}", className="big"),
                            html.Span("crashes that seriously injured or killed")], className="stat"),
                  html.Div([html.Span(f"{numbers['deaths']:,}", className="big accent"),
                            html.Span("people killed")], className="stat")], className="stats"),
        html.P(story.HOOK.format(**numbers), className="hook"),
        html.P([html.Strong("Our question: "), story.QUESTION], className="question"),
        html.Nav([html.A(label, href=f"#{target}") for label, target in
                  [("1 · Big picture", "act1"), ("2 · Where", "act2"), ("3 · A building's life", "act3"),
                   ("4 · The danger", "act4"), ("5 · So what?", "act5"), ("About", "about")]], className="nav"),
    ], className="hero")


app = Dash(__name__, title="Homes on Dangerous Streets", assets_folder=str(HERE / "assets"),
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server          # the WSGI app that Vercel (and gunicorn) serve

app.layout = html.Div([
    hero(),
    filter_bar(),
    html.P("The charts change with the filters when you press Generate Report (or Enter in the search box). The text "
           "under each chart describes the default view: all boroughs, all years, all housing types, all serious harm.",
           className="hint"),
    html.Main([*[act_section(act) for act in story.ACTS], act5_section(), about_section()]),
], className="page")


# ---------------------------------------------------------------------------------------------------------------
# Generate Report: one callback redraws all 12 charts
# ---------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output(f"graph-{key}", "figure") for key in CHART_KEYS]
    + [Output(f"filter-{key}", "value") for key in FILTER_KEYS]
    + [Output("search", "value"), Output("status", "children")],
    Input("generate", "n_clicks"), Input("search", "n_submit"), Input("reset", "n_clicks"),
    [State(f"filter-{key}", "value") for key in FILTER_KEYS], State("search", "value"),
    prevent_initial_call=True,           # the page already holds the default charts
)
def generate_report(_generate, _submit, _reset, *values):
    """Redraw every chart (charts.CHARTS) for the chosen filters.

    - Generate Report: uses the dropdowns only.
    - Enter in the search box: the filters the text mentions replace those dropdowns (also "All", e.g. for
      "citywide"); the others stay as they are. The box is then cleared, so the text can't override a later
      dropdown choice.
    - Reset: back to the default view.
    """
    *dropdowns, search_text = values
    filters = dict(zip(FILTER_KEYS, dropdowns))
    search_box, notes = no_update, []
    if ctx.triggered_id == "reset":
        filters, search_box = dict(charts.DEFAULT_FILTERS), ""
    elif ctx.triggered_id == "search":
        chosen, understood, ignored = parse_search(search_text)
        filters.update(chosen)
        search_box = ""
        notes.append(f'Search "{(search_text or "").strip()}" understood: '
                     + (", ".join(understood) if understood else "nothing"))
        if ignored:
            notes.append("ignored: " + ", ".join(ignored))
    status = [html.Span(describe(filters))] + ([html.Span(" · ".join(notes), className="search-note")] if notes else [])
    return build_figures(filters) + [filters[key] for key in FILTER_KEYS] + [search_box, status]


if __name__ == "__main__":
    app.run(debug=False, port=8050)
