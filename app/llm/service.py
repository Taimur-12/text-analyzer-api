import json
from app.llm.client import client
from app.llm.prompts import sentiment_prompt

def analyze_with_llm(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role":"user", "content": sentiment_prompt(text)},
        ],
        temperature=0.2,
        max_tokens=200,
        timeout=10
    )
    content = response.choices[0].message.content
    return json.loads(content)