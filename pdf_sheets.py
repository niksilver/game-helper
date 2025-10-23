import math

from fpdf import FPDF
from PIL import Image


left_margin_fronts_page = 7
top_margin_fronts_page = 8
a4_short_length = 210
a4_long_length = 297


class PDFSheets:
    """
    PDF sheets of cards. Dimensions are in millimetres.
    """

    def __init__(self,
                 card_width,
                 card_height,
                 gutter = 4,
                 shape = 'rectangle',
                 include_backs = True,
                 ):
        """
        Create a new series of A4 sheets with cards, for printing.
        Shape may be "rectangle" (default) or "circle".
        By default card backs will be included on alternate sheets..
        """
        self.pdf = FPDF(orientation = 'landscape', unit = 'mm', format = 'A4')
        self.pdf.set_margin(0)

        self.card_width    = card_width
        self.card_height   = card_height
        self.gutter        = gutter
        self.shape         = shape
        self.include_backs = include_backs

        self.x = None
        self.y = None

        # Track card backs, a list of (image, x, y) tuples
        self.backs = []


    def _inc_xy(self):
        """
        Update the current x and y for a new card. May also trigger a
        new page.
        Returns True if a new page was triggered.
        """

        if self.x is None:
            self._add_page()
            return False

        # For convenience
        card_width  = self.card_width
        card_height = self.card_height
        gutter      = self.gutter

        # Move right
        self.x = self.x + gutter + card_width + gutter

        if self.x + gutter + card_width + gutter < a4_long_length:
            # The next card is within the bounds of the page
            return False

        # Move back to the left and down a line
        self.x = left_margin_fronts_page
        self.y = self.y + gutter + card_height + gutter

        if self.y + gutter + card_height + gutter < a4_short_length:
            # The next card is within the bounds of the page
            return False

        # Position ourselves at the top left of a new page
        self._add_page()
        return True


    def _last_xy(self):
        """
        True if the next card will need a new page.
        """
        full_width  = self.gutter + self.card_width + self.gutter
        full_height = self.gutter + self.card_height + self.gutter
        last_on_row    = (self.x + 2 * full_width)  > a4_long_length
        last_on_column = (self.y + 2 * full_height) > a4_short_length

        return last_on_row and last_on_column


    def _gutter_lines(self, x, y):
        """
        Draw little lines around the edge of a card positioned at x, y.
        These coordinates include the gutters.
        """

        # For convenience
        card_width  = self.card_width
        card_height = self.card_height
        gutter      = self.gutter

        self._gutter_h_line(x,                       y,                        gutter + card_width + gutter)
        self._gutter_h_line(x,                       y + gutter + card_height, gutter + card_width + gutter)
        self._gutter_v_line(x,                       y,                        gutter + card_height + gutter)
        self._gutter_v_line(x + gutter + card_width, y,                        gutter + card_height + gutter)


    def _gutter_h_line(self, x, y, width):
        """
        Draw a row of horizontal gutter marks with top left at x, y
        (which includes the gutters).
        """
        pdf = self.pdf
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.25)

        gap = 1    # Gap either side of the marks

        for delta in range(0, width, self.gutter):
            pdf.line(x1 = x + delta, y1 = y + gap, x2 = x + delta, y2 = y + self.gutter - gap)


    def _gutter_v_line(self, x, y, height):
        """
        Draw a row of vertical gutter marks with top left at x, y
        (which includes the gutters).
        """
        pdf = self.pdf
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.25)

        gap = 1    # Gap either side of the marks

        for delta in range(0, height, self.gutter):
            pdf.line(x1 = x + gap, y1 = y + delta, x2 = x + self.gutter - gap, y2 = y + delta)


    def _zero_gutter_edges(self, x, y):
        """
        Draw a line around the edge of the card card positioned at x, y.
        This should only be used when the gutter size is zero (no gutter).
        """

        # For convenience
        w   = self.card_width
        h   = self.card_height

        self.pdf.line(x1 = x,     y1 = y,     x2 = x + w, y2 = y)
        self.pdf.line(x1 = x + w, y1 = y,     x2 = x + w, y2 = y + h)
        self.pdf.line(x1 = x + w, y1 = y + h, x2 = x,     y2 = y + h)
        self.pdf.line(x1 = x,     y1 = y + h, x2 = x,     y2 = y)


    def _gutter_ring(self, x, y):
        """
        Draw all the gutter ring at the corner of a card positioned at x, y.
        These coordinates include the gutters.
        """

        # For convenience
        gutter = self.gutter
        pdf    = self.pdf

        centre_x = x + (gutter + self.card_width + gutter) // 2
        centre_y = y + (gutter + self.card_height + gutter) // 2
        r1       = self.card_width // 2
        r2       = r1 + gutter


        for i in range(0, 40):
            radians = 2 * math.pi / 40 * i

            pdf.line(x1 = centre_x + r1 * math.sin(radians),
                     y1 = centre_y + r1 * math.cos(radians),
                     x2 = centre_x + r2 * math.sin(radians),
                     y2 = centre_y + r2 * math.cos(radians),
                     )


    def _gutter_marks(self, x, y):
        """
        Add the gutter marks, which will be either corners for a rectangle or
        a ring for a circle.
        """
        if self.shape == 'rectangle' and self.gutter > 0:
            self._gutter_lines(x, y)
        elif self.shape == 'rectangle' and self.gutter == 0:
            self._zero_gutter_edges(x, y)
        elif self.shape == 'circle':
            self._gutter_ring(x,y)
        else:
            raise ValueError(f'Shape defined as unknown "{self.shape}"')


    def _reflect(self, image_or_file):
        """
        Reflect an image east-west.
        """
        im = image_or_file
        if isinstance(im, str):
            im = Image.open(image_or_file)

        # Data drawn from
        # https://pillow.readthedocs.io/en/stable/reference/ImageTransform.html#PIL.ImageTransform.AffineTransform
        return im.transform(size = (im.width, im.height),
                            method = Image.Transform.AFFINE,
                            data = (-1, 0, im.width, 0, 1, 0),
                            )


    def add(self,
            image_or_file,
            x_offset = 0,
            y_offset = 0,
            back_image_or_file = None,
            ):
        """
        Add an image to the card, offset from the origin, which includes the gutters.
        The image will be centred.
        The back image/file may be None.
        """
        im_width  = self.card_width  + 2*self.gutter - 2*x_offset
        im_height = self.card_height + 2*self.gutter - 2*y_offset
        self._inc_xy()
        self.pdf.image(image_or_file,
                       x = self.x + x_offset,
                       y = self.y + y_offset,
                       w = im_width,
                       h = im_height,
                       )
        self._gutter_marks(self.x, self.y)
        self.backs.append((back_image_or_file, self.x, self.y))

        if self._last_xy():
            self.add_backs_page()


    def add_backs_page(self):
        """
        Add a new page of card backs.
        This will normally be called as part of the add() process, but the
        user will need to call it themselves at after adding the last card.
        """

        # This will trigger a new page
        self.x = None
        self.y = None

        if self.include_backs:
            for im_x_y in self.backs:
                self._add_back(im_x_y[0], im_x_y[1], im_x_y[2])

        self.backs = []


    def _add_back(self, image_or_file, x, y):
        """
        Add a card back to the PDF, which includes the gutters.
        The x,y is the position of the card front, so we need to flip this page.
        """

        # For convenience
        card_width  = self.card_width
        card_height = self.card_height
        gutter      = self.gutter

        self._inc_xy()
        x_origin = a4_long_length / 2
        y_origin = a4_short_length / 2

        # We need to mirror the whole page, then mirror each card back again
        with self.pdf.mirror(origin = (x_origin, y_origin), angle = 'EAST'):
            if not(image_or_file is None):
                reflected_im = self._reflect(image_or_file)
                self.pdf.image(reflected_im,
                               x = self.x,
                               y = self.y, 
                               w = gutter + card_width + gutter,
                               h = gutter + card_height + gutter
                               )
            self._gutter_marks(self.x, self.y)


    def _add_page(self):
        """
        Add a next page to the PDF and reset our x, y position.
        """
        self.pdf.add_page()
        self.x = left_margin_fronts_page
        self.y = top_margin_fronts_page


    def output(self, filename):
        """
        Write the PDF sheets to the given file.
        """
        self.pdf.output(filename)
