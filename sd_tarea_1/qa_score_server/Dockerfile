# Using the official Alpine Python image
FROM python:3.13-slim

# Setting the working directory in the container to /app
WORKDIR /app

# Copying everything
COPY . .

# Installing the required dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
