from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source.lower()
    driver.quit()

    resultado = {
        "empresa": empresa,
        "Cookiebot": "sí" if "consent.cookiebot.com" in html else "no",
        "Google Tag Manager": "sí" if "gtm.js" in html or "googletagmanager" in html else "no",
        "Google Analytics": "sí" if "google-analytics" in html or "gtag" in html or "ga.js" in html else "no",
        "Facebook Pixel": "sí" if "facebook.com/tr" in html or "fbq(" in html else "no"
    }
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
