# Use the official Python 3.12-slim image
FROM python:3.12-slim

# Set the working directory early
WORKDIR /app

# Copy the requirements.txt first to leverage Docker caching
COPY requirements.txt .

# Install system dependencies, clean up, and set up the application
RUN apt-get update && \
    apt-get install -y --no-install-recommends git libgit2-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make Python scripts executable
RUN chmod +x *.py

# Set entrypoint to run main.py
ENTRYPOINT ["python", "-u", "main.py"]

# Default command to run with scale-type, can be overridden with Docker run arguments
CMD ["--scale-type", "scale_up"]
