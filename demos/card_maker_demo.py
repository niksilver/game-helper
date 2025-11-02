if __name__ == '__main__':
    print("This is a module, not a standalone script")
    import sys
    sys.exit(0)


from PIL import Image
from PIL import ImageFont
from card_maker import CardMaker


assets_dir  = 'demos/assets'

# font_file = '/usr/share/fonts/opentype/urw-base35/URWBookman-LightItalic.otf'
font_file = '/usr/share/fonts/opentype/urw-base35/URWBookman-Light.otf'
font_tiny  = ImageFont.truetype(font = font_file,
                                size = 20,    # Pixels, same as the gutter
                                )
font_small = ImageFont.truetype(font = font_file,
                                size = 28,
                                )
font_large = ImageFont.truetype(font = font_file,
                                size = 58,
                                )

# A CardMaker we'll use as the base, with default units px

base_maker = CardMaker(width    = 400,
                       height   = 500,
                       gutter   = 20,
                       unit     = 'px',
                       width_mm = 60,
                       )

# Another CardMaker, same dimesions, but default unit is mm

base_maker_mm = CardMaker(width    = 60,
                          height   = 75,
                          gutter   = 3,
                          unit     = 'mm',
                          width_px = 400,
                          )


def simple(wording):
    """
    Return a card with a border and some wording.
    Our border image includes a gutter, so we'll paste it accordingly.
    """

    maker = base_maker.copy()

    border_im = Image.open(assets_dir + '/card-border-with-gutter.png')
    border_im = border_im.resize(size = maker.size_with_gutters_px)

    maker.paste(im     = border_im,
                x_left = -maker.gutter,
                y_top  = -maker.gutter,
                )
    maker.text(text   = 'This is top left (and in a bit)',
               x_left = 20,
               y_top  = 20,
               font   = font_tiny,
               )
    maker.text(text     = wording,
               x_centre = maker.width / 2,
               y_middle = maker.height / 2,
               font     = font_large,
               )
    return maker


def text_positioning():
    """
    Return a card with a border and centred wording.
    Our border image includes a gutter, so we'll paste it accordingly.
    """

    maker = base_maker_mm.copy()

    border_im = Image.open(assets_dir + '/card-border-with-gutter.png')
    border_im = border_im.resize(size = maker.size_with_gutters_px)

    # Text on the top line
    maker.text(text   = 'Left-top',
               x_left = 0,
               y_top  = 0,
               font   = font_small,
               )
    maker.text(text     = 'CT',
               x_centre = maker.width / 2,
               y_top    = 0,
               font     = font_small,
               )
    maker.text(text    = 'Right-top',
               x_right = maker.width,
               y_top   = 0,
               font    = font_small,
               )

    # Text in the middle
    maker.text(text     = 'LM',
               x_left   = 0,
               y_middle = maker.height / 2,
               font     = font_small,
               )
    maker.text(text     = 'Centre-middle.',
               x_centre = maker.width / 2,
               y_middle = maker.height / 2,
               font     = font_small,
               )
    maker.text(text     = 'RM',
               x_right  = maker.width,
               y_middle = maker.height / 2,
               font     = font_small,
               )

    # Text on the bottom
    maker.text(text        = 'Left-bottom',
               x_left      = 0,
               y_descender = maker.height,
               font        = font_small,
               )
    maker.text(text        = 'CB',
               x_centre    = maker.width / 2,
               y_descender = maker.height,
               font        = font_small,
               )
    maker.text(text        = 'Right-bottom',
               x_right     = maker.width,
               y_descender = maker.height,
               font        = font_small,
               )

    return maker


def html():
    """
    Return a yellow card with some HTML content.
    """

    maker = CardMaker(width    = base_maker.width_px,
                      height   = base_maker.height_px,
                      gutter   = base_maker.gutter_px,
                      unit     = 'px',
                      width_mm = base_maker.width_mm,
                      colour = (255, 255, 0, 255),    # Yellow
                      )
    content = """Oh, <i>hi</i>.
        HTML text flows over multiple lines and has a transparent background."""
    maker.html(content,
               x_left = 10,
               y_top  = 10,
               width  = maker.width / 2,
               height = maker.height / 2,
               )
    maker.html('It will also get cut off inside its own box',
               x_left = 10,
               y_top  = 250,
               width  = maker.width / 2,
               height = 65,
               )

    return maker


def bounding_box_demo():
    """
    Make sure the bounding box returned by text() is correct.
    """

    maker = base_maker_mm.copy()

    border_im = Image.open(assets_dir + '/card-border-with-gutter.png')
    border_im = border_im.resize(size = maker.size_with_gutters_px)

    maker.paste(im     = border_im,
                x_left = -maker.gutter,
                y_top  = -maker.gutter,
                )

    text1 = f"This card is {maker.width_mm}mm wide and {maker.height_mm}mm high."
    bbox  = maker.text(text          = text1,
                       x_left        = 10,
                       y_ascender    = 10,
                       font          = font_tiny,
                       chrs_per_line = 20,
                       )

    text2 = f"Bounding box for above text:\nleft = {bbox[0]}mm\ntop = {bbox[1]}mm\nright = {bbox[2]}mm\nbottom = {bbox[3]}mm"
    bbox  = maker.text(text          = text2,
                       x_left        = 10,
                       y_ascender    = maker.height_mm * 0.60,
                       font          = font_tiny,
                       chrs_per_line = 30,
                       )

    return maker
