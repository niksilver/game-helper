import pytest

from gamehelper.image_sheet import ImageSheet


class TestImageSheetCards:
    """Tests for the 'cards' parameter as an alternative to 'rows'."""

    def test_cards_calculates_rows_exact(self):
        """When cards divides evenly by columns, rows = cards / columns."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 3,
                           cards       = 6,
                           )
        assert sheet.rows == 2

    def test_cards_calculates_rows_rounds_up(self):
        """When cards doesn't divide evenly, rows rounds up."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 3,
                           cards       = 7,
                           )
        assert sheet.rows == 3

    def test_cards_single_column(self):
        """With 1 column, rows equals cards."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 1,
                           cards       = 5,
                           )
        assert sheet.rows == 5

    def test_cards_and_rows_raises_error(self):
        """Specifying both cards and rows should raise an error."""
        with pytest.raises(ValueError):
            ImageSheet(card_width  = 100,
                       card_height = 100,
                       columns     = 2,
                       rows        = 3,
                       cards       = 6,
                       )


class TestImageSheetProperties:
    """Tests for rows and columns public read-only properties."""

    def test_rows_is_readable(self):
        """The rows property should be readable."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 3,
                           rows        = 4,
                           )
        assert sheet.rows == 4

    def test_columns_is_readable(self):
        """The columns property should be readable."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 3,
                           rows        = 4,
                           )
        assert sheet.columns == 3

    def test_rows_is_read_only(self):
        """The rows property should not be writable."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 3,
                           rows        = 4,
                           )
        with pytest.raises(AttributeError):
            sheet.rows = 5

    def test_columns_is_read_only(self):
        """The columns property should not be writable."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 3,
                           rows        = 4,
                           )
        with pytest.raises(AttributeError):
            sheet.columns = 5
