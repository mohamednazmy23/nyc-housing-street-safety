# Homes on Dangerous Streets

**Is New York building its affordable homes on dangerous streets, and what happens to those streets once people move in?**

A data engineering and visualization project that joins NYC's affordable housing production with the crashes that seriously injured or killed someone (SIRTA), January 2022 – June 2026, and tells the story on an interactive website.

**Live website: https://nyc-housing-street-safety.vercel.app**

Data Engineering and Visualization, Winter 2026, German International University · Project Milestone 1

---

## Key findings

- **61%** of the affordable housing projects started in 2023–2025 went to the fifth of ZIP codes that were most dangerous in 2022.
- **51%** of affordable buildings had a serious crash within about one block (100 m) between 2022 and mid-2026.
- Serious harm **did not change** while large affordable buildings went up, after they opened, or as a ZIP's housing grew: the danger was there first.

All twelve research questions, their charts, findings and limitations are in the notebook (section 10) and on the website.

## Data

| Domain | Dataset | Catalog | Link |
|---|---|---|---|
| Housing & Development | Affordable Housing Production by Building (`hg8x-zxpr`) | H2 | [NYC Open Data](https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data) |
| Transportation | Serious Injury Response Tracking & Analysis Program, SIRTA (`xeqp-qz8h`) | T4 | [NYC Open Data](https://data.cityofnewyork.us/Transportation/Serious-Injury-Response-Tracking-Analysis-Program-/xeqp-qz8h/about_data) |

The two datasets are joined at three levels: ZIP code (by year and by month), borough (by year), and exact distance between buildings and crashes (100 m and 250 m). The notebook downloads both datasets in full every time it runs.

## Repository

```
notebooks/nyc_dev_project.ipynb   the full analysis: overview, EDA, cleaning, integration, 12 questions, story
src/charts.py                     the 12 chart functions, shared by the notebook and the website
src/data_loader.py                loads the six processed tables with the right column types
src/search.py                     search mode: turns typed text into filters
app/app.py                        the Dash website (filters, search, Generate Report, story)
app/story.py                      the website's story text
app/assets/style.css              the website's style
data/processed/                   the six joined tables the charts use (exported by notebook section 9.4)
tests/test_search.py              tests for search mode and the Generate Report callback
docs/                             contributions log, decision log, data work notes, requirements tracker,
                                  data dictionary
requirements.txt                  packages for the website (what Vercel installs)
requirements-dev.txt              packages for the notebook and data work (includes requirements.txt)
```

## Setup

You need **Python 3.12** and Git.

```
git clone https://github.com/mohamednazmy23/nyc-housing-street-safety.git
cd nyc-housing-street-safety
py -3.12 -m venv venv              # macOS/Linux: python3.12 -m venv venv
venv\Scripts\activate              # macOS/Linux: source venv/bin/activate
pip install -r requirements-dev.txt
```

On Windows, `requirements-dev.txt` also installs `pip-system-certs`, which fixes the `SSL: CERTIFICATE_VERIFY_FAILED` error some machines get when the notebook downloads the data.

## Run the notebook

Open `notebooks/nyc_dev_project.ipynb` in VS Code or Jupyter, choose the `venv` kernel, and run all cells from the top (**Restart & Run All**). It downloads both datasets, cleans and joins them, writes the six tables to `data/processed/` and draws all charts. It takes a few minutes.

## Run the website locally

```
python app/app.py
```

Then open http://127.0.0.1:8050. Choose filters and press **Generate Report**, or type a query such as `Brooklyn 2022 new buildings` in the search box and press Enter. Stop the server with Ctrl+C.

## Tests

```
python tests/test_search.py
```

Checks the search parser (e.g. "new york" is the city, not "new construction"; a second borough is reported, not dropped) and the website callback (Generate Report uses the dropdowns, Enter applies the search, Reset clears everything).

## Deployment

The website runs on [Vercel](https://vercel.com) (free plan). Vercel finds `app/app.py`, installs `requirements.txt` and serves the Flask app `app` inside it; `.vercelignore` keeps the notebook, docs and tests out of the upload.

```
npm install -g vercel
vercel login
vercel --prod --yes
```

Run the last command again from the repository root after changing the website or the processed data.

## Team and contributions

| Member | Research questions | Contribution |
|---|---|---|
| Mohamed Nazmy | Q1, Q2 | Notebook lead: repository and notebook setup, dataset selection, housing overview and EDA, appendix, Research Questions doc, shared chart contract and data dictionary; reviewed every pull request |
| Mostafa Ayman | Q5, Q6 | Story: website story text, notebook introduction and story summary, README |
| Mostafa Alaa | Q9, Q10 | Housing pre-integration cleaning |
| Ali Issa | Q3, Q4 | SIRTA overview, EDA and pre-integration cleaning |
| Moustafa Maged | Q11, Q12 | Integration, post-integration cleaning, exported tables and data loader |
| Baraa Tantawy | Q7, Q8 | Website (Dash app, filters, search mode, Generate Report) and its tests, Vercel deployment, Python environment, Story doc and Team Tasks plan, documentation logs |

Every step is logged in `docs/contributions_log.md` and `docs/decision_log.md`; the AI prompts used are in notebook section 12.3.
