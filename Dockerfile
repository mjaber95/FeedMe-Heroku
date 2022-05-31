FROM python:3.8.6-buster

COPY FeedMe /FeedMe
COPY best.pt /best.pt
COPY raw_data /raw_data
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080
CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
