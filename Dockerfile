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
CMD mkdir -p /var/log/quarantine && chown nobody /var/log/quarantine && mkdir -p /var/run/quarantine && chown nobody /var/run/quarantine && chmod -R 777 /var/log/quarantine && chmod -R 777 /var/run/quarantine && chmod -R 777 /results && celery worker -A src.celery_app.application -l DEBUG --uid=nobody --logfile="/var/log/quarantine/%n%I.log" --pidfile="/var/run/quarantine/%n.pid" -D  && python src/watcher.py

