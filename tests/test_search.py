"""Tests for search mode and the Generate Report button.

Run from the repository root:   python tests/test_search.py
(Each test_ function also works with pytest.)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "app")]

from search import parse_search  # noqa: E402


# --- the parser -------------------------------------------------------------------------------------------------
def test_example_queries():
    assert parse_search("Brooklyn 2022 new buildings")[0] == {
        "year": 2022, "borough": "Brooklyn", "housing_type": "New Construction"}
    assert parse_search("Bronx 2024 new construction fatal")[0] == {
        "borough": "Bronx", "year": 2024, "housing_type": "New Construction", "severity": "Deaths"}
    assert parse_search("THE BRONX, killed!")[0] == {"borough": "Bronx", "severity": "Deaths"}
    assert parse_search("staten island preservation")[0] == {"borough": "Staten Island", "housing_type": "Preservation"}
    assert parse_search("")[0] == {}


def test_new_york_is_not_new_construction():          # review item 2
    chosen, _, ignored = parse_search("new york deaths")
    assert chosen == {"borough": "All", "severity": "Deaths"}
    assert "housing_type" not in chosen and "york" not in ignored


def test_second_value_is_reported_not_dropped():      # review item 3
    chosen, _, ignored = parse_search("Bronx and Brooklyn")
    assert chosen == {"borough": "Bronx"}             # the first one in the text wins
    assert any(word.startswith("brooklyn") for word in ignored)
    chosen, _, ignored = parse_search("deaths 2022 injuries")
    assert chosen == {"severity": "Deaths", "year": 2022}
    assert any(word.startswith("injuries") for word in ignored)


def test_all_words_reset_a_filter():                  # review item 4 (parser side)
    assert parse_search("citywide")[0] == {"borough": "All"}
    assert parse_search("all boroughs 2024")[0] == {"borough": "All", "year": 2024}
    assert parse_search("all years all types all harm")[0] == {"year": "All", "housing_type": "All", "severity": "All"}


def test_every_year_is_checked():                     # review items 5 and 6
    chosen, _, ignored = parse_search("2019 and 2023")
    assert chosen == {"year": 2023}
    assert any(word.startswith("2019") for word in ignored)
    chosen, _, ignored = parse_search("2024 queens 2025")
    assert chosen == {"year": 2024, "borough": "Queens"} and any(word.startswith("2025") for word in ignored)
    assert parse_search("2024 queens 2024")[1] == ["year: 2024", "borough: Queens"]   # a repeat is not ignored


def test_unknown_words_are_reported():
    chosen, _, ignored = parse_search("Manhattan xyz")
    assert chosen == {"borough": "Manhattan"} and ignored == ["xyz"]


# --- the website callback ---------------------------------------------------------------------------------------
def _press(client, trigger, dropdowns, search_text):
    """Send one Generate Report / Enter / Reset request, exactly like the browser does."""
    import app as site
    callback = client.get("/_dash-dependencies").get_json()[0]
    outputs = [{"id": o.split(".")[0], "property": o.split(".")[1]} for o in callback["output"].strip(".").split("...")]
    prop = {"generate": "n_clicks", "search": "n_submit", "reset": "n_clicks"}
    payload = {"output": callback["output"], "outputs": outputs,
               "inputs": [{"id": i, "property": p, "value": 1} for i, p in prop.items()],
               "state": [{"id": f"filter-{k}", "property": "value", "value": v} for k, v in zip(site.FILTER_KEYS, dropdowns)]
               + [{"id": "search", "property": "value", "value": search_text}],
               "changedPropIds": [f"{trigger}.{prop[trigger]}"]}
    response = client.post("/_dash-update-component", json=payload)
    assert response.status_code == 200, response.data[:300]
    body = response.get_json()["response"]
    return ({k: body[f"filter-{k}"]["value"] for k in site.FILTER_KEYS},
            body.get("search", {}).get("value", "<unchanged>"), sum(k.startswith("graph-") for k in body))


def test_website_callback():
    import app as site
    client = site.server.test_client()

    # Review item 1: Generate Report uses the dropdowns, never old search text
    filters, box, charts_drawn = _press(client, "generate", ["Queens", "All", "All", "All"], "Brooklyn")
    assert filters["borough"] == "Queens" and charts_drawn == 12

    # Enter applies the search to the filters it mentions, keeps the others, and clears the box
    filters, box, _ = _press(client, "search", ["Queens", 2024, "All", "All"], "Brooklyn deaths")
    assert filters == {"borough": "Brooklyn", "year": 2024, "housing_type": "All", "severity": "Deaths"} and box == ""

    # Review item 4: "citywide" sets the borough dropdown back to All
    filters, _, _ = _press(client, "search", ["Queens", "All", "All", "All"], "citywide")
    assert filters["borough"] == "All"

    # Reset clears everything
    filters, box, _ = _press(client, "reset", ["Queens", 2024, "Preservation", "Deaths"], "x")
    assert filters == {"borough": "All", "year": "All", "housing_type": "All", "severity": "All"} and box == ""

    # Review item 8: the callback does not run when the page opens; the page already holds the 12 charts
    assert client.get("/_dash-dependencies").get_json()[0]["prevent_initial_call"] is True
    layout = client.get("/_dash-layout").get_data(as_text=True)
    assert layout.count('"figure"') >= 12


if __name__ == "__main__":
    tests = [value for name, value in dict(globals()).items() if name.startswith("test_")]
    for test in tests:
        test()
        print("passed:", test.__name__)
    print(f"all {len(tests)} tests passed")
