from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "API de auditorías BEVICIS con Selenium operativa en Fly.io"

@app.route("/auditar", methods=["POST"])
def auditar():
    data = request.get_json()
    empresa = data.get("empresa", "Empresa")
    url = data.get("url")

    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(10)  # Aumentado para permitir carga de scripts dinámicos
    html = driver.page_source.lower()
    driver.quit()

    def contiene_cookiebot(html):
        patrones = [
            "consent.cookiebot.com",
            "window.cookiebot",
            "data-cbid",
            "cdn.cookiebot.com",
            "cookieconsent.show"
        ]
        return any(p in html for p in patrones)

    resultado = {
        "empresa": empresa,
        "Cookiebot": "sí" if contiene_cookiebot(html) else "no",
        "Google Tag Manager": "sí" if "gtm.js" in html or "googletagmanager" in html else "no",
        "Google Analytics": "sí" if "google-analytics" in html or "gtag" in html or "ga.js" in html else "no",
        "Facebook Pixel": "sí" if "facebook.com/tr" in html or "fbq(" in html else "no"
    }
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
