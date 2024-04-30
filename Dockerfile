# Start from Python slim image
FROM python:3.8-slim

# Install MQTT library for Python
RUN pip install paho-mqtt

# Install necessary system utilities
RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    telnet \
    iputils-ping

# Copy the Python script into the container
COPY mission/script_boat.py /app/
COPY mission/script_boia.py /app/

# Set the work directory
WORKDIR /app

