from flask import Flask, render_template, request
import csv
from datetime import datetime
import os

app = Flask(__name__)

CSV_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "donations.csv"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/donate", methods=["POST"])
def donate():

    name = request.form["name"]
    amount = request.form["amount"]
    utr = request.form["utr"]

    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    # CSV file nahi hai to header ke saath create karo
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Amount", "UTR", "Date"])

    # Ensure new donation starts on a new line
    with open(CSV_FILE, "rb+") as file:
        file.seek(0, os.SEEK_END)

        if file.tell() > 0:
            file.seek(-1, os.SEEK_END)
            last_character = file.read(1)

            if last_character != b"\n":
                file.write(b"\n")

    # Save donation
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([name, amount, utr, date])

    return render_template(
        "success.html",
        name=name,
        amount=amount,
        utr=utr
    )


@app.route("/records")
def records():

    donations = []
    total = 0

    if os.path.exists(CSV_FILE):

        with open(CSV_FILE, "r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row.get("Name") and row.get("Amount"):

                    donations.append(row)

                    try:
                        total += float(row["Amount"])
                    except (ValueError, TypeError):
                        pass

    return render_template(
        "records.html",
        donations=donations,
        total=total
    )


if __name__ == "__main__":
    app.run(debug=True)