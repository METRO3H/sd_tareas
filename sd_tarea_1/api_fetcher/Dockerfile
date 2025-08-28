# Using the official Alpine Python image

FROM python:3.13-slim


# Setting the working directory in the container to /app
WORKDIR /app

# Copying the requirements.txt file to the container
COPY . .

# Installing the required dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Run fetcher.py when the container launches
CMD ["python", "fetcher.py"]