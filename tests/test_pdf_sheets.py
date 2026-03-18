import re
import time
import pytest
from datetime import datetime, timezone

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


    def test_output_embeds_date_in_pdf(self, tmp_path):
        """The date parameter should be embedded as the PDF CreationDate."""
        self._make_pdf(tmp_path / 'out.pdf', date = 0)
        pdf_bytes = (tmp_path / 'out.pdf').read_bytes()
        match = re.search(rb'CreationDate \(D:(\d{14})', pdf_bytes)
        assert match, "PDF does not contain a CreationDate"
        assert match.group(1) == b'19700101000000'


    def test_output_is_deterministic_with_default_date(self, tmp_path):
        """Two calls with no date argument should produce identical binary output."""
        a = self._make_pdf(tmp_path / 'a.pdf')
        time.sleep(1)
        b = self._make_pdf(tmp_path / 'b.pdf')
        assert a == b


    def test_output_none_date_uses_current_time(self, tmp_path):
        """date=None should embed the current date and time in the PDF."""
        before = datetime.now(tz = timezone.utc).replace(microsecond = 0)
        self._make_pdf(tmp_path / 'out.pdf', date = None)
        after = datetime.now(tz = timezone.utc)
        pdf_bytes = (tmp_path / 'out.pdf').read_bytes()
        match = re.search(rb'CreationDate \(D:(\d{14})', pdf_bytes)
        assert match, "PDF does not contain a CreationDate"
        ts_str        = match.group(1).decode()
        creation_date = datetime.strptime(ts_str, '%Y%m%d%H%M%S').replace(tzinfo = timezone.utc)
        assert before <= creation_date <= after
