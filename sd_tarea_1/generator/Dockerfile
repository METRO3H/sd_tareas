FROM python:3.13-slim

# Setting the working directory in the container to /app
WORKDIR /app

COPY requirements.txt .

# Installing the required dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# run generator.py
CMD ["python", "-u","generator.py"]