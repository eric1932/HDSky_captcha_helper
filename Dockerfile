FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY ./app /app

RUN apt-get update \
    && apt-get install -y python3-opencv \
    && pip3 install -r /app/requirements.txt
