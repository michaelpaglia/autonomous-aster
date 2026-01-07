FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install aster connector from GitHub
RUN pip install git+https://github.com/asterdex/aster-connector-python.git

# Copy application files
COPY src/ ./src/
COPY main.py .
COPY .env .

# Create log directory
RUN mkdir -p /app/logs

# Run the bot
CMD ["python", "-u", "main.py"]
