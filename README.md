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


# Learning

Run `make test` to run a small number of unit tests.

Demo scripts are in the `demos` directory.


## Setup

The HTML rendering uses [pdf2image](https://github.com/Belval/pdf2image),
which in turn requires poppler to be installed. On Ubuntu:
```
sudo apt-get install poppler-utils
```
otherwise look at [the pdf2image page](https://github.com/Belval/pdf2image).
