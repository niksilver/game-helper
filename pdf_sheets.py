from fpdf import FPDF


left_margin_fronts_page = 10
top_margin_fronts_page = 10
a4_short_length = 210
a4_long_length = 297


class PDFSheets:
    """
    PDF sheets of cards. Dimensions are in millimetres.
    """

    def __init__(self,
                 card_width,
                 card_height,
                 gutter = 4):
        """
        Create a new series of A4 sheets with cards, for printing.
        """
        self.pdf = FPDF(orientation = 'landscape', unit = 'mm', format = 'A4')
        self.pdf.set_margin(0)

        self.card_width  = card_width
        self.card_height = card_height
        self.gutter      = gutter

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


    def _gutter_square(self, x, y):
        """
        Draw a square for cutting at x, y.
        """
        pdf = self.pdf
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.25)

        gap   = 1    # Gap at edge of each square
        x_lhs = x
        x_rhs = x + self.gutter
        y_top = y
        y_bot = y + self.gutter

        pdf.line(x1 = x_lhs + gap , y1 = y_top       , x2 = x_rhs - gap , y2 = y_top)
        pdf.line(x1 = x_rhs       , y1 = y_top + gap , x2 = x_rhs       , y2 = y_bot - gap)
        pdf.line(x1 = x_lhs + gap , y1 = y_bot       , x2 = x_rhs - gap , y2 = y_bot)
        pdf.line(x1 = x_lhs       , y1 = y_top + gap , x2 = x_lhs       , y2 = y_bot - gap)


    def _gutter_corners(self, x, y):
        """
        Draw all the gutter squares at the corner of a card positioned at x, y.
        """

        # For convenience
        card_width  = self.card_width
        card_height = self.card_height
        gutter      = self.gutter

        self._gutter_square(x                       , y)
        self._gutter_square(x + gutter + card_width , y)
        self._gutter_square(x + gutter + card_width , y + gutter + card_height)
        self._gutter_square(x                       , y + gutter + card_height)


    def add(self,
            image_or_file,
            x_offset = 0,
            y_offset = 0,
            back_image_or_file = None,
            ):
        """
        Add an image to the card, offset from the origin, which includes the gutters.
        The back image/file may be None.
        """
        self._inc_xy()
        self.pdf.image(image_or_file,
                       x = self.x + x_offset,
                       y = self.y + y_offset,
                       w = self.card_width,
                       h = self.card_height,
                       )
        self._gutter_corners(self.x, self.y)
        self.backs.append((back_image_or_file, self.x, self.y))

        if self._last_xy():
            self.add_backs()


    def add_backs(self):
        """
        Add a new pack of card backs.
        This will normally be called as part of the add() process, but the
        user will need to call it themselves at after adding the last card.
        """

        # This will trigger a new page
        self.x = None
        self.y = None

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
        with self.pdf.mirror(origin = (x_origin, y_origin), angle = 'EAST'):
            if not(image_or_file is None):
                self.pdf.image(image_or_file,
                               x = self.x,
                               y = self.y, 
                               w = gutter + card_width + gutter,
                               h = gutter + card_height + gutter
                               )
            self._gutter_corners(self.x, self.y)


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
