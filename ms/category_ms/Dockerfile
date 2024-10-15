FROM python:3.11-bullseye

RUN useradd --create-home --home-dir /home/category_ms category_ms

WORKDIR /home/category_ms

RUN mkdir -p /home/category_ms/app

RUN chown -R category_ms:category_ms /home/category_ms/app

USER category_ms

COPY ./app ./app

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/category_ms/.local/bin

COPY ./app.py .
COPY requirements.txt .

ADD requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5003

CMD [ "python", "./app.py" ]
