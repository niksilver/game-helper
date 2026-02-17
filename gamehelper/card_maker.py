import copy
import io

from   PIL              import Image
from   PIL              import ImageDraw
from   PIL              import ImageFont
from   PIL              import ImageChops
from   fpdf             import FPDF
from   html2image       import Html2Image
import cairosvg
from   gamehelper.utils import optimise


class CardMaker:
    """
    A class that allows us to create a card image.
    """

    width  = None
    height = None

    _DEFAULT_TEXT_LINE_SPACING_MM = 1.5

    def __init__(self,
                 width:    float,
                 height:   float,
                 width_mm: float | None               = None,
                 width_px: int | None                 = None,
                 gutter:   float                      = 0,
                 image:    Image.Image | None         = None,
                 colour:   tuple[int, int, int, int]  = (0, 0, 0, 0),
                 unit:     str | None                 = None,
                 ) -> None:
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
        self._width_px = width_px
        self._width_mm = width_mm

        self._height   = height
        self._gutter   = gutter
        self._unit     = unit

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
        self._html2image      = None
        self._font_families   = {}

        # Set default text line spacing (1.5mm in the default unit)
        default_spacing_px      = self._DEFAULT_TEXT_LINE_SPACING_MM * self._width_px / self._width_mm
        self._text_line_spacing = self.from_px(default_spacing_px)


    def _set_unit_properties(self) -> None:
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


    def copy(self) -> 'CardMaker':
        """
        Create a copy of the object. Useful for when we have a base card with
        a border and we want to make lots of cards based on that
        """

        dup = copy.copy(self)
        dup._im_with_gutters = self._im_with_gutters.copy()

        return dup


    # ------------ Width -------------


    @property
    def width(self) -> float:
        """
        The width of the card, excluding gutters, in the default unit.
        """
        return self._width


    @property
    def width_px(self) -> int:
        """
        The width of the card, excluding gutters, in pixels as an int.
        """
        return self._width_px


    @property
    def width_mm(self) -> float:
        """
        The width of the card, excluding gutters, in millimetres.
        """
        return self._width_mm


    @property
    def width_with_gutters(self) -> float:
        """
        The width of the card, including gutters, in the default unit.
        """
        return self._gutter + self._width + self._gutter


    @property
    def width_with_gutters_px(self) -> int:
        """
        The width of the card, including gutters, in pixels.
        """
        return self._gutter_px + self._width_px + self._gutter_px


    @property
    def width_with_gutters_mm(self) -> float:
        """
        The width of the card, including gutters, in millimetres.
        """
        return self._gutter_mm + self._width_mm + self._gutter_mm


    # ------------ Height -------------


    @property
    def height(self) -> float:
        """
        The height of the card, excluding gutters, in the default unit.
        """
        return self._height


    @property
    def height_px(self) -> int:
        """
        The height of the card, excluding gutters, in pixels as an int.
        """
        return self._height_px


    @property
    def height_mm(self) -> float:
        """
        The height of the card, excluding gutters, in millimetres.
        """
        return self._height_mm


    @property
    def height_with_gutters(self) -> float:
        """
        The height of the card, including gutters, in the default unit.
        """
        return self._gutter + self._height + self._gutter


    @property
    def height_with_gutters_px(self) -> int:
        """
        The height of the card, including gutters, in pixels.
        """
        return self._gutter_px + self._height_px + self._gutter_px


    @property
    def height_with_gutters_mm(self) -> float:
        """
        The height of the card, including gutters, in millimetres.
        """
        return self._gutter_mm + self._height_mm + self._gutter_mm


    # ------------ Size -------------


    @property
    def size(self) -> tuple[float, float]:
        """
        The (width, height) of the card, excluding gutters, in the default unit.
        """
        return (self._width, self._height)


    @property
    def size_px(self) -> tuple[int, int]:
        """
        The (width, height) of the card, excluding gutters, in pixels.
        """
        return (self._width_px, self._height_px)


    @property
    def size_mm(self) -> tuple[float, float]:
        """
        The (width, height) of the card, excluding gutters, in millimetres.
        """
        return (self._width_mm, self._height_mm)


    @property
    def size_with_gutters(self) -> tuple[float, float]:
        """
        The (width, height) of the card, including gutters, in the default unit.
        """
        return (self._gutter + self._width + self._gutter,
                self._gutter + self._height + self._gutter)


    @property
    def size_with_gutters_px(self) -> tuple[int, int]:
        """
        The (width, height) of the card, including gutters, in pixels.
        """
        return (self._gutter_px + self._width_px + self._gutter_px,
                self._gutter_px + self._height_px + self._gutter_px)


    @property
    def size_with_gutters_mm(self) -> tuple[float, float]:
        """
        The (width, height) of the card, including gutters, in millimetres.
        """
        return (self._gutter_mm + self._width_mm + self._gutter_mm,
                self._gutter_mm + self._height_mm + self._gutter_mm)


    # ------------ Gutter -------------


    @property
    def gutter(self) -> float:
        """
        The gutter size of the card, in the default unit.
        """
        return self._gutter


    @property
    def gutter_px(self) -> int:
        """
        The gutter size of the card, in pixels.
        """
        return self._gutter_px


    @property
    def gutter_mm(self) -> float:
        """
        The gutter size of the card, in millimetres.
        """
        return self._gutter_mm


    # ------------ Text line spacing -------------


    @property
    def text_line_spacing(self) -> float:
        """
        The line spacing for text, in the default unit.
        """
        return self._text_line_spacing

    @text_line_spacing.setter
    def text_line_spacing(self, value: float | None) -> None:
        """
        Set the line spacing for text, in the default unit.
        Setting to None reverts to the default (1.5mm equivalent).
        """
        if value is None:
            default_spacing_px      = self._DEFAULT_TEXT_LINE_SPACING_MM * self._width_px / self._width_mm
            self._text_line_spacing = self.from_px(default_spacing_px)
        else:
            self._text_line_spacing = value

    @property
    def text_line_spacing_mm(self) -> float:
        """
        The line spacing for text, in millimetres.
        """
        return self.to_mm(self._text_line_spacing)

    @text_line_spacing_mm.setter
    def text_line_spacing_mm(self, value: float | None) -> None:
        """
        Set the line spacing for text, in millimetres.
        Setting to None reverts to the default (1.5mm).
        """
        if value is None:
            self.text_line_spacing = None
        else:
            match self._unit:
                case 'mm':
                    self._text_line_spacing = value
                case 'px':
                    self._text_line_spacing = value * self._width_px / self._width_mm

    @property
    def text_line_spacing_px(self) -> float:
        """
        The line spacing for text, in pixels.
        """
        return self.to_px(self._text_line_spacing)

    @text_line_spacing_px.setter
    def text_line_spacing_px(self, value: float | None) -> None:
        """
        Set the line spacing for text, in pixels.
        Setting to None reverts to the default (1.5mm equivalent).
        """
        if value is None:
            self.text_line_spacing = None
        else:
            match self._unit:
                case 'px':
                    self._text_line_spacing = value
                case 'mm':
                    self._text_line_spacing = value * self._width_mm / self._width_px


    # -------------------


    def to_px(self, x: float | None) -> float | None:
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


    def to_mm(self, x: float | None) -> float | None:
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


    def from_px(self, x: float | None) -> float | None:
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


    def from_mm(self, x: float | None) -> float | None:
        """
        Convert from some number of millimetres to the default unit.
        """
        if x is None:
            return None

        match self._unit:
            case 'mm':
                return x
            case 'px':
                return x * self._width_px / self._width_mm


    # -------------------


    def load_image(self,
                   filename: str,
                   size:     tuple[float, float] | None = None,
                   width:    float | None               = None,
                   height:   float | None               = None,
                   ) -> Image.Image:
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
              im_or_filename: Image.Image | str,
              size:           tuple[float, float] | None = None,
              width:          float | None               = None,
              height:         float | None               = None,
              x_left:         float | None               = None,
              x_centre:       float | None               = None,
              x_right:        float | None               = None,
              y_top:          float | None               = None,
              y_middle:       float | None               = None,
              y_bottom:       float | None               = None,
              ) -> None:
        """
        Paste a given image onto the card; it will use itself as a mask.
        (0, 0) is the top left of the card, excluding the gutters.

        See `load_image` for explanation of
        `size`, `width` and `height` parameters.
        """

        # Require the correct x and y arguments

        x_vals = [x_left, x_centre, x_right]
        y_vals = [y_top, y_middle, y_bottom]

        def count_vals(s):
            count = 0
            for val in s:
                if val is not None: count = count + 1
            return count

        x_count = count_vals([x_left, x_centre, x_right])
        if x_count != 1:
            raise ValueError(f"Must specify exactly one of "
                             f"x_left, x_centre, x_right but got {x_count}")

        y_count = count_vals([y_top, y_middle, y_bottom])
        if y_count != 1:
            raise ValueError(f"Must specify exactly one of "
                             f"y_top, y_middle, y_bottom but got {y_count}")

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

    def need_resize_px(self,
                       im:     Image.Image,
                       size:   tuple[float, float] | None = None,
                       width:  float | None               = None,
                       height: float | None               = None,
                       ) -> tuple[bool, tuple[int, int]]:
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


    def font_families(self, families: dict[str, str]) -> None:
        """
        Register font families for use in `html()`.
        Each key is a font family name and its value is the path to the font file.
        """
        self._font_families = families

    def _get_HTML2Image(self) -> Html2Image:
        """
        Get (or set up) our reusable instance of HTML2Image, including its
        connection to the browser.
        """
        if not(self._html2image):
            self._html2image = Html2Image(browser = 'google-chrome',
                                          )
            self._html2image.output_path = self._html2image.temp_path
            self._html2image.browser.print_command   = False
            self._html2image.browser.disable_logging = True

        return self._html2image


    def html(self,
             content:     str,
             left:        float,
             top:         float,
             width:       float,
             height:      float        = None,
             h_align:     str | None   = None,
             v_align:     str | None   = None,
             font_size:   float | None = None,
             font_family: str | None   = None,
             ) -> None:
        """
        Render some HTML content in a box of the given size.
        As usual, all lengths are in the default unit.
        The height defaults to the maximum available from the
        `top` to the bottom of the card including the gutter.
        `font_family` sets the document font family (must be registered
        via `font_families()` if it's a custom font).

        Rendering HTML is slower than the `text()` method if that's all you want,
        but it may be more convenient to manage.
        """

        if not(height):
            height = self.height_with_gutters - top - self.gutter

        font_size_css   = f'font-size:      {self.to_px(font_size)};' if font_size   else ""
        font_family_css = f"font-family:    '{font_family}';"         if font_family else ""
        h_align_css     = f'text-align:     {h_align};'               if h_align     else ""
        v_align_css     = f'vertical-align: {v_align};'               if v_align     else ""

        font_face_css = []
        for name, path in self._font_families.items():
            font_face_css.append(f"@font-face {{ font-family: '{name}'; "
                                 f"src: url('{path}'); }}")

        width_px  = int(self.to_px(width))
        height_px = int(self.to_px(height))

        hti      = self._get_HTML2Image()
        out_path = hti.screenshot(html_str = content,
                                  size     = (width_px, height_px),
                                  css_str  = font_face_css +
                                             ['body {',
                                              'margin: 0px;',
                                              f'width: {width_px}px;',
                                              font_size_css,
                                              font_family_css,
                                              h_align_css,
                                              v_align_css,
                                              '}',
                                              ]
                                  )
        im       = Image.open(out_path[0])
        im       = im.convert('RGBA')

        self.paste(im,
                   x_left = left,
                   y_top  = top,
                   )


    def text(self,
             text:          str                       = "Default",
             x_left:        float | None              = None,
             x_centre:      float | None              = None,
             x_right:       float | None              = None,
             y_ascender:    float | None              = None,
             y_top:         float | None              = None,
             y_middle:      float | None              = None,
             y_baseline:    float | None              = None,
             y_bottom:      float | None              = None,
             y_descender:   float | None              = None,
             fill:          tuple[int, int, int]      = (0, 0, 0),
             font:          ImageFont.FreeTypeFont | None = None,
             spacing:       float | None              = None,
             chrs_per_line: int | None                = None,
             width:         float | None              = None,
             ) -> tuple[float, float, float, float]:
        """
        Add some text to the card.
        - x, y are relative to the top left of the card excluding the gutters.
        - The font must be an ImageFont object.
        - `spacing` is the spacing between lines, in the default unit.
          If None, defaults to `text_line_spacing`.
        - If given, newlines will be inserted at `chrs_per_line`.
        - `width` is the desired width of the text box, in the default unit.
          Cannot be specified together with `chrs_per_line`.

        Returns the bounding box, as per
        https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textbbox
        but in the default unit.
        This is relative to the top of the card content, excluding the gutter.
        """

        if width is not None and chrs_per_line is not None:
            raise ValueError("Cannot specify both 'width' and 'chrs_per_line'")

        if spacing is None:
            spacing = self.text_line_spacing

        # Switch to pixels

        x_left      = self.to_px(x_left)
        x_centre    = self.to_px(x_centre)
        x_right     = self.to_px(x_right)
        y_ascender  = self.to_px(y_ascender)
        y_top       = self.to_px(y_top)
        y_middle    = self.to_px(y_middle)
        y_baseline  = self.to_px(y_baseline)
        y_bottom    = self.to_px(y_bottom)
        y_descender = self.to_px(y_descender)
        spacing     = self.to_px(spacing)

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

        chrs_per_line = self._calc_chrs_per_line(text, width, chrs_per_line,
                                                 font, spacing)
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
    def _insert_new_lines(text: str, len: int) -> str:
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


    def _calc_chrs_per_line(self,
                            text:          str,
                            width:         float | None,
                            chrs_per_line: int | None,
                            font:          ImageFont.FreeTypeFont | None,
                            spacing:       float,
                            ) -> int | None:
        """
        Calculate the optimal `chrs_per_line` for the given text and width.

        If `chrs_per_line` is given, return it as-is.
        If `width` is given, use `optimise()` to find the best value.
        If neither is given, return None.
        """
        if chrs_per_line is not None:
            return chrs_per_line

        if width is None:
            return None

        target_width_px = self.to_px(width)
        draw            = ImageDraw.Draw(self._im_with_gutters)

        def assessment(chrs):
            wrapped    = self._insert_new_lines(text, chrs)
            bbox       = draw.textbbox(xy      = (0, 0),
                                       text    = wrapped,
                                       font    = font,
                                       spacing = spacing,
                                       )
            bbox_width = bbox[2] - bbox[0]
            acceptable = bbox_width <= target_width_px
            return (bbox_width - target_width_px, acceptable)

        return optimise(len(text), assessment)


    def image(self) -> Image.Image:
        """
        Return the card image, excluding the gutters.
        """
        return self._im_with_gutters.crop(box = (self._gutter_px,
                                                 self._gutter_px,
                                                 self._gutter_px + self._width_px,
                                                 self._gutter_px + self._height_px,
                                                 ))


    def image_with_gutters(self) -> Image.Image:
        """
        Return the card image, including the gutters.
        """
        return self._im_with_gutters.copy()


    def colour_wash(self, colour: tuple[int, int, int, int]) -> None:
        """
        Give the card a wash of colour.
        Transparency will be preserved.
        """

        self._im_with_gutters = self.colour_wash_image(self._im_with_gutters, colour)


    @staticmethod
    def colour_wash_image(im:     Image.Image,
                          colour: tuple[int, int, int, int],
                          ) -> Image.Image:
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
