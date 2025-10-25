# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy your code and dependency list
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your bot script
COPY gateway_bot.py .

# Environment variables (you can override these at runtime)
ENV DISCORD_BOT_TOKEN="DISCORD_BOT_TOKEN"
ENV N8N_WEBHOOK_URL="http://host.docker.internal:5678/webhook-test/discord-message"

# Run the bot
CMD ["python", "gateway_bot.py"]

