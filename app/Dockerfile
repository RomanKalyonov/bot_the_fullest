# base image for tgbot
FROM python:3.8.6

# Set work dir
WORKDIR ./app/

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . .
