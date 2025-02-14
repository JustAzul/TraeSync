# Use a lightweight Python 3.9 image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command: 
# You can override the --config-folder argument with a mounted volume at runtime.
# CMD ["python3", "main.py", "--config-folder", "/app/config", "--check-interval", "60"]
