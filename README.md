# discord-bot

**Example project** that demonstrates how to detect messages from Discord and forward them to an external system (API, webhook, message queue, etc.).
This repository provides a minimal, easy-to-adapt template for listening to Discord messages, filtering/processing them, and sending the payload onward.

---

## Table of Contents

* [What this is](#what-this-is)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Setup](#setup)

  * [1. Clone](#1-clone)
  * [2. Ignore secret token](#2-ignore-secret-token)
  * [3. Install dependencies](#3-install-dependencies)
  * [4. Configure environment variables](#4-configure-environment-variables)
* [Run](#run)
* [How message detection works](#how-message-detection-works)
* [Forwarding to external systems](#forwarding-to-external-systems)
* [Examples](#examples)
* [Development & testing](#development--testing)
* [Troubleshooting](#troubleshooting)
* [Security](#security)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

---

## What this is

A small Discord bot example written to:

* connect to Discord via a bot token,
* listen for messages (in channels, DMs, or specific channels),
* process and optionally filter the messages,
* send detected message data to a target system (HTTP endpoint, webhook, or queue).

This is intentionally simple so you can plug in your own processing logic and destination system.

---

## Features

* Connect to Discord gateway using a bot token
* Detect messages that match simple filters (keywords, mentions, regex)
* Enrich and normalize message payloads (author, timestamp, channel, attachments)
* Send payload to external system via configurable method (HTTP POST / webhook / custom handler)
* Example of safe handling for private token files (`.gitignore` instructions included)

---

## Prerequisites

* Node.js >= 16 (or whichever runtime your example uses) **or** Python >= 3.8 (adjust according to project language)
* A GitHub/Git remote (optional)
* A Discord application and bot token (create in [Discord Developer Portal](https://discord.com/developers/applications))
* Access to the external system you'll forward messages to (URL, webhook, credentials)

---

## Setup

### 1. Clone

```bash
git clone https://github.com/VisarutJDev/discord-bot.git
cd discord-bot
```

### 2. Ignore secret token

If your bot token is stored in a file like `private_token.txt` or a `.env` file, make sure it is ignored by Git:

```bash
# Add token file name to .gitignore
echo "private_token.txt" >> .gitignore
echo ".env" >> .gitignore

# If .gitignore changed, commit it
git add .gitignore
git commit -m "Ignore private token files"
```

> **Important:** Never commit tokens or credentials. If you committed one by accident, remove it from history (see `troubleshooting`).

### 3. Install dependencies

(Example for Node.js using discord.js)

```bash
npm install
```

(Or for Python + discord.py)

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` (kept local and ignored) or set environment variables:

Example `.env`:

```
DISCORD_BOT_TOKEN=your_bot_token_here
FORWARD_URL=https://example.com/webhook
FORWARD_METHOD=POST
FILTER_KEYWORDS=alert,important
```

Alternative: store token in `private_token.txt` (not recommended) but ensure `.gitignore` contains it.

---

## Run

Start the bot:

```bash
# Node
npm start

# or Python
python bot.py
```

You should see logs showing connection to Discord and ready status:

```
Bot logged in as MyBot#1234
Listening to messages...
```

---

## How message detection works

1. **Event subscription**: The bot subscribes to Discord message events (e.g., `messageCreate` in discord.js or `on_message` in discord.py).
2. **Filtering**: On each message, the bot runs configured filters:

   * Ignore messages from bots (to avoid loops).
   * Keyword filters (`FILTER_KEYWORDS`) or regex matching.
   * Optional channel ID whitelist/blacklist.
3. **Normalization**: The bot builds a JSON payload:

```json
{
  "id": "message-id",
  "guild_id": "guild-id",
  "channel_id": "channel-id",
  "author": {
    "id": "user-id",
    "username": "user",
    "discriminator": "1234"
  },
  "content": "The message text",
  "attachments": [...],
  "timestamp": "2025-10-25T..."
}
```

4. **Forwarding**: The payload is forwarded to the configured destination via a handler (HTTP POST, webhook, push to queue, etc.). The handler may add metadata, HMAC signatures, or retries.

---

## Forwarding to external systems

The project includes a pluggable forwarding handler. Example strategies:

* **HTTP POST**: Send JSON payload to `FORWARD_URL`. Handle errors and retry with exponential backoff.
* **Webhook secret**: Sign outgoing payloads with HMAC to let the receiver verify authenticity.
* **Message queue**: Push payloads into RabbitMQ / Kafka / SQS for downstream processing.
* **Local handler**: Save payloads locally for debugging.

Example HTTP forwarder (pseudocode):

```js
async function forward(payload) {
  await fetch(process.env.FORWARD_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Signature': signature },
    body: JSON.stringify(payload),
  });
}
```

---

## Examples

### Filter messages for keywords

Detect messages containing `!alert` or keywords from `FILTER_KEYWORDS` and forward them.

### Forward attachments

If a message contains attachments, include attachment URLs in the forwarded payload. Optionally download and re-upload to your storage if the receiver cannot fetch external URLs.

### Rate limiting & batching

If high message volume is expected, implement batching or rate-limiting to avoid throttling on the receiver and to reduce network overhead.

---

## Development & testing

* Use a test Discord server and bot account.
* Keep tokens for dev/test separate from production tokens.
* Use local mocks for the forward endpoint in tests (e.g., `http://localhost:8080/mock-webhook`).
* Unit-test the filtering and payload building logic.

---

## Troubleshooting

* **`Author identity unknown` / commit issues**: configure `git config --global user.name` and `user.email`.
* **Token accidentally committed**: rotate the token immediately. To remove from Git history, use:

  ```bash
  git rm --cached private_token.txt
  git commit -m "Remove secret token"
  # Then purge from history (dangerous, use carefully)
  git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch private_token.txt" --prune-empty --tag-name-filter cat -- --all
  ```
* **Push failures (invalid credentials)**: use PAT or SSH key (see project docs).
* **Discord connection errors**: ensure bot token is valid and the bot is invited to the server with correct intents. If you need message content, enable the **Message Content Intent** in the Discord Developer Portal and request it in your client options.

---

## Security

* Keep bot token and any API keys out of repo. Use secrets manager or environment variables for production.
* When forwarding sensitive content, use TLS and sign payloads.
* Implement retries and dead-letter queue for failed forwards to avoid message loss.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit your changes and open a PR
4. Include tests for new logic

---

## License

This project is provided as an example. Add your LICENSE file (e.g., MIT) as appropriate.

---

## Contact

For questions or help adapting this to your systems, open an issue or contact the maintainer at `visarut@example.com`.

