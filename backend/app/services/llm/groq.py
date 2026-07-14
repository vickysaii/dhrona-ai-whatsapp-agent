from groq import Groq
from app.config import settings


class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def generate_chat_response(
        self,
        prompt: str,
        system_instruction: str,
        temperature: float = 0.3,
        max_tokens: int = 800,
    ):
        """
        Generate a response using Groq.
        Returns (response_text, tokens_used)
        """

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": system_instruction,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        answer = response.choices[0].message.content

        tokens = 0
        if response.usage:
            tokens = response.usage.total_tokens

        return answer, tokens