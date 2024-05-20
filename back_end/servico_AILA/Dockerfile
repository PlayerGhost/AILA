# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Avoids Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install supervisord
RUN apt-get update

# Set up a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Set the working directory to /app
WORKDIR /app

# Install pip requirements for both services
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Create a non-root user and give access to the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN mkdir /app/logs && chown -R appuser:appuser /app/logs
USER appuser

CMD ["python", "app.py"]