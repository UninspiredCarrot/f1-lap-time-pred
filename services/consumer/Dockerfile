# Use an official Python runtime as a parent image
FROM python:3.9-slim

# # Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . . 

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

# Command to run the producer script
CMD ["python", "consumer.py"]
