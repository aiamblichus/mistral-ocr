# Mistral OCR

<img align="right" src="./vibecoded.png" width="200">

Extract text from PDFs and images using Mistral's OCR API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

Mistral OCR is a command-line tool that leverages Mistral's OCR technology to extract text content from PDFs and images. It produces clean markdown output and supports batch processing.

## ✨ Features

- **PDF & Image Support**: Process PDFs, JPG, PNG, and other common image formats
- **High Accuracy**: Powered by Mistral's advanced OCR models
- **Batch Processing**: Process multiple files efficiently
- **Rich CLI**: Beautiful progress indicators and colored output
- **Flexible Output**: Save extracted content as markdown files
- **Metadata Export**: Optional JSON metadata for each processed file

## 🚀 Quick Start

### Installation

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
uv tool install "mistral-ocr @ https://github.com/aiamblichus/mistral-ocr.git"
```

### API Key Setup

Get your Mistral API key from [Mistral's platform](https://mistral.ai/) and set it as an environment variable:

```bash
export MISTRAL_API_KEY="your-api-key-here"
```

## 📖 Usage

### Basic Usage

Process a single PDF:

```bash
mistral-ocr document.pdf
```

Process multiple files:

```bash
mistral-ocr file1.pdf file2.jpg image.png
```

### Advanced Options

Specify output directory:

```bash
mistral-ocr --output-dir ./output *.pdf
```

Use a specific OCR model:

```bash
mistral-ocr --model mistral-ocr-latest document.pdf
```

Include base64 image data (increases API cost):

```bash
mistral-ocr --include-image-base64 screenshot.png
```

### Output

For each processed file, Mistral OCR creates:

- `filename.ocr.md` - Extracted text content in markdown format
- `filename.ocr.json` - Processing metadata (optional, when output directory is specified)

## 🛠 Development

### Prerequisites

- Python 3.13+
- uv package manager

### Setup

```bash
# Install dependencies
make install-dev

# Build and install the package
make install-package

# Run tests
make test

# Lint and format code
make lint
make format
```

### Project Structure

```
mistral-ocr/
├── main.py              # CLI entry point with typer app
├── ocr/                 # OCR service package
│   ├── __init__.py
│   ├── base.py         # Base OCR service classes
│   └── mistral.py      # Mistral OCR implementation
├── pyproject.toml       # Project configuration
├── Makefile            # Development tasks
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

- `MISTRAL_API_KEY` - Your Mistral API key (required)

### CLI Options

| Option                   | Short | Description                           | Default              |
| ------------------------ | ----- | ------------------------------------- | -------------------- |
| `--output-dir`           | `-o`  | Output directory for processed files  | Current directory    |
| `--model`                | `-m`  | OCR model to use                      | `mistral-ocr-latest` |
| `--include-image-base64` |       | Include base64 image data in response | `False`              |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests and linting: `make test && make lint`
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature`
7. Open a Pull Request

### Code Style

This project uses:

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Pytest** for testing

Run `make format` before committing to ensure code style compliance.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai/) for their excellent OCR API
- [Typer](https://typer.tiangolo.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful console output
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation

## 📞 Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs or issues
- 💡 Suggesting features
- 🤝 Contributing code

---

Made with ❤️ using Mistral's OCR technology
