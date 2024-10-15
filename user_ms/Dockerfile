FROM python:3.11-bullseye

WORKDIR /usr/src/app

# Copy the requirements file first to leverage Docker cache
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Specify the command to run the application
CMD ["python", "app.py"]