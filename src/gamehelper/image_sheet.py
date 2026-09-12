import math

from PIL import Image

from .card_maker import CardMaker


class ImageSheet:
    """
    A sheet of cards rendered as an image.
    """

    def __init__(self,
                 card_width:  int,
                 card_height: int,
                 columns:     int                       = 1,
                 rows:        int | None                = None,
                 cards:       int | None                = None,
                 colour:      tuple[int, int, int, int] = (255, 255, 255, 255),
                 ) -> None:
        """
        A sheet of cards, white by default.

        Specify either 'rows' or 'cards' to set the grid height.
        If 'cards' is specified, rows is calculated as ceil(cards / columns).
        """
        if rows is not None and cards is not None:
            raise ValueError("Cannot specify both 'rows' and 'cards'")

        if cards is not None:
            rows = math.ceil(cards / columns)
        elif rows is None:
            rows = 1

        self._card_width     = card_width
        self._card_height    = card_height
        self._width          = card_width * columns
        self._height         = card_height * rows
        self._columns        = columns
        self._rows           = rows
        self._current_column = 0
        self._current_row    = 0
        self._base_im = Image.new(mode  = 'RGBA',
                                  size  = (self._width, self._height),
                                  color = colour,
                                  )

    @property
    def rows(self) -> int:
        """The number of rows in the sheet (read-only)."""
        return self._rows

    @property
    def columns(self) -> int:
        """The number of columns in the sheet (read-only)."""
        return self._columns

    def add(self, card: CardMaker | Image.Image | str) -> None:
        """
        Add the next card onto the sheet.
        `card` is a CardMaker, Image, or image filename.
        The image will exclude any gutters.
        In all cases the image will scale to fit the space.
        """

        slot_width  = int(self._width / self._columns)
        slot_height = int(self._height / self._rows)
        x_pos       = self._current_column * slot_width
        y_pos       = self._current_row * slot_height

        im = None
        if isinstance(card, CardMaker):
            im = card.image()
        elif isinstance(card, Image.Image):
            im = card
            im = im.convert('RGBA')
        elif isinstance(card, str):
            im = Image.open(card)
            im = im.convert('RGBA')
        else:
            raise TypeError(f"Can only an Image or CardMaker or str but got a {type(card)}")

        scaled_im   = im.resize(size = (self._card_width, self._card_height))
        self._base_im.paste(im   = scaled_im,
                           box  = (x_pos, y_pos),
                           mask = scaled_im,
                           )

        self._current_column = (self._current_column + 1) % self._columns
        if self._current_column == 0:
            self._current_row = self._current_row + 1


    def save(self, filename: str) -> None:
        """
        Write the sheet to the named file.
        """
        self._base_im.save(filename)
