"""Vercel entry point: serves the Dash website (app/app.py) as one Python serverless function.

Vercel looks for a WSGI callable named `app` here; vercel.json sends every URL to this function, so Dash's own
routes (the page, its scripts and the Generate Report callback) all reach it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

from app import server as app  # noqa: E402,F401  (app/app.py; `server` is Dash's Flask app)
