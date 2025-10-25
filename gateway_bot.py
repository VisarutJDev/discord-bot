import asyncio
import json
import os
import requests
import websockets

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # export DISCORD_BOT_TOKEN="your_token_here"
GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

async def heartbeat(ws, interval):
    while True:
        await asyncio.sleep(interval / 1000)
        await ws.send(json.dumps({"op": 1, "d": None}))

async def main():
    async with websockets.connect(GATEWAY_URL) as ws:
        # Receive Hello
        hello = json.loads(await ws.recv())
        heartbeat_interval = hello["d"]["heartbeat_interval"]
        asyncio.create_task(heartbeat(ws, heartbeat_interval))

        # Identify the bot
        payload = {
            "op": 2,
            "d": {
                "token": TOKEN,
                "intents": 513,  # GUILDS + GUILD_MESSAGES
                "properties": {"$os": "linux", "$browser": "ubuntu", "$device": "server"}
            }
        }
        await ws.send(json.dumps(payload))

        # Main event loop
        while True:
            msg = await ws.recv()
            event = json.loads(msg)
            t = event.get("t")
            d = event.get("d")

            if t == "READY":
                print(f"✅ Logged in as {d['user']['username']}")
            elif t == "MESSAGE_CREATE":
                try:
                    bot = d["author"]["bot"]
                    if bot: 
                        continue
                except KeyError as e:
                    print(f"KeyError: {e} not bot message")

                author = d["author"]["username"]
                content = d["content"]
                print(f"💬 {author}: {content}")
                try:
                    payload = d
                    r = requests.get(N8N_WEBHOOK_URL, json=payload)
                    print(f"📤 Sent to n8n ({r.status_code})")
                except Exception as e:
                    print(f"⚠️ Error sending to n8n: {e}")

asyncio.run(main())

