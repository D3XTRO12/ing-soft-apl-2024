FROM python:3.11-bullseye

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/user-ms/.local/bin


RUN useradd --create-home --home-dir /home/user-ms user-ms

WORKDIR /home/user-ms

USER user-ms
RUN mkdir app

COPY ./app ./app
COPY ./app.py .

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]