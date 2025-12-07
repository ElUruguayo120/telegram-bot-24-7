FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for logs and data
RUN mkdir -p /app/data

# Run the bot
CMD ["python3", "news_bot.py"]

