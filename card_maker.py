from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops

from fpdf import FPDF

import pdf2image


class CardMaker:
    """
    A class that allows us to create a card image.
    """

    width  = None
    height = None

    def __init__(self,
                 width = None, height = None,
                 gutter = 0,
                 image = None,
                 colour = (0, 0, 0, 0)    # Transparent background
                 ):
        """
        A maker for card with the given dimensions, excluding the gutter.
        (0, 0) is the top left of the card, excluding the gutter, and
        (width, height) is the bottom right of the card, excluding the gutter.
        Values are converted to ints.
        The cards will be transparent by default.
        """
        self._width  = int(width)
        self._height = int(height)
        self._gutter = int(gutter)

        if image is None:
            image = Image.new(mode = 'RGBA',
                              size = (2 * self._gutter + self._width,
                                      2 * self._gutter + self._height),
                              color = colour,
                              )
        else:
            image = image.copy()

        self._card_im = image


    @property
    def width(self):
        """
        The width of the card, including gutters.
        """
        return self._width


    @property
    def height(self):
        """
        The height of the card, including gutters.
        """
        return self._height


    @property
    def gutter(self):
        """
        The gutter size of the card.
        """
        return self._gutter


    def paste(self,
              im,
              x_left = None, x_centre = None, x_right = None,
              y_top = None, y_middle = None, y_bottom = None):
        """
        Paste a given image onto the card; it will use itself as a mask.
        """
        x_pos, y_pos = None, None

        if not(x_left is None):
            x_pos = x_left + self._gutter
        if not(x_right is None):
            x_pos = x_right - im.width + self._gutter
        if not(x_centre is None):
            x_pos = int(x_centre - int(im.width / 2)) + self._gutter

        if not(y_top is None):
            y_pos = y_top + self._gutter
        if not(y_bottom is None):
            y_pos = y_bottom - im.height + self._gutter
        if not(y_middle is None):
            y_pos = int(y_middle - (im.height / 2)) + self._gutter

        self._card_im.paste(im = im,
                           box = (int(x_pos), int(y_pos)),
                           mask = im,
                           )

    def html(self,
             content,
             ):
        pdf = FPDF()
        pdf.add_page()
        pdf.write_html(content)
        byte_array = pdf.output()
        print(f"Length of pdf byte arrage is {len(byte_array)}")

        ims = pdf2image.convert_from_bytes(pdf_file = byte_array)
        # ims = pdf2image.convert_from_path(pdf_path = 'tmp.pdf')
        print(f"Type of ims is {type(ims)}")
        print(f"Length of ims is {len(ims)}")
        print(f"Type of ims[0] is {type(ims[0])}")
        # print(f"Length of ims[0] is {len(ims[0])}")
        im = ims[0]
        print(f"Image is {im.width} x {im.height}")
        im = im.convert(mode = 'RGBA')
        self.paste(im, x_left = 0, y_top = 0)


    def text(self,
             text = "Default",
             x_left = None, x_centre = None, x_right = None,
             y_ascender = None, y_top = None, y_middle = None,
             y_baseline = None, y_bottom = None, y_descender = None,
             fill = (0, 0, 0),
             font = None,
             spacing = 4,
             chrs_per_line = None,
             ):
        """
        Add some text to the card.
        The font must be an ImageFont object.
        If given, newlines will be inserted at chrs_per_line
        Returns the bounding box, as per
        https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textbbox
        This is relative to the top of the card content, excluding the gutter.
        """
        x_pos, y_pos       = None, None
        h_anchor, v_anchor = None, None
        align              = None

        if not(x_left is None):
            x_pos    = x_left + self._gutter
            h_anchor = "l"
            align    = "left"
        if not(x_centre is None):
            x_pos    = x_centre + self._gutter
            h_anchor = "m"
            align    = "center"
        if not(x_right is None):
            x_pos    = x_right + self._gutter
            h_anchor = "r"
            align    = "right"
        
        if not(y_ascender is None):
            y_pos    = y_ascender + self._gutter
            v_anchor = "a"
        if not(y_top is None):
            y_pos    = y_top + self._gutter
            v_anchor = "t"
        if not(y_middle is None):
            y_pos    = y_middle + self._gutter
            v_anchor = "m"
        if not(y_baseline is None):
            y_pos    = y_baseline + self._gutter
            v_anchor = "s"
        if not(y_bottom is None):
            y_pos    = y_bottom + self._gutter
            v_anchor = "b"
        if not(y_descender is None):
            y_pos    = y_descender + self._gutter
            v_anchor = "d"

        if chrs_per_line:
            text = self._insert_new_lines(text, chrs_per_line)

        draw = ImageDraw.Draw(self._card_im)
        draw.text(xy      = (int(x_pos), int(y_pos)),
                  anchor  = h_anchor + v_anchor,
                  text    = text,
                  fill    = fill,
                  font    = font,
                  align   = align,
                  spacing = spacing,
                  )
        bbox = draw.textbbox(xy      = (int(x_pos), int(y_pos)),
                             anchor  = h_anchor + v_anchor,
                             text    = text,
                             font    = font,
                             align   = align,
                             spacing = spacing,
                             )
        return (bbox[0] - self._gutter,
                bbox[1] - self._gutter,
                bbox[2] - self._gutter,
                bbox[3] - self._gutter)


    @staticmethod
    def _insert_new_lines(text, len):
        """
        Given a text string and a line length, replace spaces with new line
        characters to fit the length.
        """
        space = 0    # Index of last space
        count = 0    # Number of characters consumed

        for i, char in enumerate(text):
            count = count + 1
            if char == ' ':
                space = i
            if count+1 == len:
                text = text[:space] + '\n' + text[space+1:]
                count = i - space

        return text


    def image(self):
        """
        Return the card image.
        This includes the gutters, so if the gutter is > 0 then its width
        and height will be greater than the width and height originally given.
        """
        return self._card_im


    def colour_wash(self, colour):
        """
        Give the image on the card a wash of colour.
        Transparency will be preserved.
        """

        self._card_im = self.colour_wash_image(self._card_im, colour)


    @staticmethod
    def colour_wash_image(image, colour):
        """
        DEPRECATED!
        Take an image and give it a colour wash.
        Transparency will be preserved.
        """
        wash_im = Image.new(mode = 'RGBA',
                            size = image.size,
                            color = colour,
                            )
        washed_im = ImageChops.add(image, wash_im, scale = 2)

        base_im = Image.new(mode = 'RGBA',
                            size = image.size,
                            color = (0, 0, 0, 0),
                            )
        base_im.paste(im = washed_im,
                      box = (0, 0),
                      mask = image)

        return base_im
