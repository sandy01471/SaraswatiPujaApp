from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os
import json
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Secret key for admin login session
app.secret_key = "saraswati-puja-admin-secret-2026"

# Admin login
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Saraswati@9508#Puja2026!"


# ---------------- GOOGLE SHEETS ----------------

def get_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    credentials_info = {
        "type": "service_account",
        "project_id": os.environ["GOOGLE_PROJECT_ID"],
        "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": os.environ["GOOGLE_SERVICE_ACCOUNT_EMAIL"],
        "token_uri": "https://oauth2.googleapis.com/token"
    }

    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        os.environ["GOOGLE_SHEET_ID"]
    )

    return spreadsheet.sheet1


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- DONATION ----------------

@app.route("/donate", methods=["POST"])
def donate():

    name = request.form.get("name", "").strip()
    amount = request.form.get("amount", "").strip()
    utr = request.form.get("utr", "").strip()

    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    # Save donation to Google Sheet
    sheet = get_sheet()

    sheet.append_row([
        name,
        amount,
        utr,
        date
    ])

    return render_template(
        "success.html",
        name=name,
        amount=amount,
        utr=utr
    )


# ---------------- ADMIN LOGIN ----------------

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("records"))

        return render_template(
            "admin.html",
            error="Invalid username or password"
        )

    return render_template("admin.html")


# ---------------- ADMIN RECORDS ----------------

@app.route("/records")
def records():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    sheet = get_sheet()

    rows = sheet.get_all_records()

    total = 0

    for donation in rows:
        try:
            total += float(donation["Amount"])
        except (ValueError, TypeError, KeyError):
            pass

    return render_template(
        "records.html",
        donations=rows,
        total=total
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
