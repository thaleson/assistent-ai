from typing import Any

import httpx


API_BASE_URL = "http://127.0.0.1:8000/api/v1"


def send_message(
    message: str,
    conversation_id: str,
) -> dict[str, Any]:
    """
    Send a message to the Raissa AI backend.
    """
    payload = {
        "conversation_id": conversation_id,
        "message": message,
    }

    with httpx.Client(timeout=90.0) as client:
        response = client.post(
            f"{API_BASE_URL}/chat",
            json=payload,
        )

        response.raise_for_status()

        return response.json()


def list_conversations() -> list[dict[str, Any]]:
    """
    Return the most recent conversations from the backend.
    """
    with httpx.Client(timeout=30.0) as client:
        response = client.get(
            f"{API_BASE_URL}/conversations"
        )

        response.raise_for_status()

        return response.json()


def get_conversation(
    conversation_id: str,
) -> dict[str, Any]:
    """
    Return the complete history of a conversation.
    """
    with httpx.Client(timeout=30.0) as client:
        response = client.get(
            f"{API_BASE_URL}/conversations/{conversation_id}"
        )

        response.raise_for_status()

        return response.json()



def generate_conversation_summary(
    conversation_id: str,
) -> dict[str, Any]:
    """
    Generate a summary for an existing conversation.
    """
    with httpx.Client(timeout=90.0) as client:
        response = client.post(
            (
                f"{API_BASE_URL}/conversations/"
                f"{conversation_id}/summary"
            )
        )

        response.raise_for_status()

        return response.json()


def download_summary_document(
    conversation_id: str,
    document_format: str,
) -> bytes:
    """
    Download a generated conversation summary document.
    """
    with httpx.Client(timeout=90.0) as client:
        response = client.get(
            (
                f"{API_BASE_URL}/conversations/"
                f"{conversation_id}/summary/"
                f"{document_format}"
            )
        )

        response.raise_for_status()

        return response.content