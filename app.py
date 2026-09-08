"""Flask entry point for the laundry dashboard."""
from flask import Flask, jsonify, render_template

from laundry import LaundryClient, LaundryUnavailable

app = Flask(__name__)
laundry = LaundryClient()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/status")
def status():
    try:
        response = jsonify(laundry.get_machines())
    except LaundryUnavailable:
        response = jsonify(error="Unable to refresh laundry status. Please try again shortly.")
        response.status_code = 503
    response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == "__main__":
    app.run(port=5000)
