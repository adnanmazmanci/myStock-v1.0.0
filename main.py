import time
from datetime import datetime
from utils.rss_collector import collect_latest_headlines
from utils.chatgpt import summarize_with_chatgpt
from utils.logger import log_message
from utils.storage import append_with_timestamp
from utils.notifier import send_public_update, send_status_message

# Emoji mapping for each tag
TAG_EMOJIS = {
    "US": "🇺🇸",
    "Europe": "🇪🇺",
    "Asia": "🇨🇳",
    "Türkiye": "🇹🇷",
    "Commodities": "🛢️",
    "Crypto": "🪙",
    "Global": "🌍"
}

def run_cycle():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n\n===== 🕒 {timestamp} =====\n"
    log_entry = header + log_message("🔄 Run started")

    try:
        # Step 1: Fetch latest headlines
        print("🔍 Fetching headlines...")
        headlines = collect_latest_headlines()
        if not headlines:
            log_entry += log_message("⚠️ No new headlines found.")
            send_status_message(log_entry)
            return

        log_entry += log_message(f"📰 {len(headlines)} new headlines fetched.")

        # Step 2: Group headlines by tag
        grouped = {}
        for h in headlines:
            tag = h['tag']
            grouped.setdefault(tag, []).append(h)

        # Step 3: Generate ChatGPT summaries per tag
        for tag, group in grouped.items():
            print(f"📝 Sending prompt for {tag} headlines to ChatGPT...")
            text = "\n".join([f"- {h['title']} ({h['link']})" for h in group])
            prompt = (
                f"For each of the following {tag} financial headlines, provide a short 1-2 sentence commentary "
                f"on the market implications. Return only a bulleted list where each line starts with the original headline in bold, "
                f"followed by a colon and your commentary.\n\n"
                f"{text}"
            )
            comment_block = summarize_with_chatgpt(prompt)

            if comment_block:
                append_with_timestamp(comment_block, "responses/responses.txt")
                emoji = TAG_EMOJIS.get(tag, "📰")
                formatted = f"{emoji} **{tag} Headlines Summary:**\n\n{comment_block}"
                send_public_update(formatted)
                log_entry += log_message(f"📤 {tag} headlines sent.")

        # Step 4: Market-wide conclusion
        all_titles = "\n".join([f"- {h['title']}" for h in headlines])
        conclusion_prompt = (
            "Based on the following global financial headlines, give a short overall summary "
            "of what might be happening in the world markets. The summary should be 3-4 sentences long.\n\n"
            f"{all_titles}"
        )
        print("📝 Sending overall market summary prompt to ChatGPT...")
        conclusion = summarize_with_chatgpt(conclusion_prompt)

        if conclusion:
            append_with_timestamp(conclusion, "responses/responses.txt")
            send_public_update(f"📊 **Market Conclusion:**\n\n{conclusion}")
            log_entry += log_message("✅ Final market summary sent.")

    except Exception as e:
        log_entry += log_message(f"❌ Error during run:\n{e}")
        send_status_message(f"❗ Error: {e}")

    finally:
        log_entry += log_message("✅ Run complete. Waiting 5 minutes...")
        send_status_message(log_entry)

def main():
    while True:
        run_cycle()
        time.sleep(300)  # ⏱ 10 seconds for testing, change to 300 (5 mins) for production

if __name__ == "__main__":
    main()
