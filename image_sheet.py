from PIL import Image


class ImageSheet:
    """
    A sheet of cards rendered as an image.
    """

    def __init__(self,
                 card_width = None, card_height = None,
                 columns = 1, rows = 1,
                 colour = (255, 255, 255, 255),    # Default white background
                 ):
        """
        A sheet of cards, white by default.
        """
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


    def add(self, im):
        """
        Add the next card image onto the sheet.
        """

        slot_width  = int(self._width / self._columns)
        slot_height = int(self._height / self._rows)
        x_pos       = self._current_column * slot_width
        y_pos       = self._current_row * slot_height
        scaled_im   = im.resize(size = (self._card_width, self._card_height))
        self._base_im.paste(im   = scaled_im,
                           box  = (x_pos, y_pos),
                           mask = scaled_im,
                           )

        self._current_column = (self._current_column + 1) % self._columns
        if self._current_column == 0:
            self._current_row = self._current_row + 1


    def save(self, filename):
        """
        Write the sheet to the named file.
        """
        self._base_im.save(filename)
