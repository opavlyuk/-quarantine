# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /quarantine

# Copy the current directory contents into the container at /app
COPY . /quarantine

# Copy config
COPY ./config.yml /config.yml

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD celery worker -A src.celery_app.application -l DEBUG  --logfile="/var/log/quarantine/%n%I.log" -D  && python src/watcher.py

