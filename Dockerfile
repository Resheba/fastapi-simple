FROM python:3.11-slim

# RUN mkdir /site

# WORKDIR /site

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
