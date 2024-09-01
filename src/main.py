import flask_cors
from flask import Flask, jsonify

app = Flask(__name__)
flask_cors.CORS(app)

from src.webscrapper import WebScraper

scraper = WebScraper()


@app.route("/api/cedula/<id>", methods=["GET"])
def get_data(id):
    return jsonify(scraper.get_data(id))


if __name__ == "__main__":
    app.run()
