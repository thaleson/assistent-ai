from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConversationSummaryOutput:
    conversation_id: str
    title: str
    summary: str