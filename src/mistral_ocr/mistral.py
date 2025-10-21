"""Mistral OCR service implementation."""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

from mistralai import Mistral

from .base import BaseOCRService, OCRResult


class MistralOCRService(BaseOCRService):
    """OCR service using Mistral's OCR API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "mistral-ocr-latest",
    ):
        """Initialize the Mistral OCR service.

        Args:
            api_key: Mistral API key. If None, uses MISTRAL_API_KEY env var.
            model: OCR model to use (default: mistral-ocr-latest)
        """
        self.model = model
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")

        if not self.api_key:
            raise ValueError(
                "MISTRAL_API_KEY environment variable must be set or api_key provided"
            )

        try:
            self.client = Mistral(api_key=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Error initializing Mistral client: {e}") from e

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "mistral"

    def _is_image_file(self, file_path: Path) -> bool:
        """Check if file is an image based on extension."""
        image_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".avif",
            ".gif",
            ".bmp",
            ".tiff",
            ".tif",
        }
        return file_path.suffix.lower() in image_extensions

    def _encode_file_to_base64(self, file_path: Path) -> str:
        """Encode a file to base64 string."""
        try:
            with open(file_path, "rb") as file:
                return base64.b64encode(file.read()).decode("utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error encoding file {file_path}: {e}") from e

    def _extract_content_from_response(self, ocr_response: Any) -> str:
        """Extract content from OCR response."""
        return "\n\n".join(page.markdown for page in ocr_response.pages)

    def _create_metadata(
        self,
        ocr_response: Any,
        source_path: Path,
        include_image_base64: bool,
    ) -> dict[str, Any]:
        """Create metadata dictionary from OCR response."""
        metadata = {
            "scheme": "mistral_ocr",
            "provider": self.provider_name,
            "model": self.model,
            "source_file": str(source_path),
            "include_image_base64": include_image_base64,
        }

        # If response has additional metadata, include it
        if hasattr(ocr_response, "pages") and ocr_response.pages:
            pages = ocr_response.pages
            if len(pages) > 0:
                metadata["pages"] = len(pages)

        return metadata

    def process_file(
        self,
        file_path: Path,
        output_dir: Path | None = None,
        include_image_base64: bool = False,
        **kwargs: Any,
    ) -> OCRResult:
        """Process a single file with Mistral OCR.

        Args:
            file_path: Path to the PDF or image file to process
            output_dir: Directory to save output files (optional)
            include_image_base64: Whether to include base64 image data in response
            **kwargs: Additional options (ignored for Mistral)

        Returns:
            OCRResult containing the extracted content and metadata
        """
        # Determine document type and prepare data
        if self._is_image_file(file_path):
            # For images, encode to base64 and use image_url type
            base64_data = self._encode_file_to_base64(file_path)
            mime_type = f"image/{file_path.suffix.lower().lstrip('.')}"
            if mime_type == "image/jpg":
                mime_type = "image/jpeg"

            document: dict[str, Any] = {
                "type": "image_url",
                "image_url": f"data:{mime_type};base64,{base64_data}",
            }
        else:
            # For documents (PDF, etc.), upload file first
            with open(file_path, "rb") as file:
                uploaded_file = self.client.files.upload(
                    file={
                        "file_name": file_path.name,
                        "content": file,
                    },
                    purpose="ocr",
                )

            # Get signed URL
            signed_url = self.client.files.get_signed_url(file_id=uploaded_file.id)

            document = {
                "type": "document_url",
                "document_url": signed_url.url,
            }

        # Process with OCR
        ocr_response = self.client.ocr.process(
            model=self.model,
            document=document,  # type: ignore[arg-type]
            include_image_base64=include_image_base64,
        )

        # Extract markdown content from response
        content = self._extract_content_from_response(ocr_response)

        # Create metadata
        metadata = self._create_metadata(ocr_response, file_path, include_image_base64)

        # Save to files if output_dir is specified
        output_path = None
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Write content to markdown file
            output_path = output_dir / f"{file_path.stem}.ocr.md"
            output_path.write_text(content, encoding="utf-8")

            # Write metadata to JSON file
            metadata_path = output_dir / f"{file_path.stem}.ocr.json"
            with metadata_path.open("w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

        return OCRResult(
            content=content,
            metadata=metadata,
            output_path=output_path,
        )
