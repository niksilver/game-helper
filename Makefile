.PHONY: test docs

test:
	@echo "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
	uv run pytest --tb=short --capture=no

docs:
	uv run pdoc src/gamehelper -o ./docs

image-demo:
	uv run demos/image_sheet_demo.py

pdf-demo:
	uv run demos/pdf_sheets_demo.py
