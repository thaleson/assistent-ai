from dataclasses import dataclass

from backend.domain.enums.document_format import (
    DocumentFormat,
)


@dataclass(frozen=True, slots=True)
class GenerateDocumentInput:
    title: str
    content: str
    document_format: DocumentFormat


@dataclass(frozen=True, slots=True)
class GenerateDocumentOutput:
    content: bytes
    filename: str
    media_type: str