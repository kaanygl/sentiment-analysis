from flask import Flask, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_url_path="")


def get_db_connection():
    conn = sqlite3.connect("election.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/get-data")
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analysis_datas")  # Fetch all columns
    rows = cursor.fetchall()
    conn.close()

    data = {}
    for row in rows:
        choice_name = row["Topic_Analysis"]  # Column for choice names
        xValues = [row["Side_A"], row["Side_B"], row["Side_C"]]
        yValues = [
            row["Percentage_of_A"],
            row["Percentage_of_B"],
            row["Percentage_of_C"],
        ]

        # Filter out empty xValues and their corresponding yValues
        filtered_xValues = []
        filtered_yValues = []
        for i in range(len(xValues)):
            if xValues[i]:  # Check if xValue is not empty
                filtered_xValues.append(xValues[i])
                filtered_yValues.append(yValues[i])

        data[choice_name] = {"xValues": filtered_xValues, "yValues": filtered_yValues}

    return jsonify(data)


@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory(os.getcwd(), path)


if __name__ == "__main__":
    app.run(debug=True)
