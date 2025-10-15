FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency list first (to leverage Docker cache)
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of the project files
COPY . .

# Expose app port
EXPOSE 8000

# Run the app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
