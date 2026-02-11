.PHONY: test docs

ifeq ($(VIRTUAL_ENV),)
$(error Please activate virtual environment for Python)
endif

test:
	@echo "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
	python -m pytest --tb=short --capture=no

docs:
	python -m pdoc gamehelper/ -o ./docs

image-demo:
	python demos/image_sheet_demo.py

pdf-demo:
	python demos/pdf_sheets_demo.py
