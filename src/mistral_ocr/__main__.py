"""Mistral OCR CLI tool."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from mistral_ocr.mistral import MistralOCRService

# Create typer app and console
app = typer.Typer(
    name="mistral-ocr",
    help="Extract text from PDFs and images using Mistral OCR",
    add_completion=False,
)
console = Console()


@app.command("ocr")
def ocr(
    files: list[Path] = typer.Argument(
        ..., help="List of PDF or image files to process"
    ),
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", "-o", help="Output directory for processed files"),
    ] = Path("."),
    model: Annotated[
        str,
        typer.Option("--model", "-m", help="OCR model to use"),
    ] = "mistral-ocr-latest",
    include_image_base64: Annotated[
        bool,
        typer.Option(help="Include base64 image data in OCR response (increases cost)"),
    ] = False,
) -> None:
    """Process PDFs and images using Mistral OCR.

    This command extracts text content from PDFs and images using Mistral's OCR API
    and outputs markdown files with the extracted content.

    Examples:
        mistral-ocr ocr document.pdf
        mistral-ocr ocr --output-dir ./output *.pdf
        mistral-ocr ocr --model mistral-ocr-latest image.jpg
    """
    # Validate input files
    valid_files = []
    for file_path in files:
        if not file_path.exists():
            console.print(f"[red]Error:[/red] File {file_path} does not exist")
            raise typer.Exit(1)

        if not file_path.is_file():
            console.print(f"[red]Error:[/red] {file_path} is not a file")
            raise typer.Exit(1)

        valid_files.append(file_path)

    if not valid_files:
        console.print("[yellow]Warning:[/yellow] No valid files to process")
        return

    # Initialize the OCR service
    try:
        service = MistralOCRService(model=model)
    except Exception as e:
        console.print(f"[red]Error initializing Mistral OCR service:[/red] {e}")
        raise typer.Exit(1)

    # Process files
    console.print(f"Processing {len(valid_files)} files with Mistral OCR...")

    success_count = 0
    total_count = len(valid_files)

    with console.status("[bold green]Processing files...[/bold green]") as status:
        results = service.process_files(
            valid_files,
            output_dir=output_dir,
            include_image_base64=include_image_base64,
        )

        for i, (file_path, result) in enumerate(zip(valid_files, results)):
            status.update(f"Processing {file_path.name}... ({i+1}/{total_count})")

            if result.metadata.get("success", True):
                success_count += 1
                if output_dir:
                    console.print(
                        f"[green]✓[/green] Processed {file_path.name} → {result.output_path}"
                    )
                else:
                    console.print(f"[green]✓[/green] Processed {file_path.name}")
            else:
                error = result.metadata.get("error", "Unknown error")
                console.print(f"[red]✗[/red] Failed {file_path.name}: {error}")

    # Summary
    if success_count == total_count:
        console.print(
            f"[bold green]Successfully processed all {total_count} files![/bold green]"
        )
    else:
        console.print(
            f"[yellow]Processed {success_count}/{total_count} files successfully[/yellow]"
        )


if __name__ == "__main__":
    app()
