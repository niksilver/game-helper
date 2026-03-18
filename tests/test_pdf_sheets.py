import time
import pytest
from datetime import datetime

from gamehelper.pdf_sheets import PDFSheets


class TestPDFSheetsOutput:


    def _make_pdf(self, path, **kwargs):
        """Create a minimal one-page PDF and return its bytes."""
        sheets = PDFSheets(card_width = 63, card_height = 88)
        sheets._add_page()
        sheets.output(str(path), **kwargs)
        with open(str(path), 'rb') as f:
            return f.read()


    def test_output_accepts_int_date(self, tmp_path):
        """Should accept an int (seconds since Epoch) for the date parameter."""
        self._make_pdf(tmp_path / 'out.pdf', date = 0)


    def test_output_is_deterministic_with_int_date(self, tmp_path):
        """Two calls with the same int date should produce identical binary output."""
        a = self._make_pdf(tmp_path / 'a.pdf', date = 0)
        b = self._make_pdf(tmp_path / 'b.pdf', date = 0)
        assert a == b


    def test_output_different_int_dates_differ(self, tmp_path):
        """Two calls with different int dates should produce different binary output."""
        a = self._make_pdf(tmp_path / 'a.pdf', date = 0)
        b = self._make_pdf(tmp_path / 'b.pdf', date = 1000)
        assert a != b


    def test_output_accepts_datetime(self, tmp_path):
        """Should accept a datetime object for the date parameter."""
        self._make_pdf(tmp_path / 'out.pdf', date = datetime(2024, 1, 1))


    def test_output_is_deterministic_with_default_date(self, tmp_path):
        """Two calls with no date argument should produce identical binary output."""
        a = self._make_pdf(tmp_path / 'a.pdf')
        time.sleep(1)
        b = self._make_pdf(tmp_path / 'b.pdf')
        assert a == b
