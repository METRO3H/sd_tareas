# Using the official Alpine Python image
FROM python:3.13-slim

# Setting the working directory in the container to /app
WORKDIR /app

# Installing the required dependencies for psycopg
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Installing the required dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8050
EXPOSE 8075

# Run FastAPI with Uvicorn
CMD ["uvicorn", "m_server:app", "--host", "0.0.0.0", "--port", "8075"]
