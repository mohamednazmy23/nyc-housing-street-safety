"""Search mode: turn a typed query into the same filters the dropdowns set.

Example: "Brooklyn 2022 new buildings" -> borough Brooklyn, year 2022, housing type New Construction.

Rules (tests: tests/test_search.py):
- Only filters the text mentions are returned; the website keeps the other dropdowns as they are.
- "citywide", "all boroughs", "all years", "all types", "all harm" set that filter back to "All".
- One value per filter: the first one in the text wins; a later, different one is reported as ignored.
- Anything not understood (unknown words, years outside 2022-2026) is reported, never silently dropped.
"""
import re

from charts import FILTER_OPTIONS

# Words or phrases (lower case) for each filter value. The values themselves come from charts.FILTER_OPTIONS,
# so the search can never offer a value the dropdowns don't have (checked below, at import).
SYNONYMS = {
    "borough": {
        "Bronx": ["the bronx", "bronx", "bx"],
        "Brooklyn": ["brooklyn", "bklyn", "bk"],
        "Manhattan": ["manhattan", "mn"],
        "Queens": ["queens", "qn"],
        "Staten Island": ["staten island", "staten", "si"],
        "All": ["all boroughs", "every borough", "citywide", "city wide", "whole city", "new york city",
                "new york", "nyc"],
    },
    "year": {
        "All": ["all years", "every year", "all time"],
    },
    "housing_type": {
        "New Construction": ["new construction", "new buildings", "new building", "newly built", "new build",
                             "construction", "new"],
        "Preservation": ["preservation", "preserved", "preserve", "existing buildings", "renovated"],
        "All": ["all types", "all housing types", "all housing", "every type"],
    },
    "severity": {
        "Deaths": ["fatalities", "fatality", "fatal", "deaths", "death", "deadly", "killed", "died"],
        "Severe injuries": ["severe injuries", "severe injury", "severely injured", "injuries", "injured", "severe"],
        "All": ["all harm", "serious harm", "all crashes", "all severities"],
    },
}
LABELS = {"borough": "borough", "year": "year", "housing_type": "housing type", "severity": "crash measure"}
FILLER_WORDS = {"in", "on", "of", "the", "and", "or", "for", "with", "show", "me", "crashes", "crash", "housing",
                "affordable", "homes", "units", "buildings", "streets", "street", "year", "borough", "all", "a",
                "to", "from", "near", "at"}

for _key, _values in SYNONYMS.items():          # the search may only use values the dropdowns offer
    assert set(_values) <= set(FILTER_OPTIONS[_key]), (_key, set(_values) - set(FILTER_OPTIONS[_key]))
YEARS = [value for value in FILTER_OPTIONS["year"] if value != "All"]


def _find_mentions(text):
    """Every filter phrase and year in the text, with its position. Longer phrases are matched first and
    blanked out, so "new york" is never read as "new", and "staten island" never as "island"."""
    rest, mentions = text, []
    phrases = [(phrase, key, value) for key, options in SYNONYMS.items()
               for value, words in options.items() for phrase in words]
    for phrase, key, value in sorted(phrases, key=lambda item: -len(item[0])):
        for match in re.finditer(rf"\b{re.escape(phrase)}\b", rest):
            mentions.append((match.start(), key, value, phrase))
        rest = re.sub(rf"\b{re.escape(phrase)}\b", lambda m: " " * len(m.group()), rest)   # keep positions
    for match in re.finditer(r"\b(?:19|20)\d\d\b", rest):
        year = int(match.group())
        mentions.append((match.start(), "year", year if year in YEARS else None, match.group()))
        rest = rest[:match.start()] + " " * (match.end() - match.start()) + rest[match.end():]
    return sorted(mentions), rest


def parse_search(text):
    """Return (chosen, understood, ignored).

    chosen: dict with only the filters the text mentions, e.g. {"borough": "Brooklyn", "year": 2022}
            (a value may be "All", e.g. for "citywide").
    understood: "filter: value" strings, for the status line.
    ignored: words or values the search did not use, each with a short reason where useful.
    """
    clean = " " + re.sub(r"[^a-z0-9 ]", " ", (text or "").lower()) + " "
    mentions, rest = _find_mentions(clean)
    chosen, understood, ignored = {}, [], []
    for _, key, value, phrase in mentions:
        if value is None:
            ignored.append(f"{phrase} (no data for that year; years are {YEARS[0]}–{YEARS[-1]})")
        elif key not in chosen:
            chosen[key] = value
            understood.append(f"{LABELS[key]}: {value}")
        elif chosen[key] != value:
            ignored.append(f"{phrase} (one {LABELS[key]} at a time; kept {chosen[key]})")
    ignored += [word for word in rest.split() if word not in FILLER_WORDS]
    return chosen, understood, ignored
