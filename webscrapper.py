from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import asyncio


class WebScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")  # open Browser in maximized mode
        options.add_argument("disable-infobars")  # disabling infobars
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
            wait = WebDriverWait(self.driver, 10)
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
            print(response)
            return response
        except:
            return {
                "cedula": x,
                "nombre": "No encontrado",
                "nacimiento": "No encontrado",
            }

    def close(self):
        self.driver.quit()


# def get_data(x):
#     driver = webdriver.Chrome()
#     driver.get("https://servicioselectorales.tse.go.cr/chc/consulta_cedula.aspx")
#     search_box = driver.find_element("name", "txtcedula")
#     search_box.send_keys(x)  # retrieve response
#     search_box.send_keys(Keys.RETURN)
#     html = driver.page_source
#     lblcedula = (
#         BeautifulSoup(html, "html.parser").find("span", {"id": "lblcedula"}).text
#     )
#     lblname = (
#         BeautifulSoup(html, "html.parser")
#         .find("span", {"id": "lblnombrecompleto"})
#         .text
#     )
#     lblnacimiento = (
#         BeautifulSoup(html, "html.parser")
#         .find("span", {"id": "lblfechaNacimiento"})
#         .text
#     )
#     return {
#         "cedula": lblcedula,
#         "nombre": lblname,
#         "nacimiento": lblnacimiento,
#     }
