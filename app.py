from flask import Flask, render_template, request, redirect, url_for
import pickle, os

app = Flask(__name__)
FILENAME = "SRB.dat"

# -------------------- Utility Functions --------------------
def load_records():
    records = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "rb") as f:
            try:
                while True:
                    records.append(pickle.load(f))
            except EOFError:
                pass
    return records

def save_records(records):
    with open(FILENAME, "wb") as f:
        for rec in records:
            pickle.dump(rec, f)

# -------------------- Landing Page --------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------- User Options --------------------
@app.route("/user_options")
def user_options():
    return render_template("user_options.html")

# -------------------- User Routes --------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    records = load_records()
    if not records:
        return render_template("error.html", message="No accounts exist. Please sign up first.")
    last5 = int(request.form["acc_no"])
    for r in records:
        acc_last5 = int(str(r[0])[-5:])
        if acc_last5 == last5:
            return render_template("dashboard.html", user=r)
    return render_template("error.html", message="No account found with that number.")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    records = load_records()
    acc_no = 19770800000001 if len(records) == 0 else max(r[0] for r in records)+1
    name = request.form["name"]
    typ = request.form["acc_type"]
    amt = int(request.form["amount"])

    if typ == "Savings" and amt < 500:
        return render_template("error.html", message="Minimum amount for Savings Account is 500.")
    elif typ == "Current" and amt < 1000:
        return render_template("error.html", message="Minimum amount for Current Account is 1000.")
    elif typ not in ["Savings","Current"]:
        return render_template("error.html", message="Invalid account type.")

    rec = [acc_no, name, amt, typ]
    with open(FILENAME, "ab") as f:
        pickle.dump(rec, f)
    return render_template("success.html", message=f"Account created! Account No.: {acc_no}")

@app.route("/deposit/<int:acc_no>", methods=["GET", "POST"])
def deposit(acc_no):
    records = load_records()
    for r in records:
        if r[0] == acc_no:
            if request.method == "POST":
                amt = int(request.form["amount"])
                r[2] += amt
                save_records(records)
                return render_template("success.html", message=f"Deposit successful! New Balance: {r[2]}")
            return render_template("deposit.html", acc_no=acc_no)
    return render_template("error.html", message="Account not found.")

@app.route("/withdraw/<int:acc_no>", methods=["GET", "POST"])
def withdraw(acc_no):
    records = load_records()
    for r in records:
        if r[0] == acc_no:
            if request.method == "POST":
                amt = int(request.form["amount"])
                if amt <= r[2]:
                    r[2] -= amt
                    save_records(records)
                    return render_template("success.html", message=f"Withdrawal successful! New Balance: {r[2]}")
                else:
                    return render_template("error.html", message="Not enough balance.")
            return render_template("withdraw.html", acc_no=acc_no)
    return render_template("error.html", message="Account not found.")

# -------------------- Admin Routes --------------------
@app.route("/admin_login_page")
def admin_login_page():
    return render_template("admin_login_page.html")

@app.route("/admin_dashboard", methods=["POST"])
def admin_dashboard_post():
    password = request.form.get("password")
    if password == "admin123":  # Change admin password here
        records = load_records()
        return render_template("admin_dashboard.html", records=records)
    else:
        return render_template("error.html", message="Incorrect Admin Password.")


@app.route("/update/<int:acc_no>", methods=["GET", "POST"])
def update_account(acc_no):
    records = load_records()
    for r in records:
        if r[0] == acc_no:
            if request.method == "POST":
                new_balance = int(request.form["new_balance"])
                r[2] = new_balance
                save_records(records)
                return render_template("success.html", message=f"Account {acc_no} updated! New Balance: {r[2]}")
            return render_template("update_account.html", user=r)
    return render_template("error.html", message="Account not found.")

@app.route("/delete/<int:acc_no>", methods=["POST"])
def delete_account(acc_no):
    records = load_records()
    records = [r for r in records if r[0] != acc_no]
    save_records(records)
    return render_template("success.html", message=f"Account {acc_no} deleted successfully.")

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


