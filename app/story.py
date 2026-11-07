"""Story text for the website (Story doc: 5 acts, What? / So what? / Now what?).

The text describes the DEFAULT view (all filters "All"); the charts update with the filters, the text stays fixed
(Story doc rule). Every number comes from the notebook (section 10) and must be updated there first.
"""

TITLE = "Homes on Dangerous Streets"
FINDING_TITLE = "61% of New York's new affordable housing projects go to its most dangerous ZIP codes"
SUBTITLE = "How New York's affordable-housing construction lines up with serious crashes, Jan 2022 to Jun 2026"
QUESTION = ("Is New York building its affordable homes on dangerous streets, and what happens to those streets "
            "once people move in?")
HOOK = ("Since January 2022, New York has completed or preserved {units:,} affordable homes. In the same months, "
        "{crashes:,} crashes left someone seriously injured or dead, and {deaths:,} people were killed. "
        "This page follows those homes onto the streets around them.")

# One block per act: title, the charts in the order shown, a one-line takeaway per chart, and the act panel
ACTS = [
    {
        "id": "act1", "title": "Act 1 · The big picture",
        "intro": "Do housing and danger line up across the city: borough by borough, and ZIP by ZIP?",
        "charts": [
            ("q12", "Year by year, borough by borough",
             "Housing output swings from year to year while serious harm hardly moves. No borough moved to more "
             "affordable homes and less harm from 2022 to 2025. Press ▶ to play the years."),
            ("q1", "ZIP by ZIP",
             "The quarter of ZIPs that got the most new affordable units (88% of them) also had 41% of the serious "
             "harm (Spearman ρ = 0.67). Busy ZIPs have more of both: this shows overlap, not cause."),
        ],
        "panel": {"What?": "New affordable housing and serious crashes overlap strongly at ZIP level, but they don't "
                           "move together from year to year.",
                  "So what?": "New affordable homes are going up in the busiest, most dangerous parts of the city.",
                  "Now what?": "Housing plans and street-safety plans should be made together for the same ZIPs."},
    },
    {
        "id": "act2", "title": "Act 2 · Where",
        "intro": "Which streets and doorsteps, and which kinds of housing?",
        "charts": [
            ("q8", "The streets",
             "The worst corridors near affordable housing are big arterials (Atlantic Avenue, Eastern Parkway, Jerome "
             "Avenue, the Grand Concourse), but the top 10 hold only 9.6% of the serious harm near housing: it is "
             "spread over 1,448 streets."),
            ("q11", "The doorstep",
             "51% of the affordable buildings completed by June 2026 had a serious crash within 100 m, about one "
             "block: 63% in Manhattan, 29% on Staten Island."),
            ("q9", "The kind of housing",
             "How much affordable housing a ZIP gets tracks its serious harm (ρ = 0.40). The kind of housing (income "
             "tier, bedroom size, rental or ownership) barely does."),
        ],
        "panel": {"What?": "Half of all affordable buildings have serious danger within a block. The worst streets "
                           "are wide arterials, but most of the harm is spread over hundreds of ordinary streets.",
                  "So what?": "Fixing a handful of avenues will not protect most residents of new affordable housing.",
                  "Now what?": "Review the streets around every new affordable building, starting with the top "
                               "corridors: Atlantic Avenue, Eastern Parkway, Jerome Avenue and the Grand Concourse."},
    },
    {
        "id": "act3", "title": "Act 3 · A building's life",
        "intro": "Before, during and after: does the danger come first, or does it follow the housing?",
        "charts": [
            ("q10", "Before: where projects are placed",
             "61% of the affordable projects started in 2023–2025 went to the fifth of ZIPs that were most dangerous "
             "in 2022: more concentrated than the danger itself (44.5% of 2022 harm) or the city's older affordable "
             "housing (49.6%)."),
            ("q6", "During: construction",
             "Streets were no more dangerous while a large affordable building was going up: 1.46 vs 1.46 serious "
             "harm per ZIP per month."),
            ("q2", "After: the year after opening",
             "Serious harm in a ZIP barely changed in the 12 months after a New Construction building opened, for "
             "any size (large buildings: −0.03 per month; ZIPs with no completion: +0.07)."),
            ("q7", "Over the years: growth and change",
             "ZIPs whose new affordable housing grew fastest saw serious harm change no differently from the rest "
             "(ρ = −0.02 across 87 ZIPs)."),
        ],
        "panel": {"What?": "New projects go mostly to ZIPs that were already dangerous, and harm does not change "
                           "during construction, after opening, or as housing grows.",
                  "So what?": "The danger comes first. It is about where housing is placed, not about what the new "
                              "housing does to the street.",
                  "Now what?": "Flag new affordable sites in the most dangerous fifth of ZIPs early, and plan street "
                               "fixes before residents move in."},
    },
    {
        "id": "act4", "title": "Act 4 · The nature of the danger",
        "intro": "When it happens, how deadly it is, and whether it gets fixed.",
        "charts": [
            ("q3", "When",
             "In the ZIPs with the most affordable housing, a bit more of the serious harm happens late at night "
             "(25.4% vs 22.6% between 22:00 and 06:00) and at weekends."),
            ("q5", "How deadly",
             "On city streets, a serious crash is about as deadly in the ZIPs with the most new housing (5.6 deaths "
             "per 100) as elsewhere (6.4). Highway crashes are twice as deadly."),
            ("q4", "Fixed or not",
             "The share of serious harm at known repeat-danger spots doesn't fall in any group, and it is highest "
             "every year where the most housing is built (8.7% over four years)."),
        ],
        "panel": {"What?": "Danger near new housing is a little more likely at night, about as deadly as elsewhere, "
                           "and keeps returning to the same spots.",
                  "So what?": "Known danger spots stay dangerous exactly where thousands of new residents arrive.",
                  "Now what?": "Put repeat-danger spots near new affordable housing first in line for redesign, and "
                               "look at night-time speed and lighting there."},
    },
]

