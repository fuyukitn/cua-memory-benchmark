from flask import Blueprint, render_template, redirect, url_for, session
import re

spreadsheet_bp = Blueprint("spreadsheet", __name__, url_prefix="/spreadsheet")

# Helper to generate spreadsheet column names up to n columns
def spreadsheet_colnames(n):
    names = []
    i = 1
    while len(names) < n:
        name = ''
        x = i
        while x > 0:
            x, r = divmod(x-1, 26)
            name = chr(65 + r) + name
        names.append(name)
        i += 1
    return names

COLS = spreadsheet_colnames(100)
ROWS = list(range(1, 101))

def get_sheet():
    sheet = session.get("sheet")
    if sheet is None:
        sheet = {f"{col}{row}": "" for col in COLS for row in ROWS}
    return sheet

@spreadsheet_bp.route("/")
def index():
    sheet = get_sheet()
    return render_template("spreadsheet/index.html", cols=COLS, rows=ROWS, sheet=sheet)

@spreadsheet_bp.route("/clear")
def clear():
    session.pop("sheet", None)
    return redirect(url_for("spreadsheet.index"))