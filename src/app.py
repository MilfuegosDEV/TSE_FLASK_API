from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve


class WebScrapper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")  # open Browser in maximized mode
        options.add_argument("disable-infobars")  # disabling infobars
        options.add_argument("--log-level=1")  # disabling logs
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")  # applicable to windows os only
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--headless")

        # to supress the error messages/logs
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)

    def get_data(self, x):
        try:
            self.driver.get(
                "https://servicioselectorales.tse.go.cr/chc/consulta_cedula.aspx"
            )
            wait = WebDriverWait(self.driver, 1)
            wait.until(lambda driver: driver.find_element(By.NAME, "txtcedula"))
            search_box = self.driver.find_element("name", "txtcedula")
            search_box.send_keys(x)
            search_box.send_keys(Keys.RETURN)
            wait.until(
                lambda driver: driver.find_element(By.ID, "lblcedula")
                and driver.find_element(By.ID, "lblnombrecompleto")
                and driver.find_element(By.ID, "lblfechaNacimiento")
            )

            html = self.driver.page_source
            lblcedula = (
                BeautifulSoup(html, "html.parser")
                .find("span", {"id": "lblcedula"})
                .text
            )
            lblname = (
                BeautifulSoup(html, "html.parser")
                .find("span", {"id": "lblnombrecompleto"})
                .text
            )
            lblnacimiento = (
                BeautifulSoup(html, "html.parser")
                .find("span", {"id": "lblfechaNacimiento"})
                .text
            )

            response = {
                "cedula": lblcedula,
                "nombre": lblname,
                "nacimiento": lblnacimiento,
            }
            return response
        except:
            return {
                "cedula": x,
                "nombre": "No encontrado",
                "nacimiento": "No encontrado",
            }

    def close(self):
        self.driver.quit()


app = Flask(__name__)
scrapper = WebScrapper()
CORS(app)
app.config["ENV"] = "production"


@app.route("/", methods=["GET"])
def home():
    return "<h1>Flask API</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route("/api", methods=["GET"])
def api():
    return jsonify({"message": "Welcome to the API", "status": 200, "data": []})


@app.route("/api/cedula/<id>", methods=["GET"])
def cedula(id):
    try:
        return jsonify(scrapper.get_data(id))
    except:
        return jsonify({"message": "Error", "status": 500, "data": []})


if __name__ == "__main__":
    mode = "prod"

    if mode == "dev":
        app.run(debug=True)
    else:
        serve(app, host="3.125.183.140", port=8080)
