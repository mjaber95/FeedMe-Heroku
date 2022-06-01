FROM python:3.8.6-buster
WORKDIR /app
COPY FeedMe /FeedMe
COPY best.pt /best.pt
COPY raw_data /raw_data
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 8501
COPY . /app
ENTRYPOINT [ "streamlit", "run" ]
CMD ["app.py"]
