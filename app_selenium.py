from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "API de auditorías BEVICIS con Selenium avanzada (JS DOM) en Fly.io"

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
    time.sleep(8)

    # Ejecutamos JavaScript para detectar scripts cargados dinámicamente
    scripts = driver.execute_script("""
        return Array.from(document.scripts).map(s => s.src || '');
    """)
    html = driver.page_source.lower()
    driver.quit()

    resultado = {
        "empresa": empresa,
        "Cookiebot": "sí" if any("cookiebot" in s for s in scripts) else "no",
        "Google Tag Manager": "sí" if any("gtm.js" in s or "googletagmanager" in s for s in scripts) else "no",
        "Google Analytics": "sí" if any("ga.js" in s or "gtag/js" in s or "google-analytics" in s for s in scripts) else "no",
        "Facebook Pixel": "sí" if "facebook.com/tr" in html or "fbq(" in html else "no"
    }

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
