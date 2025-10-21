.PHONY: help install install-dev build install-package test lint format clean dev-setup

# Default target
help:
	@echo "Available commands:"
	@echo "  install        - Install project dependencies"
	@echo "  install-dev    - Install project with development dependencies"
	@echo "  build          - Build the package"
	@echo "  install-package - Install the built package"
	@echo "  test           - Run tests"
	@echo "  lint           - Run linting"
	@echo "  format         - Format code"
	@echo "  clean          - Clean build artifacts"
	@echo "  dev-setup      - Full development setup (install-dev + install-package)"

# Install dependencies only
install:
	uv pip install -e .

# Install with development dependencies
install-dev:
	uv sync

# Build the package
build:
	uv build

# Install the built package
install-package: build
	uv pip install dist/*.whl --force-reinstall

# Run tests
test:
	uv run pytest

# Run linting
lint:
	uv run ruff check .
	uv run mypy .

# Format code
format:
	uv run ruff format .
	uv run ruff check --fix .

# Clean build artifacts
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Full development setup
dev-setup: install-dev install-package
	@echo "Development environment set up successfully!"
	@echo "You can now run 'mistral-ocr --help' to see available commands."
