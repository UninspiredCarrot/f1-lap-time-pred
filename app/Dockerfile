# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl
# Copy the current directory contents into the container at /app
COPY . .
EXPOSE 3000
# Command to run the producer script
CMD ["python", "app.py"]
