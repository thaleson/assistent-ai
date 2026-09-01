import re
import unicodedata
from collections.abc import Iterable

from backend.application.dto.document import (
    GenerateDocumentInput,
    GenerateDocumentOutput,
)
from backend.domain.interfaces.document_generator import (
    IDocumentGenerator,
)


class GenerateDocumentUseCase:
    def __init__(
        self,
        generators: Iterable[IDocumentGenerator],
    ) -> None:
        self._generators = {
            generator.document_format: generator
            for generator in generators
        }

    def execute(
        self,
        document_input: GenerateDocumentInput,
    ) -> GenerateDocumentOutput:
        """
        Generate a downloadable document.
        """
        generator = self._generators.get(
            document_input.document_format
        )

        if generator is None:
            raise ValueError(
                "Unsupported document format."
            )

        content = generator.generate(
            title=document_input.title,
            content=document_input.content,
        )

        filename = self._build_filename(
            document_input.title
        )

        return GenerateDocumentOutput(
            content=content,
            filename=(
                f"{filename}."
                f"{generator.file_extension}"
            ),
            media_type=generator.media_type,
        )

    @staticmethod
    def _build_filename(
        title: str,
    ) -> str:
        """
        Build a safe filename from the document title.
        """
        normalized = unicodedata.normalize(
            "NFKD",
            title,
        )

        normalized = normalized.encode(
            "ascii",
            "ignore",
        ).decode("ascii")

        normalized = normalized.lower()

        normalized = re.sub(
            r"[^a-z0-9]+",
            "_",
            normalized,
        )

        normalized = normalized.strip("_")

        return normalized or "raissa_ai_resumo"