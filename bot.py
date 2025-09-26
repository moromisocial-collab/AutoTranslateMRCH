import discord
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

# 翻訳を許可するチャンネルIDリスト
ALLOWED_CHANNELS = [1420722848506445826]  # 数字に置き換え

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def translate_text(text, target_lang):
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(DEEPL_URL, data=params)
    result = response.json()
    return result["translations"][0]["text"]

@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # ✅ チャンネル制限
    if message.channel.id not in ALLOWED_CHANNELS:
        return

    content = message.content

    # 日本語を含んでいれば → 英語
    if any("\u3040" <= ch <= "\u30ff" for ch in content):
        translated = translate_text(content, "EN")
        await message.channel.send(f"🇯🇵→🇺🇸 {translated}")

    # 英語を含んでいれば → 日本語
    elif any("a" <= ch.lower() <= "z" for ch in content):
        translated = translate_text(content, "JA")
        await message.channel.send(f"🇺🇸→🇯🇵 {translated}")

client.run(DISCORD_TOKEN)