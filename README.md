# Gamehelper

Utilities to help generate cards (and tokens) for board games.
Written in Python.


## Key modules

`CardMaker` class enables the creation of individual cards.

`PDFSheets` class assembles card images into a PDF document. This document
may consist of several sheets, and allows card backs to be printed on the
reverse of each card. Each card may have a gutter for cutting.

`ImageSheet` class assembles card images into a grid in a single
image. Useful for uploading to Screentop, etc.

`ExcelHelper` class for easier navigation of an Excel sheet, where you
might store card data.


## Learning

Run `make test` to run a small number of unit tests.

Demo scripts are in the `demos` directory. From the root directory here, run
```
python demos/name_of_demo_script.py
```
or either of these:
```
make image-demo
make pdf-demo
```


## Setup

The HTML rendering uses [html2image](https://pypi.org/project/html2image/),
which in turn requires Chromium or Google Chrome to be installed, which will
run headless.
This is what I used to get Google Chome on WSL/Ubuntu:
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -y google-chrome-stable_current_amd64.deb
google-chrome --version
```

I found Google Chrome also needed other packages to run without warnings.
In my case
```
sudo apt install dbus
sudo apt install upower
```


## Development

While this is in development and in use in another project, we'll have a
structure like this:

```
myproject
 |_Makefile
 \_gamehelper
    |_gamehelper
    | |_card_maker.py
    | |_image_sheet.py
    | |_pdf_sheets.py
    |
    |_tests
    \_demos
```

This structure is taken from [PyPA on GitHub](https://github.com/pypa/sampleproject/)
and the associated [packaging documentation](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).

The chosen build backend is hatchling - it [seems simplest](https://www.linkedin.com/pulse/comparing-python-build-backends-setuptools-hatchling-flit-sharma-cq2cf/).

We can then install it in editable mode like this:
```
cd myproject
python -m pip install -e gamehelper
```
