from flask import Flask, render_template, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'secret-key'

# Helper to generate Excel column names up to n columns
def excel_colnames(n):
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

COLS = excel_colnames(100)  # 100 columns: A, B, ..., CV
ROWS = list(range(1, 101))  # 1-100


def get_sheet():
    """Return current sheet from session or initialize new sheet dict."""
    sheet = session.get("sheet")
    if sheet is None:
        # initialize empty values
        sheet = {f"{col}{row}": "" for col in COLS for row in ROWS}
    return sheet


@app.route("/")
def index():
    sheet = get_sheet()
    return render_template("index.html", cols=COLS, rows=ROWS, sheet=sheet)


@app.route("/clear")
def clear():
    session.pop("sheet", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True) 