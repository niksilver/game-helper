from PIL import Image

from card_maker import CardMaker


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


    def add(self, card_or_im_or_file):
        """
        Add the next CardMaker or Image onto the sheet.
        The CardMaker image will exclude any gutters.
        In either case the image will scale to fit the space.
        """

        slot_width  = int(self._width / self._columns)
        slot_height = int(self._height / self._rows)
        x_pos       = self._current_column * slot_width
        y_pos       = self._current_row * slot_height

        im = None
        if isinstance(card_or_im_or_file, CardMaker):
            im = card_or_im_or_file.image()
        elif isinstance(card_or_im_or_file, Image.Image):
            im = card_or_im_or_file
            im = im.convert('RGBA')
        elif isinstance(card_or_im_or_file, str):
            im = Image.open(card_or_im_or_file)
            im = im.convert('RGBA')
        else:
            raise TypeError(f"Can only an Image or CardMaker but got a {type(card_or_im)}")

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
