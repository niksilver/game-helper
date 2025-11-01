if __name__ == '__main__':
    print("This is a module, not a standalone script")
    import sys
    sys.exit(0)


from PIL import Image
from PIL import ImageFont
from card_maker import CardMaker


assets_dir  = 'demos/assets'

font_file = '/usr/share/fonts/opentype/urw-base35/URWBookman-LightItalic.otf'
font_tiny  = ImageFont.truetype(font = font_file,
                                size = 20,    # Pixels, same as the gutter
                                )
font_large = ImageFont.truetype(font = font_file,
                                size = 58,
                                )

base_maker = CardMaker(width    = 400,
                       height   = 500,
                       gutter   = 20,
                       unit     = 'px',
                       width_mm = 60,
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


def html(content):
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
    maker.html(content,
               x_left = 10,
               y_top  = 10,
               width  = maker.width / 2,
               height = maker.height / 2,
               )

    return maker
