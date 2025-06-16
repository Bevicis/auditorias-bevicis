FROM python:3.10-slim

RUN apt-get update && apt-get install -y     wget unzip gnupg curl     chromium-driver chromium

ENV CHROME_BIN=/usr/bin/chromium

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "app_selenium.py"]
