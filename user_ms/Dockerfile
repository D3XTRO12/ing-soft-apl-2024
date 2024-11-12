FROM python:3.11-bullseye

WORKDIR /usr/src/app

# Copy the requirements file from correct location
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire user_ms directory
COPY  / .

EXPOSE 5000

CMD ["python", "app.py"]