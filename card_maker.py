from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops

from fpdf import FPDF

import copy
import pdf2image


class CardMaker:
    """
    A class that allows us to create a card image.
    """

    width  = None
    height = None

    def __init__(self,
                 width = None, height = None,
                 width_mm = None,
                 width_px = None,
                 gutter = 0,
                 image = None,
                 colour = (0, 0, 0, 0),    # Transparent background
                 unit = None,
                 ):
        """
        A maker for card with the given dimensions, excluding the gutter.
        (0, 0) is the top left of the card, excluding the gutter, and
        (width, height) is the bottom right of the card, excluding the gutter.
        Values are converted to ints.
        The cards will be transparent by default.
        We must specify the default unit of these and future length parameters.
        """

        if unit is None:
            raise ValueError('Must specify the unit being used')
        if not(unit in ['px', 'mm']):
            raise ValueError(f"Unit must be px or mm, but got '{unit}'")

        self._width    = int(width)
        self._height   = int(height)
        self._gutter   = int(gutter)
        self._unit     = unit

        self._width_px = width_px
        self._width_mm = width_mm
        self._set_unit_properties()

        if image is None:
            w_px = 2 * self._gutter_px + self._width_px
            h_px = 2 * self._gutter_px + self._height_px
            image = Image.new(mode = 'RGBA',
                              size = (int(w_px),
                                      int(h_px)),
                              color = colour,
                              )
        else:
            image = image.copy()

        self._im_with_gutters = image


    def _set_unit_properties(self):
        """
        Set the various _mm and _px properties appropriately
        """

        if self._width_px is None and self._width_mm is None:
            raise ValueError('Must specify width_mm or width_px')
        if not(self._width_px is None) and not(self._width_mm is None):
            raise ValueError('Cannot specify width of both mm and px')
        if self._unit == 'px' and not(self._width_px is None):
            raise ValueError('Cannot specify width_px when default unit is also px')
        if self._unit == 'mm' and not(self._width_mm is None):
            raise ValueError('Cannot specify width_mm when default unit is also mm')

        match self._unit:
            case 'px':
                px_per_mm = self._width / self._width_mm

                self._width_px  = self._width
                self._width_mm  = self._width_px / px_per_mm
                self._height_px = self._height
                self._height_mm = self._height_px / px_per_mm
                self._gutter_px = self._gutter
                self._gutter_mm = self._gutter_px / px_per_mm
            case 'mm':
                mm_per_px = self._width / self._width_px

                self._width_mm  = self._width
                self._width_px  = self._width_mm / mm_per_px
                self._height_mm = self._height
                self._height_px = self._height_mm / mm_per_px
                self._gutter_mm = self._gutter
                self._gutter_px = self._gutter_mm / mm_per_px
            case _:
                raise ValueError(f"Cannot convert from unit '{self._unit}'")


    def copy(self):
        """
        Create a copy of the object. Useful for when we have a base card with
        a border and we want to make lots of cards based on that
        """

        dup = copy.copy(self)
        dup._im_with_gutters = self._im_with_gutters.copy()

        return dup


    # ------------ Width -------------


    @property
    def width(self):
        """
        The width of the card, excluding gutters, in the default unit.
        """
        return self._width


    @property
    def width_px(self):
        """
        The width of the card, excluding gutters, in pixels.
        """
        return self._width_px


    @property
    def width_mm(self):
        """
        The width of the card, excluding gutters, in millimetres.
        """
        return self._width_mm


    @property
    def width_with_gutters(self):
        """
        The width of the card, including gutters, in the default unit.
        """
        return self._gutter + self._width + self._gutter


    @property
    def width_with_gutters_px(self):
        """
        The width of the card, including gutters, in pixels.
        """
        return self._gutter_px + self._width_px + self._gutter_px


    @property
    def width_with_gutters_mm(self):
        """
        The width of the card, including gutters, in millimetres.
        """
        return self._gutter_mm + self._width_mm + self._gutter_mm


    # ------------ Height -------------


    @property
    def height(self):
        """
        The height of the card, excluding gutters, in the default unit.
        """
        return self._height


    @property
    def height_px(self):
        """
        The height of the card, excluding gutters, in pixels.
        """
        return self._height_px


    @property
    def height_mm(self):
        """
        The height of the card, excluding gutters, in millimetres.
        """
        return self._height_mm


    @property
    def height_with_gutters(self):
        """
        The height of the card, including gutters, in the default unit.
        """
        return self._gutter + self._height + self._gutter


    @property
    def height_with_gutters_px(self):
        """
        The height of the card, including gutters, in pixels.
        """
        return self._gutter_px + self._height_px + self._gutter_px


    @property
    def height_with_gutters_mm(self):
        """
        The height of the card, including gutters, in millimetres.
        """
        return self._gutter_mm + self._height_mm + self._gutter_mm


    # ------------ Gutter -------------


    @property
    def gutter(self):
        """
        The gutter size of the card, in the default unit.
        """
        return self._gutter


    @property
    def gutter_px(self):
        """
        The gutter size of the card, in pixels.
        """
        return self._gutter_px


    @property
    def gutter_mm(self):
        """
        The gutter size of the card, in millimetres.
        """
        return self._gutter_mm


    # ------------ Size -------------


    @property
    def size(self):
        """
        The (width, height) of the card, excluding gutters, in the default unit.
        """
        return (self._width, self._height)


    @property
    def size_px(self):
        """
        The (width, height) of the card, excluding gutters, in pixels.
        """
        return (self._width_px, self._height_px)


    @property
    def size_mm(self):
        """
        The (width, height) of the card, excluding gutters, in millimetres.
        """
        return (self._width_mm, self._height_mm)


    @property
    def size_with_gutters(self):
        """
        The (width, height) of the card, including gutters, in the default unit.
        """
        return (self._gutter + self._width + self._gutter,
                self._gutter + self._height + self._gutter)


    @property
    def size_with_gutters_px(self):
        """
        The (width, height) of the card, including gutters, in pixels.
        """
        return (self._gutter_px + self._width_px + self._gutter_px,
                self._gutter_px + self._height_px + self._gutter_px)


    @property
    def size_with_gutters_mm(self):
        """
        The (width, height) of the card, including gutters, in millimetres.
        """
        return (self._gutter_mm + self._width_mm + self._gutter_mm,
                self._gutter_mm + self._height_mm + self._gutter_mm)


    # -------------------


    def to_px(self, x):
        """
        Convert from a number in the default unit to pixels.
        """
        if x is None:
            return None

        match self._unit:
            case 'px':
                return x
            case 'mm':
                return x * self._width_px / self._width_mm


    def paste(self,
              im,
              x_left = None, x_centre = None, x_right = None,
              y_top = None, y_middle = None, y_bottom = None):
        """
        Paste a given image onto the card; it will use itself as a mask.
        (0, 0) is the top left of the card, excluding the gutters.
        Units must be in the default unit.
        """

        # Switch to pixels

        x_left   = self.to_px(x_left)
        x_centre = self.to_px(x_centre)
        x_right  = self.to_px(x_right)
        y_top    = self.to_px(y_top)
        y_middle = self.to_px(y_middle)
        y_bottom = self.to_px(y_bottom)

        x_pos, y_pos = None, None

        if not(x_left is None):
            x_pos = x_left + self._gutter_px
        if not(x_right is None):
            x_pos = x_right - im.width + self._gutter_px
        if not(x_centre is None):
            x_pos = int(x_centre - int(im.width / 2)) + self._gutter_px

        if not(y_top is None):
            y_pos = y_top + self._gutter_px
        if not(y_bottom is None):
            y_pos = y_bottom - im.height + self._gutter_px
        if not(y_middle is None):
            y_pos = int(y_middle - (im.height / 2)) + self._gutter_px

        self._im_with_gutters.paste(im = im,
                                    box = (int(x_pos), int(y_pos)),
                                    mask = im,
                                    )

    def html(self,
             content,
             width_px, height_px,    # pixels
             ):
        """
        Render some HTML content in a box of the given width and height in pixels.
        """

        card_width_mm = 63
        card_width_px = self._width
        print(f"Card with is {card_width_px} px")
        px_per_mm     = card_width_px / card_width_mm

        box_width_mm  = width_px  / px_per_mm
        print(f"Box with is {box_width_mm} mm")
        box_height_mm = height_px / px_per_mm

        pdf = FPDF(format = (box_width_mm, box_height_mm))
        pdf.add_page()
        pdf.set_margin(0)
        pdf.write_html(content)
        byte_array = pdf.output()

        dots_per_mm = card_width_px / card_width_mm
        mm_per_in   = 25.4
        dots_per_in = dots_per_mm * mm_per_in
        print(f"Dots per mm = {dots_per_mm}")
        print(f"Dots per in = {dots_per_in}")

        ims = pdf2image.convert_from_bytes(pdf_file = byte_array,
                                           # transparent = True,
                                           # fmt = 'png',
                                           dpi = dots_per_in,
                                           )
        im = ims[0]    # First page. A PPMImage by defaul
        print(f"Image width is {im.width} px")

        im_ratio = im.height / im.width
        im = im.convert(mode = 'RGBA')
        # im = im.resize(size = (200, int(200 * im_ratio)))
        self.paste(im, x_left = 10, y_top = 10)


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
        x, y are relative to the top left of the card excluding the gutters.
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

        draw = ImageDraw.Draw(self._im_with_gutters)
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
            elif char == '\n':
                text = text[:i] + '\n' + text[i+1:]
                count = 0
            if count+1 == len:
                text = text[:space] + '\n' + text[space+1:]
                count = i - space

        return text


    def image(self):
        """
        Return the card image, excluding the gutters.
        """
        return self._im_with_gutters.crop(box = (self._gutter_px,
                                                 self._gutter_px,
                                                 self._gutter_px + self._width_px,
                                                 self._gutter_px + self._height_px,
                                                 ))


    def image_with_gutters(self):
        """
        Return the card image, including the gutters.
        """
        return self._im_with_gutters.copy()


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
