import asyncio
import json

from groq import Groq

from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent_router import IAgentRouter


class LLMAgentRouter(IAgentRouter):
    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self._client = Groq(
            api_key=api_key,
        )
        self._model = model

    async def route(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> AgentType:
        """
        Classify the user message using recent conversation context.
        """
        history_text = "\n".join(
            f"{item.role.value}: {item.content}"
            for item in history[-10:]
        )

        system_prompt = """
You are an intent router for Raissa AI.

Classify the user's current message into exactly one category:

general:
Conversations, everyday questions, organization, ideas, emotional support,
advice, or anything that does not primarily belong to study or finance.

study:
Learning, school, university, exams, exercises, academic subjects,
explanations, summaries, homework, or study plans.

finance:
Money, budgeting, salary, expenses, debt, savings, investments,
income, financial planning, or personal finance.

Use the conversation history to understand short or ambiguous follow-up
messages.

Consider the main intention of the current conversation, not isolated
keywords.
""".strip()

        user_content = (
            "Recent conversation:\n"
            f"{history_text or '(no previous messages)'}\n\n"
            "Current user message:\n"
            f"{message}"
        )

        response = await asyncio.to_thread(
            self._client.chat.completions.create,
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_content,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "agent_routing",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "agent": {
                                "type": "string",
                                "enum": [
                                    "general",
                                    "study",
                                    "finance",
                                ],
                            }
                        },
                        "required": [
                            "agent",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            temperature=0,
        )

        content = response.choices[0].message.content

        if not content:
            return AgentType.GENERAL

        data = json.loads(content)

        return AgentType(
            data["agent"]
        )