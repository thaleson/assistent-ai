from abc import ABC, abstractmethod

from backend.domain.enums.document_format import (
    DocumentFormat,
)


class IDocumentGenerator(ABC):
    @property
    @abstractmethod
    def document_format(self) -> DocumentFormat:
        """
        Return the document format handled by the generator.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def media_type(self) -> str:
        """
        Return the MIME type produced by the generator.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """
        Return the generated file extension.
        """
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        title: str,
        content: str,
    ) -> bytes:
        """
        Generate a document and return its binary content.
        """
        raise NotImplementedError