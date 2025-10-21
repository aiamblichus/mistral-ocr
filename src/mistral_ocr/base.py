"""Base class for OCR services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class OCRResult(BaseModel):
    """Result of OCR processing."""

    content: str
    """The extracted text/markdown content."""

    metadata: dict[str, Any]
    """Metadata about the processing (model, pages, etc.)."""

    output_path: Path | None = None
    """Path where the result was saved, if any."""


class BaseOCRService(ABC):
    """Base class for OCR services.

    Provides a common interface for different OCR providers like Mistral, etc.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'mistral')."""

    @abstractmethod
    def process_file(
        self,
        file_path: Path,
        output_dir: Path | None = None,
        **kwargs: Any,
    ) -> OCRResult:
        """Process a single file with OCR.

        Args:
            file_path: Path to the file to process (PDF or image)
            output_dir: Directory to save output files (optional)
            **kwargs: Additional provider-specific options

        Returns:
            OCRResult containing the extracted content and metadata
        """
        ...

    def process_files(
        self,
        file_paths: list[Path],
        output_dir: Path | None = None,
        **kwargs: Any,
    ) -> list[OCRResult]:
        """Process multiple files with OCR.

        Args:
            file_paths: List of file paths to process
            output_dir: Directory to save output files (optional)
            **kwargs: Additional provider-specific options

        Returns:
            List of OCRResult objects
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.process_file(file_path, output_dir, **kwargs)
                results.append(result)
            except Exception as e:
                # Create a failed result
                failed_result = OCRResult(
                    content="",
                    metadata={
                        "error": str(e),
                        "provider": self.provider_name,
                        "source_file": str(file_path),
                        "success": False,
                    },
                )
                results.append(failed_result)
        return results
