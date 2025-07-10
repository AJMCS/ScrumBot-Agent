import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("OXEN_API_KEY"),
    base_url="https://hub.oxen.ai/api"
)

response = client.chat.completions.create(
    model="openai:gpt-4o-mini",
    messages=[{"role": "user", "content": "What is a great name for an ox that also manages your AI infrastructure?"}]
)

print(response.output['content'][0]['text'])