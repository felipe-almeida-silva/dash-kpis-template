# Use an official Python runtime as a parent image
FROM python:3.11-bullseye

# Set the working directory to /app
WORKDIR /app

# Create a directory called "my_directory"
RUN mkdir /app/tmp

# Install Node.js and Git
RUN apt-get update && \
    apt-get install -y curl git build-essential && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8050

# Run app.py when the container launches
CMD ["python3", "dash-kpis.py"]