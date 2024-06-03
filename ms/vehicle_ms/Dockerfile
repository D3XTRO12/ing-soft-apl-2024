FROM python:3.11-bullseye

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/vehicle-ms/.local/bin

RUN useradd --create-home --home-dir /home/vehicle-ms vehicle-ms

WORKDIR /home/vehicle-ms

USER vehicle-ms
RUN mkdir app

COPY ./app ./app
COPY ./app.py .

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD [ "python", "./app.py" ]
