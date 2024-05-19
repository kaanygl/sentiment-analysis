from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    session,
    redirect,
    url_for,
    render_template,
)
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import base64

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.urandom(24)


def get_db_connection():
    conn = sqlite3.connect("election.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/get-data")
def get_data():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analysis_datas")
    rows = cursor.fetchall()
    conn.close()

    data = {}
    for row in rows:
        choice_name = row["Topic_Analysis"]
        xValues = [row["Side_A"], row["Side_B"], row["Side_C"]]
        yValues = [
            row["Percentage_of_A"],
            row["Percentage_of_B"],
            row["Percentage_of_C"],
        ]

        filtered_xValues = []
        filtered_yValues = []
        for i in range(len(xValues)):
            if xValues[i]:
                filtered_xValues.append(xValues[i])
                filtered_yValues.append(yValues[i])

        data[choice_name] = {"xValues": filtered_xValues, "yValues": filtered_yValues}

    return jsonify(data)


@app.route("/")
def index():
    user_id = session.get("user_id")
    user = None
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
    return render_template("mainpage.html", user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match", 400

        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=16
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        session["user_id"] = user_id
        return redirect(url_for("index"))

    return render_template("regform.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        else:
            return "Invalid email or password", 400

    return render_template("regform.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))


@app.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT description, image FROM images WHERE id IN (8, 9, 10, 11, 12)"
    )
    images = cursor.fetchall()
    conn.close()

    encoded_images = []
    for image in images:
        formatted_description = image["description"].replace("_", " ").title()
        encoded_image = base64.b64encode(image["image"]).decode("utf-8")
        encoded_images.append(
            {"description": formatted_description, "image": encoded_image}
        )

    user_id = session.get("user_id")
    user = None
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

    return render_template("reports.html", images=encoded_images, user=user)


if __name__ == "__main__":
    app.run(debug=True)
