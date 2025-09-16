FROM python:3.13-slim

# Setting the working directory in the container to /app
WORKDIR /app

# Copying everything
COPY . .

# Installing the required dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt