from telegram import Bot
import yaml

with open('config/settings.yaml') as f:
    config = yaml.safe_load(f)

bot = Bot(token=config["telegram_bot_token"])

def send_status_message(text: str):
    try:
        bot.send_message(chat_id=config["status_chat_id"], text=text)
    except Exception as e:
        print(f"⚠️ Error sending status message to Telegram: {e}")

def send_public_update(text: str):
    try:
        bot.send_message(chat_id=config["public_chat_id"], text=text)
    except Exception as e:
        print(f"⚠️ Error sending public update to Telegram: {e}")
