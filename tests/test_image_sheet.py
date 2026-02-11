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
        assert sheet._rows == 2

    def test_cards_calculates_rows_rounds_up(self):
        """When cards doesn't divide evenly, rows rounds up."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 3,
                           cards       = 7,
                           )
        assert sheet._rows == 3

    def test_cards_single_column(self):
        """With 1 column, rows equals cards."""
        sheet = ImageSheet(card_width  = 100,
                           card_height = 100,
                           columns     = 1,
                           cards       = 5,
                           )
        assert sheet._rows == 5

    def test_cards_and_rows_raises_error(self):
        """Specifying both cards and rows should raise an error."""
        with pytest.raises(ValueError):
            ImageSheet(card_width  = 100,
                       card_height = 100,
                       columns     = 2,
                       rows        = 3,
                       cards       = 6,
                       )
