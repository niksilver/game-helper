.PHONY: test docs

ifeq ($(VIRTUAL_ENV),)
$(error Please activate virtual environment for Python)
endif

test:
	@echo "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
	python -m pytest --tb=short --capture=no

docs:
	python -m pdoc gamehelper/ -o ./docs
