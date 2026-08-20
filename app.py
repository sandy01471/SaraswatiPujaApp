from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

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


@app.route("/records")
def records():

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


if __name__ == "__main__":
    app.run(debug=True)
