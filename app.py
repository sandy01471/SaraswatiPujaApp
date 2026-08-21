from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)

# Secret key for admin login session
app.secret_key = "saraswati-puja-admin-secret-2026"

# Admin login
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Saraswati@9508#Puja2026!"

# Temporary storage for demo
donations = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/donate", methods=["POST"])
def donate():

    name = request.form.get("name", "").strip()
    amount = request.form.get("amount", "").strip()
    utr = request.form.get("utr", "").strip()

    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    donation = {
        "Name": name,
        "Amount": amount,
        "UTR": utr,
        "Date": date
    }

    donations.append(donation)

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

    # Only logged-in admin can see records
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    total = 0

    for donation in donations:
        try:
            total += float(donation["Amount"])
        except (ValueError, TypeError):
            pass

    return render_template(
        "records.html",
        donations=donations,
        total=total
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