HEADLINES = [
    ("61%", "of the affordable projects started in 2023–2025 went to the fifth of ZIP codes that were most "
            "dangerous in 2022."),
    ("51%", "of affordable buildings had a serious crash within about one block (100 m) between 2022 and mid-2026."),
    ("No change", "in serious harm while large buildings went up or after they opened: the danger was there first."),
]

LIMITS = [
    "**Correlation is not causation.** Every chart shows where housing and danger meet, not that one causes the other.",
    "**Totals, not rates.** We use only our two datasets, so there is no population, traffic or street length; busy "
    "places have more of everything.",
    "**ZIP codes are large.** A ZIP can hide very different streets; Q8 and Q11 use exact distances instead.",
    "**Some locations are missing or estimated.** 1,958 confidential buildings have no location; 3,817 crash ZIPs "
    "were filled from the nearest point, about 93% correctly; 2,441 crashes have no coordinates.",
    "**2026 is half a year** (January to June), so yearly comparisons use 2022–2025.",
    "**Repeat-danger information is missing** for part of 2023–2024 crashes.",
    "**Distances ignore timing.** A 2022 crash next to a building finished in 2026 counts as near housing.",
]

IMPACT = [
    ("NYC DOT / Vision Zero", "Q1, Q8, Q11",
     "Review the streets within 250 m of new affordable buildings, starting with the top corridors and repeat-danger spots."),
    ("HPD (Housing Preservation & Development)", "Q2, Q6, Q10",
     "Flag new projects in the most dangerous ZIPs at approval and coordinate street work with DOT before move-in."),
    ("City Council members", "Q4, Q10",
     "Fund redesigns of repeat-danger spots in districts that receive the most new affordable housing."),
    ("Housing and street-safety advocates", "Q11",
     "Use the doorstep shares by borough to ask for safety reviews around affordable buildings."),
    ("Residents", "Q3, Q8",
     "Know the most dangerous streets near your building, and that late nights carry a little more of the risk."),
]

DATASETS = [
    ("Affordable Housing Production by Building (H2, hg8x-zxpr)",
     "https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data"),
    ("Serious Injury Response Tracking & Analysis Program, SIRTA (T4, xeqp-qz8h)",
     "https://data.cityofnewyork.us/Transportation/Serious-Injury-Response-Tracking-Analysis-Program-/xeqp-qz8h/about_data"),
]
METHOD = ("Both datasets were cleaned (missing values, outliers, formats, duplicates), then joined at three levels: ZIP "
          "code (by year and month), borough (by year), and exact distance between buildings and crashes (100 m and "
          "250 m). Missing crash ZIP codes were filled from the nearest located crash or building. Every step, number "
          "and decision is documented in the project notebook in the GitHub repository.")
