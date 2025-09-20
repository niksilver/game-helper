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
        self.card_width     = card_width
        self.card_height    = card_height
        self.width          = card_width * columns
        self.height         = card_height * rows
        self.columns        = columns
        self.rows           = rows
        self.current_column = 0
        self.current_row    = 0
        self.base_im = Image.new(mode  = 'RGBA',
                                 size  = (self.width, self.height),
                                 color = colour,
                                 )


    def add(self, im):
        """
        Add the next card image onto the sheet.
        """

        slot_width  = int(self.width / self.columns)
        slot_height = int(self.height / self.rows)
        x_pos       = self.current_column * slot_width
        y_pos       = self.current_row * slot_height
        scaled_im   = im.resize(size = (self.card_width, self.card_height))
        self.base_im.paste(im   = scaled_im,
                           box  = (x_pos, y_pos),
                           mask = scaled_im,
                           )

        self.current_column = (self.current_column + 1) % self.columns
        if self.current_column == 0:
            self.current_row = self.current_row + 1


    def save(self, filename):
        """
        Write the sheet to the named file.
        """
        self.base_im.save(filename)
