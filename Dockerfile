FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install aster connector from GitHub
RUN pip install git+https://github.com/asterdex/aster-connector-python.git

# Copy application files
COPY config.py .
COPY grok_client.py .
COPY autonomous_cosmic_trader.py .

# Create log directory
RUN mkdir -p /app/logs

# Run the bot
CMD ["python", "-u", "autonomous_cosmic_trader.py"]
