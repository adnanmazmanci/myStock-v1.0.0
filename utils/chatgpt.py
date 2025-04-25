import openai
import yaml

# Load config from settings.yaml
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

client = openai.OpenAI(api_key=config["openai_api_key"])

def summarize_with_chatgpt(prompt: str) -> str:
    """Uses gpt-4o-mini to summarize the provided prompt via Chat Completions endpoint."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4o-mini" if available in your plan
            messages=[
                {"role": "system", "content": "You're a financial analyst summarizing market news."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Error occurred while requesting ChatGPT: {e}")
        return None
