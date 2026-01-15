

def sentiment_prompt(text: str) -> str:
    return f"""
        You are an NLP analyst.

        Analyze the sentiment and tone of the following text.

        Text:
        {text}

        Return a JSON object with:
        - sentiment (positive | neutral | negative)
        - tone (one word)
        - explanation (1 short sentence)
        """
