.PHONY: test docs

test:
	@echo "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
	uv run pytest --tb=short --capture=no

docs:
	python -m pdoc gamehelper/ -o ./docs

image-demo:
	python demos/image_sheet_demo.py

pdf-demo:
	python demos/pdf_sheets_demo.py
