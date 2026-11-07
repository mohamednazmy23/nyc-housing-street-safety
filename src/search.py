"""Search mode: turn a typed query into the same filters the dropdowns set.

Example: "Brooklyn 2022 new buildings" -> borough Brooklyn, year 2022, housing type New Construction.
Words that match no filter are reported back, so the website can say what it did not understand.
"""
import re

from charts import DEFAULT_FILTERS

# Each filter value with the words or phrases that select it (lower case). Longer phrases are matched first,
# so "staten island" wins over "island" and "new construction" over "new".
SYNONYMS = {
    "borough": {
        "Bronx": ["the bronx", "bronx", "bx"],
        "Brooklyn": ["brooklyn", "bk", "bklyn"],
        "Manhattan": ["manhattan", "mn", "nyc downtown"],
        "Queens": ["queens", "qn"],
        "Staten Island": ["staten island", "staten", "si"],
    },
    "housing_type": {
        "New Construction": ["new construction", "new buildings", "new building", "newly built", "new build",
                             "construction", "new"],
        "Preservation": ["preservation", "preserved", "preserve", "existing buildings", "renovated"],
    },
    "severity": {
        "Deaths": ["fatalities", "fatality", "fatal", "deaths", "death", "deadly", "killed", "died"],
        "Severe injuries": ["severe injuries", "severe injury", "severely injured", "injuries", "injured", "severe"],
    },
}
YEARS = {2022, 2023, 2024, 2025, 2026}
ALL_WORDS = ["all boroughs", "all years", "all types", "citywide", "all", "nyc", "new york"]
FILLER_WORDS = {"in", "on", "of", "the", "and", "for", "with", "show", "me", "crashes", "crash", "housing",
                "affordable", "homes", "units", "buildings", "streets", "street", "year", "borough"}


def parse_search(text):
    """Return (filters, understood, not_understood).

    filters: dict like DEFAULT_FILTERS; a filter the text doesn't mention stays "All".
    understood: list of "filter: value" strings, for the status line.
    not_understood: words that matched nothing (filler words such as "in" or "crashes" are ignored).
    """
    filters = dict(DEFAULT_FILTERS)
    understood = []
    rest = " " + re.sub(r"[^a-z0-9 ]", " ", (text or "").lower()) + " "

    year_match = re.search(r"\b(20\d\d)\b", rest)
    if year_match and int(year_match.group(1)) in YEARS:
        filters["year"] = int(year_match.group(1))
        understood.append(f"year: {filters['year']}")
        rest = rest.replace(year_match.group(1), " ", 1)

    phrases = [(phrase, key, value) for key, options in SYNONYMS.items()
               for value, words in options.items() for phrase in words]
    for phrase, key, value in sorted(phrases, key=lambda item: -len(item[0])):
        pattern = rf"\b{re.escape(phrase)}\b"
        if filters[key] == "All" and re.search(pattern, rest):
            filters[key] = value
            understood.append(f"{key.replace('_', ' ')}: {value}")
        rest = re.sub(pattern, " ", rest)          # a used (or repeated) phrase is not "not understood"

    for phrase in ALL_WORDS:
        rest = re.sub(rf"\b{re.escape(phrase)}\b", " ", rest)
    not_understood = [word for word in rest.split() if word not in FILLER_WORDS]
    return filters, understood, not_understood
