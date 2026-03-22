from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# existing backend (auth)
BACKEND = "http://localhost:3000"

# ML backend
ML_BACKEND = "http://127.0.0.1:5000"


@app.route("/")
def home():
    return redirect("/login")


# ---------- Signup ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")

        r = requests.post(
            f"{BACKEND}/signup",
            json={"email": email, "password": password}
        )

        if r.status_code == 200:
            return redirect("/account-created")

        return render_template("signup.html", error="User already exists")

    return render_template("signup.html")


# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        r = requests.post(
            f"{BACKEND}/login",
            json={"email": email, "password": password}
        )

        if r.status_code == 200:
            return redirect("/welcome")
        else:
            return "Login failed"

    return render_template("login.html")


# ---------- Account Created ----------
@app.route("/account-created")
def account_created():
    return render_template("account_created.html")


# ---------- Welcome Page (ADD ML HERE) ----------
@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    result = None

    if request.method == "POST":
        url = request.form.get("url")

        try:
            response = requests.post(
                f"{ML_BACKEND}/predict",
                json={"url": url},
                timeout=5
            )

            result = response.json()

        except Exception as e:
            result = {"error": str(e)}

    return render_template("welcome.html", result=result)


# ---------- RUN ----------
app.run(debug=True, port=5001)