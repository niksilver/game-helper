import copy
import io

from   PIL       import Image
from   PIL       import ImageDraw
from   PIL       import ImageFont
from   PIL       import ImageChops
from   fpdf      import FPDF
import pdf2image
import cairosvg


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

        self._width    = width
        self._height   = height
        self._gutter   = gutter
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

                self._width_px  = int(self._width)
                self._width_mm  =     self._width_px / px_per_mm
                self._height_px = int(self._height)
                self._height_mm =     self._height_px / px_per_mm
                self._gutter_px = int(self._gutter)
                self._gutter_mm =     self._gutter_px / px_per_mm
            case 'mm':
                mm_per_px = self._width / self._width_px

                self._width_mm  =     self._width
                self._width_px  = int(self._width_mm / mm_per_px)
                self._height_mm =     self._height
                self._height_px = int(self._height_mm / mm_per_px)
                self._gutter_mm =     self._gutter
                self._gutter_px = int(self._gutter_mm / mm_per_px)
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
        The width of the card, excluding gutters, in pixels as an int.
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
        The height of the card, excluding gutters, in pixels as an int.
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


    def to_mm(self, x):
        """
        Convert from a number in the default unit to mm.
        """
        if x is None:
            return None

        match self._unit:
            case 'mm':
                return x
            case 'px':
                return x * self._width_mm / self._width_px


    def from_px(self, x):
        """
        Convert from some number of pixels to the default unit.
        """
        if x is None:
            return None

        match self._unit:
            case 'px':
                return x
            case 'mm':
                return x * self._width_mm / self._width_px


    # -------------------


    def load_image(self,
                   filename,
                   size = None, width = None, height = None,
                   ):
        """
        Load an image from a file, possibly resize it, and return it.
        If `filename` points to an SVG it will be converted to a PNG.

        Units should be in the default unit.
        `im` may be an Image object or a filename.
        (If it's a filename it may be an SVG.)
        `size`, `width` and `height` are all optional.
        `size` is a (width, height) pair.
        If only `width` or `height` is given then the image will scale
        proportionally.

        The returned image will be RGBA.
        """

        # Make sure im is an Image in the correct format

        im     = None
        is_svg = False

        if filename[-4:] == '.svg':
            is_svg   = True
            b_string = cairosvg.svg2png(url = filename)
            b_io     = io.BytesIO(b_string)
            im       = Image.open(b_io)
            im       = im.convert('RGBA')

        else:
            im = Image.open(filename)
            im = im.convert('RGBA')

        # We may need to resize it.
        # If it's an SVG we have to resize it as we (re)load it.
        # Inconveniently, the SVG converter will only scale it in either the
        # x or y dimension, so the resizing has to be done separately.

        (resize, size_px) = self.need_resize_px(im, size, width, height)

        if resize and is_svg:
            max_size = max(size_px)
            b_string = cairosvg.svg2png(url           = filename,
                                        output_width  = size_px[0],
                                        output_height = size_px[1],
                                        )
            b_io = io.BytesIO(b_string)
            im   = Image.open(b_io)
            im   = im.convert('RGBA')

        elif resize:
            # NB: Suspected error here! size is not necessarily in px.
            im = im.resize(size = size_px)

        return im


    def paste(self,
              im_or_filename,
              size = None, width = None, height = None,
              x_left = None, x_centre = None, x_right = None,
              y_top = None, y_middle = None, y_bottom = None):
        """
        Paste a given image onto the card; it will use itself as a mask.
        (0, 0) is the top left of the card, excluding the gutters.

        See `load_image` for explanation of
        `size`, `width` and `height` parameters.
        """

        # Make sure we have an Image and it's the specified size.

        im = None
        if type(im_or_filename) == str:
            filename = im_or_filename
            im       = self.load_image(filename, size, width, height)

        else:
            im = im_or_filename
            (resize, size_px) = self.need_resize_px(im, size, width, height)
            if resize:
                im = im.resize(size = size_px)

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

        # Paste the image in the right place

        self._im_with_gutters.paste(im = im,
                                    box = (int(x_pos), int(y_pos)),
                                    mask = im,
                                    )

    def need_resize_px(self, im, size = None, width = None, height = None):
        """
        Decide if an image should be resized, and what its new dimensions
        should be, in pixels.
        Only one of `size`, `width` and `height` is needed, and the dimensions
        are the default dimensions of the object.
        If only `width` or `height` is specified the resizing will be a
        proportional scaling.

        Returns (flag, (width, height)) where flag is if it requires resizing.
        """
        # Convert to pixels

        if size is not None:
            size = (int(self.to_px(size[0])),
                    int(self.to_px(size[1])) )
        if width is not None:
            width = int(self.to_px(width))
        if height is not None:
            height = int(self.to_px(height))

        # Switch the values into width and height only (either may be None)

        if size is not None:
            (width, height) = size

        # Should we resize?

        resize = False
        if (width is not None) and im.width != width:
            resize = True
        if (height is not None) and im.height != height:
            resize = True

        # Calculate desired width and height

        if (width is None) and (height is None):
            return (resize, im.size)

        if (width is not None) and (height is None):
            height = im.height * (width / im.width)

        if (width is None) and (height is not None):
            width = im.width * (height / im.height)

        return (resize, (int(width), int(height)))


    def html(self,
             content,
             x_left, y_top,
             width, height,
             ):
        """
        Render some HTML content in a box of the given size.
        """

        box_width_mm  = self.to_mm(width)
        box_height_mm = self.to_mm(height)

        pdf = FPDF(format = (box_width_mm, box_height_mm))
        pdf.add_page()
        pdf.set_margin(0)
        pdf.write_html(content)
        byte_array = pdf.output()

        dots_per_mm = self._width_px / self._width_mm
        mm_per_in   = 25.4
        dots_per_in = dots_per_mm * mm_per_in

        ims = pdf2image.convert_from_bytes(pdf_file = byte_array,
                                           transparent = True,
                                           fmt = 'png',
                                           dpi = dots_per_in,
                                           )
        im = ims[0]    # First page. A PPMImage by default

        im_ratio = im.height / im.width
        im = im.convert(mode = 'RGBA')
        self.paste(im,
                   x_left = x_left,
                   y_top = y_top,
                   )


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
        but in the default unit.
        This is relative to the top of the card content, excluding the gutter.
        """

        # Switch to pixels

        x_left        = self.to_px(x_left)
        x_centre      = self.to_px(x_centre)
        x_right       = self.to_px(x_right)
        y_ascender    = self.to_px(y_ascender)
        y_top         = self.to_px(y_top)
        y_middle      = self.to_px(y_middle)
        y_baseline    = self.to_px(y_baseline)
        y_bottom      = self.to_px(y_bottom)
        y_descender   = self.to_px(y_descender)

        x_pos, y_pos       = None, None
        h_anchor, v_anchor = None, None
        align              = None

        if not(x_left is None):
            x_pos    = x_left + self._gutter_px
            h_anchor = "l"
            align    = "left"
        if not(x_centre is None):
            x_pos    = x_centre + self._gutter_px
            h_anchor = "m"
            align    = "center"
        if not(x_right is None):
            x_pos    = x_right + self._gutter_px
            h_anchor = "r"
            align    = "right"
        
        if not(y_ascender is None):
            y_pos    = y_ascender + self._gutter_px
            v_anchor = "a"
        if not(y_top is None):
            y_pos    = y_top + self._gutter_px
            v_anchor = "t"
        if not(y_middle is None):
            y_pos    = y_middle + self._gutter_px
            v_anchor = "m"
        if not(y_baseline is None):
            y_pos    = y_baseline + self._gutter_px
            v_anchor = "s"
        if not(y_bottom is None):
            y_pos    = y_bottom + self._gutter_px
            v_anchor = "b"
        if not(y_descender is None):
            y_pos    = y_descender + self._gutter_px
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
        return (self.from_px(bbox[0] - self._gutter_px),
                self.from_px(bbox[1] - self._gutter_px),
                self.from_px(bbox[2] - self._gutter_px),
                self.from_px(bbox[3] - self._gutter_px),
                )


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
        Give the card a wash of colour.
        Transparency will be preserved.
        """

        self._im_with_gutters = self.colour_wash_image(self._im_with_gutters, colour)


    @staticmethod
    def colour_wash_image(im, colour):
        """
        Give an image a wash of colour.
        Transparency will be preserved.
        """
        wash_im = Image.new(mode = 'RGBA',
                            size = im.size,
                            color = colour,
                            )
        washed_im = ImageChops.add(im, wash_im, scale = 2)

        base_im = Image.new(mode = 'RGBA',
                            size = im.size,
                            color = (0, 0, 0, 0),
                            )
        base_im.paste(im = washed_im,
                      box = (0, 0),
                      mask = im)

        return base_im
