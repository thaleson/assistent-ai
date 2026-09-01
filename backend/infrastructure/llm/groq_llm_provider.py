import asyncio

from groq import Groq

from backend.domain.entities.chat_message import ChatMessage
from backend.domain.interfaces.llm_provider import ILLMProvider


class GroqLLMProvider(ILLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self._client = Groq(
            api_key=api_key,
        )
        self._model = model

    async def generate(
        self,
        system_prompt: str,
        user_message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Generate a response using a model hosted on GroqCloud.
        """
        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        for history_message in history:
            messages.append(
                {
                    "role": history_message.role.value,
                    "content": history_message.content,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = await asyncio.to_thread(
            self._client.chat.completions.create,
            model=self._model,
            messages=messages,
            temperature=0.6,
            max_completion_tokens=2048,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "Groq returned an empty response."
            )

        return content