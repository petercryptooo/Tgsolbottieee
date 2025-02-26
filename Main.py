from telethon import TelegramClient, events
import re

# Vul je Telegram API gegevens in
API_ID = "20603632"
API_HASH = "3a99d1990d90308b0c2312daa304dd69"
PHONE_NUMBER = "+18633693681"

# Channel waar we naar luisteren
SOURCE_CHANNEL = "https://t.me/DRBTSolana"
TARGET_CHANNEL = "https://t.me/bdkdjeownsbs"  # Het kanaal waar je de gefilterde berichten naartoe wilt sturen

# Maak een client aan
client = TelegramClient("session_name", API_ID, API_HASH)


# Functie om berichten te filteren
def filter_message(message):
    try:
        text = message.text
        if not text:
            return False

        # Check of het een SPL Token 2022 is
        if "Type: SPL Token 2022" not in text:
            return False

        # Zoek de Fee met een regex
        fee_match = re.search(r"Fee:\s*(\d+)%", text)
        if not fee_match:
            return False
        fee = int(fee_match.group(1))

        # Check of de Fee tussen 1 en 10% is
        if not (1 <= fee <= 10):
            return False

        # Check op Telegram/Twitter-link in de beschrijving of links
        if "Telegram" in text or "Twitter" in text:
            return True

    except Exception as e:
        print(f"Fout bij filteren: {e}")
        return False

    return False


# Event-handler voor nieuwe berichten in het channel
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    message = event.message
    if filter_message(message):
        print("✅ Gefilterd bericht gevonden, doorsturen...")
        await client.send_message(TARGET_CHANNEL, message.text)


# Start de client
async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Bot is actief...")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
